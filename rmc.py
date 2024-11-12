# Constants and helper functions for protocol and error handling
ERROR_MASK = 0x80000000

# Stream simulation (placeholder functions, assumes `stream` library or similar byte handling is available)
def read_uint8(data, offset):
    return data[offset], offset + 1

def read_uint16_le(data, offset):
    return int.from_bytes(data[offset:offset+2], "little"), offset + 2

def read_uint32_le(data, offset):
    return int.from_bytes(data[offset:offset+4], "little"), offset + 4

def write_uint8(value):
    return value.to_bytes(1, "little")

def write_uint16_le(value):
    return value.to_bytes(2, "little")

def write_uint32_le(value):
    return value.to_bytes(4, "little")

# RMC Request Management
def new_rmc_request():
    return {
        "protocolID": 0,
        "customID": 0,
        "callID": 0,
        "methodID": 0,
        "parameters": b''
    }

def set_protocol_id(request, protocol_id):
    request["protocolID"] = protocol_id

def set_custom_id(request, custom_id):
    request["customID"] = custom_id

def set_call_id(request, call_id):
    request["callID"] = call_id

def set_method_id(request, method_id):
    request["methodID"] = method_id

def set_parameters(request, parameters):
    request["parameters"] = parameters

def from_bytes_rmc_request(data):
    if len(data) < 13:
        raise ValueError("[RMC] Data size less than minimum")
    
    request = new_rmc_request()
    offset = 4  # skip initial 4 bytes for size

    protocol_id, offset = read_uint8(data, offset)
    set_protocol_id(request, protocol_id ^ 0x80)

    if request["protocolID"] == 0x7f:
        custom_id, offset = read_uint16_le(data, offset)
        set_custom_id(request, custom_id)

    call_id, offset = read_uint32_le(data, offset)
    set_call_id(request, call_id)

    method_id, offset = read_uint32_le(data, offset)
    set_method_id(request, method_id)

    request["parameters"] = data[offset:]
    return request

def to_bytes_rmc_request(request):
    body = bytearray()
    body.extend(write_uint8(request["protocolID"] | 0x80))

    if request["protocolID"] == 0x7f:
        body.extend(write_uint16_le(request["customID"]))

    body.extend(write_uint32_le(request["callID"]))
    body.extend(write_uint32_le(request["methodID"]))
    body.extend(request["parameters"])

    return body

# RMC Response Management
def new_rmc_response(protocol_id, call_id):
    return {
        "protocolID": protocol_id,
        "customID": 0,
        "success": 0,
        "callID": call_id,
        "methodID": 0,
        "data": b'',
        "errorCode": 0
    }

def set_success_response(response, method_id, data):
    response["success"] = 1
    response["methodID"] = method_id
    response["data"] = data

def set_error_response(response, error_code):
    response["success"] = 0
    response["errorCode"] = error_code | ERROR_MASK

def to_bytes_rmc_response(response):
    body = bytearray()

    if response["protocolID"] > 0:
        body.extend(write_uint8(response["protocolID"]))
        if response["protocolID"] == 0x7f:
            body.extend(write_uint16_le(response["customID"]))
    
    body.extend(write_uint8(response["success"]))

    if response["success"] == 1:
        body.extend(write_uint32_le(response["callID"]))
        body.extend(write_uint32_le(response["methodID"] | 0x8000))
        if response["data"]:
            body.extend(response["data"])
    else:
        body.extend(write_uint32_le(response["errorCode"]))
        body.extend(write_uint32_le(response["callID"]))

    return body