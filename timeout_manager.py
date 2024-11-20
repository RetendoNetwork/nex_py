import time
import threading

from nex.mutex_map import MutexMap
from nex.streams import StreamSettings
from nex.timeout import Timeout
from nex.prudp_packet import PRUDPPacket
from nex.prudp_packet_interface import PRUDPPacketInterface


class TimeoutManager:
    def __init__(self):
        self.ctx = threading.Event()
        self.packets = MutexMap()
        self.stream_settings = StreamSettings()

    def schedule_packet_timeout(self, packet: PRUDPPacketInterface):
        # Simulate the PRUDP endpoint and compute the RTO (Retransmission Timeout)
        rto = packet.sender.endpoint.compute_retransmit_timeout(packet)
        timeout = Timeout()
        timeout.rto = rto
        timeout.ctx = threading.Timer(rto, self.start, args=(packet,))
        timeout.ctx.start()
        packet.set_timeout(timeout)

        self.packets.set(packet.sequence_id(), packet)

    def acknowledge_packet(self, sequence_id):
        self.packets.run_and_delete(sequence_id, self.handle_acknowledgement)

    def handle_acknowledgement(self, sequence_id, packet: PRUDPPacketInterface):
        if packet.send_count() >= self.stream_settings.rtt_retransmit:
            rtt_m = time.time() - packet.sent_at
            packet.sender.connection.rtt.adjust(rtt_m)

    def start(self, packet: PRUDPPacketInterface):
        if packet.get_timeout()._ctx.is_alive():
            packet.get_timeout()._ctx.cancel()

        connection = packet.sender.connection

        if connection.connection_state != 'connected':
            return

        if self.packets.has(packet.sequence_id()):
            if packet.send_count() < self.stream_settings.max_packet_retransmissions:
                endpoint = packet.sender.endpoint
                packet.increment_send_count()
                packet.set_sent_at(time.time())

                rto = endpoint.compute_retransmit_timeout(packet)
                timeout = packet.get_timeout()
                timeout.rto = rto
                timeout.ctx = threading.Timer(rto, self.start, args=(packet,))
                timeout.ctx.start()

                # Resend the packet
                server = connection.endpoint.server
                data = packet.bytes()
                server.send_raw(connection.socket, data)
            else:
                connection.lock()
                connection.cleanup()

    def stop(self):
        self.ctx.set()  # Stop the timeout manager

        self.packets.clear(lambda key, value: value.cancel())