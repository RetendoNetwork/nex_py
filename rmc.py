from streams import StreamIn, StreamOut, StreamSettings
from library_version import LibraryVersions
from endpoint_interface import EndpointInterface
from nex_types.class_version_container import ClassVersionContainer
from result_codes import error_mask


class RMC:
    def __init__(self, endpoint: EndpointInterface):
        self.endpoint = endpoint
        self.is_request = bool
        self.is_success = bool
        self.is_hpp = bool
        self.protocol_id = 0
        self.protocol_name = ""
        self.call_id = 0
        self.method_id = 0
        self.method_name = ""
        self.error_code = 0
        self.version_container = None
        self.parameters = None

    def copy(self):
        copied = RMC(self.endpoint)
        copied.is_request = self.is_request
        copied.is_success = self.is_success
        copied.is_hpp = self.is_hpp
        copied.protocol_id = self.protocol_id
        copied.protocol_name = self.protocol_name
        copied.call_id = self.call_id
        copied.method_id = self.method_id
        copied.method_name = self.method_name
        copied.error_code = self.error_code

        if self.parameters is not None:
            copied.parameters = self.parameters[:]

        return copied

    def from_bytes(self, data):
        if self.endpoint.use_verbose_rmc():
            return self.decode_verbose(data)
        else:
            return self.decode_packed(data)

    def decode_packed(self, data):
        stream = StreamIn(data, self.endpoint.library_versions(), self.endpoint.byte_stream_settings())

        length, err = stream.read_uint32_le()
        if err:
            raise ValueError(f"Failed to read RMC Message size. {err}")

        if stream.remaining() != length:
            raise ValueError("RMC Message has unexpected size")

        protocol_id, err = stream.read_uint8()
        if err:
            raise ValueError(f"Failed to read RMC Message protocol ID. {err}")

        self.protocol_id = protocol_id & ~0x80

        if self.protocol_id == 0x7F:
            self.protocol_id, err = stream.read_uint16_le()
            if err:
                raise ValueError(f"Failed to read RMC Message extended protocol ID. {err}")

        if protocol_id & 0x80 != 0:
            self.is_request = True
            self.call_id, err = stream.read_uint32_le()
            if err:
                raise ValueError(f"Failed to read RMC Message (request) call ID. {err}")

            self.method_id, err = stream.read_uint32_le()
            if err:
                raise ValueError(f"Failed to read RMC Message (request) method ID. {err}")

            self.parameters = stream.read_remaining()
        else:
            self.is_request = False
            self.is_success, err = stream.read_bool()
            if err:
                raise ValueError(f"Failed to read RMC Message (response) error check. {err}")

            if self.is_success:
                self.call_id, err = stream.read_uint32_le()
                if err:
                    raise ValueError(f"Failed to read RMC Message (response) call ID. {err}")

                self.method_id, err = stream.read_uint32_le()
                if err:
                    raise ValueError(f"Failed to read RMC Message (response) method ID. {err}")

                self.method_id = self.method_id & ~0x8000
                self.parameters = stream.read_remaining()
            else:
                self.error_code, err = stream.read_uint32_le()
                if err:
                    raise ValueError(f"Failed to read RMC Message (response) error code. {err}")

                self.call_id, err = stream.read_uint32_le()
                if err:
                    raise ValueError(f"Failed to read RMC Message (response) call ID. {err}")

        return None

    def decode_verbose(self, data):
        stream = StreamIn(data, self.endpoint.library_versions(), self.endpoint.byte_stream_settings())

        length, err = stream.read_uint32_le()
        if err:
            raise ValueError(f"Failed to read RMC Message size. {err}")

        if stream.remaining() != length:
            raise ValueError("RMC Message has unexpected size")

        self.protocol_name = ""
        if err := self.protocol_name.extract_from(stream):
            raise ValueError(f"Failed to read RMC Message protocol name. {err}")

        self.is_request, err = stream.read_bool()
        if err:
            raise ValueError(f"Failed to read RMC Message \"is request\" bool. {err}")

        if self.is_request:
            self.call_id, err = stream.read_uint32_le()
            if err:
                raise ValueError(f"Failed to read RMC Message (request) call ID. {err}")

            self.method_name = ""
            if err := self.method_name.extract_from(stream):
                raise ValueError(f"Failed to read RMC Message (request) method name. {err}")

            version_container = ClassVersionContainer()
            if err := version_container.extract_from(stream):
                raise ValueError(f"Failed to read RMC Message ClassVersionContainer. {err}")

            self.version_container = version_container
            self.parameters = stream.read_remaining()
        else:
            self.is_success, err = stream.read_bool()
            if err:
                raise ValueError(f"Failed to read RMC Message (response) error check. {err}")

            if self.is_success:
                self.call_id, err = stream.read_uint32_le()
                if err:
                    raise ValueError(f"Failed to read RMC Message (response) call ID. {err}")

                self.method_name = ""
                if err := self.method_name.extract_from(stream):
                    raise ValueError(f"Failed to read RMC Message (response) method name. {err}")

                self.parameters = stream.read_remaining()
            else:
                self.error_code, err = stream.read_uint32_le()
                if err:
                    raise ValueError(f"Failed to read RMC Message (response) error code. {err}")

                self.call_id, err = stream.read_uint32_le()
                if err:
                    raise ValueError(f"Failed to read RMC Message (response) call ID. {err}")

        return None

    def to_bytes(self):
        if self.endpoint.use_verbose_rmc():
            return self.encode_verbose()
        else:
            return self.encode_packed()

    def encode_packed(self):
        stream = StreamOut(self.endpoint.library_versions(), self.endpoint.byte_stream_settings())

        protocol_id_flag = 0x80 if self.is_request else 0

        if not self.is_hpp or (self.is_hpp and self.is_request):
            if self.protocol_id < 0x80:
                stream.write_uint8(self.protocol_id | protocol_id_flag)
            else:
                stream.write_uint8(0x7F | protocol_id_flag)
                stream.write_uint16_le(self.protocol_id)

        if self.is_request:
            stream.write_uint32_le(self.call_id)
            stream.write_uint32_le(self.method_id)

            if self.parameters:
                stream.grow(len(self.parameters))
                stream.write_bytes_next(self.parameters)
        else:
            stream.write_bool(self.is_success)

            if self.is_success:
                stream.write_uint32_le(self.call_id)
                stream.write_uint32_le(self.method_id | 0x8000)

                if self.parameters:
                    stream.grow(len(self.parameters))
                    stream.write_bytes_next(self.parameters)
            else:
                stream.write_uint32_le(self.error_code)
                stream.write_uint32_le(self.call_id)

        serialized = stream.bytes()

        message = StreamOut(self.endpoint.library_versions(), self.endpoint.byte_stream_settings())

        message.write_uint32_le(len(serialized))
        message.grow(len(serialized))
        message.write_bytes_next(serialized)

        return message.bytes()

    def encode_verbose(self):
        stream = StreamOut(self.endpoint.library_versions(), self.endpoint.byte_stream_settings())

        self.protocol_name.write_to(stream)
        stream.write_bool(self.is_request)

        if self.is_request:
            stream.write_uint32_le(self.call_id)
            self.method_name.write_to(stream)

            if self.version_container:
                self.version_container.write_to(stream)
            else:
                # Fail safe. This is always present even if no structures are used
                stream.write_uint32_le(0)

            if self.parameters:
                stream.grow(len(self.parameters))
                stream.write_bytes_next(self.parameters)
        else:
            stream.write_bool(self.is_success)

            if self.is_success:
                stream.write_uint32_le(self.call_id)
                self.method_name.write_to(stream)

                if self.parameters:
                    stream.grow(len(self.parameters))
                    stream.write_bytes_next(self.parameters)
            else:
                stream.write_uint32_le(self.error_code)
                stream.write_uint32_le(self.call_id)

        serialized = stream.bytes()

        message = StreamOut(self.endpoint.library_versions(), self.endpoint.byte_stream_settings())

        message.write_uint32_le(len(serialized))
        message.grow(len(serialized))
        message.write_bytes_next(serialized)

        return message.bytes()


def new_rmc_message(endpoint):
    return RMC(endpoint)


def new_rmc_request(endpoint):
    message = RMC(endpoint)
    message.is_request = True
    return message


def new_rmc_success(endpoint, parameters):
    message = RMC(endpoint)
    message.is_request = False
    message.is_success = True
    message.parameters = parameters
    return message


def new_rmc_error(endpoint, error_code):
    if error_code & error_mask == 0:
        error_code |= error_mask

    message = RMC(endpoint)
    message.is_request = False
    message.is_success = False
    message.error_code = error_code
    return message