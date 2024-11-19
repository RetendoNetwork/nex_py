from counter import Counter
from prudp_packet_interface import PRUDPPacketInterface


class PacketDispatchQueue:
    def __init__(self):
        # Initialize with an empty queue and starting sequence ID
        self.queue = {}  # A dictionary to hold packets by sequence ID
        self.next_expected_sequence_id = Counter(2)  # Start at 2, as per the comment in the original Go code

    def queue(self, packet: PRUDPPacketInterface):
        """Adds a packet to the queue"""
        self.queue[packet.sequence_id()] = packet

    def get_next_to_dispatch(self):
        """Returns the next packet to be dispatched, or None if there are no packets"""
        packet = self.queue.get(self.next_expected_sequence_id.value)
        if packet:
            return packet, True
        return None, False

    def dispatched(self, packet: PRUDPPacketInterface):
        """Removes a packet from the queue after dispatch"""
        self.next_expected_sequence_id.next()
        del self.queue[packet.sequence_id()]

    def purge(self):
        """Clears the queue of all pending packets"""
        self.queue.clear()