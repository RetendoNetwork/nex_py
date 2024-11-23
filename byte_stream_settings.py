class ByteStreamSettings:
    def __init__(self, string_length_size=2, pid_size=4, use_structure_header=False):
        self.string_length_size = string_length_size
        self.pid_size = pid_size
        self.use_structure_header = use_structure_header

    @staticmethod
    def new_byte_stream_settings():
        return ByteStreamSettings()