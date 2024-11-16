from enum import IntEnum, unique


@unique
class StationURLFlag(IntEnum):
	"""StationURLFlag is an enum of flags used by the StationURL "type" parameter."""
	
	StationURLFlagBehindNAT = 1
	StationURLFlagPublic = 2