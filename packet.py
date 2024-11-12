def new_packet(client, data):
    return {
        "sender": client,
        "data": data,
        "version": 0,
        "source": 0,
        "destination": 0,
        "packet_type": 0,
        "flags": 0,
        "session_id": 0,
        "signature": [],
        "sequence_id": 0,
        "connection_signature": [],
        "fragment_id": 0,
        "payload": [],
        "rmc_request": {},
    }

def get_data(packet):
    return packet["data"]

def get_sender(packet):
    return packet["sender"]

def set_version(packet, version):
    packet["version"] = version

def get_version(packet):
    return packet["version"]

def set_source(packet, source):
    packet["source"] = source

def get_source(packet):
    return packet["source"]

def set_destination(packet, destination):
    packet["destination"] = destination

def get_destination(packet):
    return packet["destination"]

def set_type(packet, packet_type):
    packet["packet_type"] = packet_type

def get_type(packet):
    return packet["packet_type"]

def set_flags(packet, bitmask):
    packet["flags"] = bitmask

def get_flags(packet):
    return packet["flags"]

def has_flag(packet, flag):
    return packet["flags"] & flag != 0

def add_flag(packet, flag):
    packet["flags"] |= flag

def clear_flag(packet, flag):
    packet["flags"] &= ~flag

def set_session_id(packet, session_id):
    packet["session_id"] = session_id

def get_session_id(packet):
    return packet["session_id"]

def set_signature(packet, signature):
    packet["signature"] = signature

def get_signature(packet):
    return packet["signature"]

def set_sequence_id(packet, sequence_id):
    packet["sequence_id"] = sequence_id

def get_sequence_id(packet):
    return packet["sequence_id"]

def set_connection_signature(packet, connection_signature):
    packet["connection_signature"] = connection_signature

def get_connection_signature(packet):
    return packet["connection_signature"]

def set_fragment_id(packet, fragment_id):
    packet["fragment_id"] = fragment_id

def get_fragment_id(packet):
    return packet["fragment_id"]

def set_payload(packet, payload):
    packet["payload"] = payload

def get_payload(packet):
    return packet["payload"]

def get_rmc_request(packet):
    return packet["rmc_request"]