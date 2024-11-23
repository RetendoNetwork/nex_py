from copy import deepcopy


class StreamSettings:
    def __init__(self):
        self.extra_retransmit_timeout_trigger = 0x32
        self.max_packet_retransmissions = 0x14
        self.keep_alive_timeout = 1000
        self.checksum_base = 0
        self.fault_detection_enabled = True
        self.initial_rtt = 0x2EE
        self.syn_initial_rtt = 0xFA
        self.encryption_algorithm = self.new_rc4_encryption()
        self.extra_retransmit_timeout_multiplier = 1.0
        self.window_size = 8
        self.compression_algorithm = self.new_dummy_compression()
        self.rtt_retransmit = 2
        self.retransmit_timeout_multiplier = 1.25
        self.max_silence_time = 10000

    def copy(self):
        return deepcopy(self)

    @staticmethod
    def new_stream_settings():
        return StreamSettings()