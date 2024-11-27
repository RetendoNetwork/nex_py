from typing import Optional

from nex.byte_stream import ByteStreamOut, ByteStreamIn
from nex.endpoint_interface import EndpointInterface
from nex.nex_types.class_version_container import ClassVersionContainer
from nex.nex_types.string import String


class RMC:
    def __init__(self, endpoint: EndpointInterface):
        self.endpoint = endpoint
        self.is_request = bool
        self.is_success = bool
        self.is_hpp = bool
        self.protocol_id = 0
        self.protocol_name = String()
        self.call_id = 0
        self.method_id = 0
        self.method_name = String()
        self.error_code = 0
        self.version_container = ClassVersionContainer()
        self.parameters = b''

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
        copied.parameters = self.parameters[:]
        return copied

    def from_bytes(self, data: bytes) -> Optional[Exception]:
        if self.endpoint.use_verbose_rmc():
            return self.decode_verbose(data)
        else:
            return self.decode_packed(data)

    def decode_packed(self, data: bytes) -> Optional[Exception]:
        stream = ByteStreamIn(data, self.endpoint.library_versions(), self.endpoint.byte_stream_settings())

        try:
            length = stream.read_uint32_le()
            if stream.remaining() != length:
                raise ValueError("RMC Message has unexpected size")

            protocol_id = stream.read_uint8()
            self.protocol_id = protocol_id & ~0x80

            if self.protocol_id == 0x7F:
                self.protocol_id = stream.read_uint16_le()

            if protocol_id & 0x80:
                self.is_request = True
                self.call_id = stream.read_uint32_le()
                self.method_id = stream.read_uint32_le()
                self.parameters = stream.read_remaining()
            else:
                self.is_request = False
                self.is_success = stream.read_bool()
                if self.is_success:
                    self.call_id = stream.read_uint32_le()
                    self.method_id = stream.read_uint32_le() & ~0x8000
                    self.parameters = stream.read_remaining()
                else:
                    self.error_code = stream.read_uint32_le()
                    self.call_id = stream.read_uint32_le()
        except Exception as e:
            return e

        return None

    def decode_verbose(self, data: bytes) -> Optional[Exception]:
        stream = ByteStreamIn(data, self.endpoint.library_versions(), self.endpoint.byte_stream_settings())

        try:
            length = stream.read_uint32_le()
            if stream.remaining() != length:
                raise ValueError("RMC Message has unexpected size")

            self.protocol_name = String("")
            self.is_request = stream.read_bool()
            if self.is_request:
                self.call_id = stream.read_uint32_le()
                self.method_name = String("")
                self.version_container = ClassVersionContainer.new_class_version_container()
                self.parameters = stream.read_remaining()
            else:
                self.is_success = stream.read_bool()
                if self.is_success:
                    self.call_id = stream.read_uint32_le()
                    self.method_name = String("")
                    self.parameters = stream.read_remaining()
                else:
                    self.error_code = stream.read_uint32_le()
                    self.call_id = stream.read_uint32_le()
        except Exception as e:
            return e

        return None

    def bytes(self) -> bytes:
        if self.endpoint.use_verbose_rmc():
            return self.encode_verbose()
        else:
            return self.encode_packed()

    def encode_packed(self) -> bytes:
        stream = ByteStreamOut(self.endpoint.library_versions(), self.endpoint.byte_stream_settings())

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
            if self.parameters != None & len(self.parameters):
                stream.write_bytes_next(self.parameters)
        else:
            stream.write_bool(self.is_success)
            if self.is_success:
                stream.write_uint32_le(self.call_id)
                stream.write_uint32_le(self.method_id | 0x8000)
                if self.parameters != None & len(self.parameters):
                    stream.write_bytes_next(self.parameters)
            else:
                stream.write_uint32_le(self.error_code)
                stream.write_uint32_le(self.call_id)

        serialized = stream.bytes()

        message = ByteStreamOut(self.endpoint.library_versions(), self.endpoint.byte_stream_settings())
        message.write_uint32_le(len(serialized))
        message.write_bytes_next(serialized)

        return message.bytes()

    def encode_verbose(self) -> bytes:
        stream = ByteStreamOut(self.endpoint.library_versions(), self.endpoint.byte_stream_settings())

        self.protocol_name.write_to(stream)
        stream.write_bool(self.is_request)
        if self.is_request:
            stream.write_uint32_le(self.call_id)
            self.method_name.write_to(stream)
            if self.version_container:
                self.method_name.write_to(stream)
            else:
                stream.write_uint32_le(0)
            if self.parameters:
                stream.write_bytes_next(self.parameters)
        else:
            stream.write_bool(self.is_success)
            if self.is_success:
                stream.write_uint32_le(self.call_id)
                self.method_name.write_to(stream)
                if self.parameters:
                    stream.write_bytes_next(self.parameters)
            else:
                stream.write_uint32_le(self.error_code)
                stream.write_uint32_le(self.call_id)

        serialized = stream.bytes()

        message = ByteStreamOut(self.endpoint.byte_stream_settings())
        message.write_uint32_le(len(serialized))
        message.write_bytes_next(serialized)

        return message.bytes()

    def new_rmc_message(endpoint: EndpointInterface):
        return RMC(endpoint)

    def new_rmc_request(endpoint: EndpointInterface):
        msg = RMC(endpoint)
        msg.is_request = True
        return msg

    def new_rmc_success(endpoint: EndpointInterface, parameters):
        msg = RMC(endpoint)
        msg.is_request = False
        msg.is_success = True
        msg.parameters = parameters
        return msg

    def new_rmc_error(endpoint: EndpointInterface, error_code):
        if error_code & 0x8000 == 0:
            error_code |= 0x8000
        msg = RMC(endpoint)
        msg.is_request = False
        msg.is_success = False
        msg.error_code = error_code
        return msg