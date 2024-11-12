# Helper for Counter
class Counter:
    def __init__(self, start_value=0):
        self.value = start_value

    def value(self):
        return self.value

    def increment(self):
        self.value += 1
        return self.value

# Helper to simulate PacketInterface
class PacketInterface:
    def __init__(self, sequence_id):
        self.sequence_id = sequence_id

    def sequence_id(self):
        return self.sequence_id

# Functions for PacketManager

def next_packet_manager(packet_manager):
    packet = None

    for i in range(len(packet_manager["packets"])):
        if packet_manager["current_sequence_id"].value() == packet_manager["packets"][i].sequence_id():
            packet = packet_manager["packets"][i]
            remove_by_index(packet_manager, i)
            packet_manager["current_sequence_id"].increment()
            break

    return packet

def push_packet_manager(packet_manager, packet):
    packet_manager["packets"].append(packet)

def remove_by_index(packet_manager, i):
    # Remove the packet by swapping the last element and shortening the list
    packet_manager["packets"][i] = packet_manager["packets"][-1]
    packet_manager["packets"] = packet_manager["packets"][:-1]

# Function to create a new PacketManager
def new_packet_manager():
    return {
        "current_sequence_id": Counter(0),
        "packets": [],
    }