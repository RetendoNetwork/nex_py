from counter import Counter

from prudp_packet_interface import PRUDPPacketInterface


class PacketDispatchQueue:
    def __init__(self):
        self.queue = {}
        self.next_expected_sequence_id = Counter(2)

    def queue(self, packet: 'PRUDPPacketInterface'):
        self.queue[packet.sequence_id()] = packet

    def get_next_to_dispatch(self):
        packet = self.queue.get(self.next_expected_sequence_id.value)
        if packet:
            return packet, True
        return None, False

    def dispatched(self, packet: 'PRUDPPacketInterface'):
        self.next_expected_sequence_id.next()
        del self.queue[packet.sequence_id()]

    def purge(self):
        self.queue.clear()