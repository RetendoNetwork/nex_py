class ByteStreamSettings:
    def __init__(self, string_length_size=2, pid_size=4, use_structure_header=False):
        """
        Initializes the ByteStreamSettings with default or provided values.
        
        :param string_length_size: The size for the string length (default is 2).
        :param pid_size: The size for the PID (default is 4).
        :param use_structure_header: Flag indicating if the structure header should be used (default is False).
        """
        self.string_length_size = string_length_size
        self.pid_size = pid_size
        self.use_structure_header = use_structure_header