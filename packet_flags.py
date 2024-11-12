# Flag constants for PRUDP

# FlagAck is the ID for the PRUDP Ack Flag
FlagAck = 0x1

# FlagReliable is the ID for the PRUDP Reliable Flag
FlagReliable = 0x2

# FlagNeedsAck is the ID for the PRUDP NeedsAck Flag
FlagNeedsAck = 0x4

# FlagHasSize is the ID for the PRUDP HasSize Flag
FlagHasSize = 0x8

# FlagMultiAck is the ID for the PRUDP MultiAck Flag
FlagMultiAck = 0x200

# Dictionary of flags for easy access
flags = {
    "FlagAck": FlagAck,
    "FlagReliable": FlagReliable,
    "FlagNeedsAck": FlagNeedsAck,
    "FlagHasSize": FlagHasSize,
    "FlagMultiAck": FlagMultiAck
}