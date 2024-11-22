from compression.algorithm import CompressionAlgorithm
from encryption.algorithm import EncryptionAlgorithm


class StreamSettings:
    def __init__(
        self,
        extra_retransmit_timeout_trigger=0x32,
        max_packet_retransmissions=0x14,
        keep_alive_timeout=1000,
        checksum_base=0,
        fault_detection_enabled=True,
        initial_rtt=0x2EE,
        syn_initial_rtt=0xFA,
        encryption_algorithm=EncryptionAlgorithm,
        extra_retransmit_timeout_multiplier=1.0,
        window_size=8,
        compression_algorithm=CompressionAlgorithm,
        rtt_retransmit=2,
        retransmit_timeout_multiplier=1.25,
        max_silence_time=10000,
    ):
        self.extra_retransmit_timeout_trigger = extra_retransmit_timeout_trigger
        self.max_packet_retransmissions = max_packet_retransmissions
        self.keep_alive_timeout = keep_alive_timeout
        self.checksum_base = checksum_base
        self.fault_detection_enabled = fault_detection_enabled
        self.initial_rtt = initial_rtt
        self.syn_initial_rtt = syn_initial_rtt
        self.encryption_algorithm = encryption_algorithm
        self.extra_retransmit_timeout_multiplier = extra_retransmit_timeout_multiplier
        self.window_size = window_size
        self.compression_algorithm = compression_algorithm
        self.rtt_retransmit = rtt_retransmit
        self.retransmit_timeout_multiplier = retransmit_timeout_multiplier
        self.max_silence_time = max_silence_time

    def copy(self):
        return StreamSettings(
            extra_retransmit_timeout_trigger=self.extra_retransmit_timeout_trigger,
            max_packet_retransmissions=self.max_packet_retransmissions,
            keep_alive_timeout=self.keep_alive_timeout,
            checksum_base=self.checksum_base,
            fault_detection_enabled=self.fault_detection_enabled,
            initial_rtt=self.initial_rtt,
            syn_initial_rtt=self.syn_initial_rtt,
            encryption_algorithm=self.encryption_algorithm.copy(),
            extra_retransmit_timeout_multiplier=self.extra_retransmit_timeout_multiplier,
            window_size=self.window_size,
            compression_algorithm=self.compression_algorithm.copy(),
            rtt_retransmit=self.rtt_retransmit,
            retransmit_timeout_multiplier=self.retransmit_timeout_multiplier,
            max_silence_time=self.max_silence_time,
        )