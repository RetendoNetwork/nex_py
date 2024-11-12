# Counters for managing sequence IDs
sequence_id_manager = {
    "reliable_counter": 0,
    "ping_counter": 0
}

# Increment the counter and return the new value
def increment_counter(counter_name):
    sequence_id_manager[counter_name] += 1
    return sequence_id_manager[counter_name]

# Get the next sequence ID for a packet based on its flags or type
def next_sequence_id(packet):
    if packet_has_flag(packet, "FlagReliable"):
        return increment_counter("reliable_counter")

    if packet_type(packet) == "PingPacket":
        return increment_counter("ping_counter")

    return 0

# Initialize the SequenceIDManager (if needed to reset the counters)
def new_sequence_id_manager():
    global sequence_id_manager
    sequence_id_manager = {
        "reliable_counter": 0,
        "ping_counter": 0
    }

# Example packet flag check function (replace with actual logic)
def packet_has_flag(packet, flag):
    # Implement packet flag checking logic here
    return flag in packet.get("flags", [])

# Example packet type check function (replace with actual logic)
def packet_type(packet):
    # Implement packet type retrieval here
    return packet.get("type", "")