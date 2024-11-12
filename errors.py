import reflect
import strconv

error_mask = 1 << 31

class nexerrors:
    Core = {
        "Unknown": 0x00010001,
        "NotImplemented": 0x00010002,
        "InvalidPointer": 0x00010003,
        "OperationAborted": 0x00010004,
        "Exception": 0x00010005,
        "AccessDenied": 0x00010006,
        "InvalidHandle": 0x00010007,
        "InvalidIndex": 0x00010008,
        "OutOfMemory": 0x00010009,
        "InvalidArgument": 0x0001000A,
        "Timeout": 0x0001000B,
        "InitializationFailure": 0x0001000C,
        "CallInitiationFailure": 0x0001000D,
        "RegistrationError": 0x0001000E,
        "BufferOverflow": 0x0001000F,
        "InvalidLockState": 0x00010010,
        "InvalidSequence": 0x00010011,
        "SystemError": 0x00010012,
        "Cancelled": 0x00010013
    }

    DDL = {
        "InvalidSignature": 0x00020001,
        "IncorrectVersion": 0x00020002
    }

    RendezVous = {
        "ConnectionFailure": 0x00030001,
        "NotAuthenticated": 0x00030002,
        "InvalidUsername": 0x00030064,
        "InvalidPassword": 0x00030065,
        "UsernameAlreadyExists": 0x00030066,
        "AccountDisabled": 0x00030067,
        "AccountExpired": 0x00030068,
        "ConcurrentLoginDenied": 0x00030069,
        "EncryptionFailure": 0x0003006A,
        "InvalidPID": 0x0003006B,
        "MaxConnectionsReached": 0x0003006C,
        "InvalidGID": 0x0003006D,
        "InvalidControlScriptID": 0x0003006E,
        "InvalidOperationInLiveEnvironment": 0x0003006F,
        "DuplicateEntry": 0x00030070,
        "ControlScriptFailure": 0x00030071,
        "ClassNotFound": 0x00030072,
        "SessionVoid": 0x00030073,
        "DDLMismatch": 0x00030075,
        "InvalidConfiguration": 0x00030076,
        "SessionFull": 0x000300C8,
        "InvalidGatheringPassword": 0x000300C9,
        "WithoutParticipationPeriod": 0x000300CA,
        "PersistentGatheringCreationMax": 0x000300CB,
        "PersistentGatheringParticipationMax": 0x000300CC,
        "DeniedByParticipants": 0x000300CD,
        "ParticipantInBlackList": 0x000300CE,
        "GameServerMaintenance": 0x000300CF,
        "OperationPostpone": 0x000300D0,
        "OutOfRatingRange": 0x000300D1,
        "ConnectionDisconnected": 0x000300D2,
        "InvalidOperation": 0x000300D3,
        "NotParticipatedGathering": 0x000300D4,
        "MatchmakeSessionUserPasswordUnmatch": 0x000300D5,
        "MatchmakeSessionSystemPasswordUnmatch": 0x000300D6,
        "UserIsOffline": 0x000300D7,
        "AlreadyParticipatedGathering": 0x000300D8,
        "PermissionDenied": 0x000300D9,
        "NotFriend": 0x000300DA,
        "SessionClosed": 0x000300DB,
        "DatabaseTemporarilyUnavailable": 0x000300DC,
        "InvalidUniqueID": 0x000300DD,
        "MatchmakingWithdrawn": 0x000300DE,
        "LimitExceeded": 0x000300DF,
        "AccountTemporarilyDisabled": 0x000300E0,
        "PartiallyServiceClosed": 0x000300E1,
        "ConnectionDisconnectedForConcurrentLogin": 0x000300E2
    }

    PythonCore = {
        "Exception": 0x00040001,
        "TypeError": 0x00040002,
        "IndexError": 0x00040003,
        "InvalidReference": 0x00040004,
        "CallFailure": 0x00040005,
        "MemoryError": 0x00040006,
        "KeyError": 0x00040007,
        "OperationError": 0x00040008,
        "ConversionError": 0x00040009,
        "ValidationError": 0x0004000A
    }

    Transport = {
        "Unknown": 0x00050001,
        "ConnectionFailure": 0x00050002,
        "InvalidURL": 0x00050003,
        "InvalidKey": 0x00050004,
        "InvalidURLType": 0x00050005,
        "DuplicateEndpoint": 0x00050006,
        "IOError": 0x00050007,
        "Timeout": 0x00050008,
        "ConnectionReset": 0x00050009,
        "IncorrectRemoteAuthentication": 0x0005000A,
        "ServerRequestError": 0x0005000B,
        "DecompressionFailure": 0x0005000C,
        "ReliableSendBufferFullFatal": 0x0005000D,
        "UPnPCannotInit": 0x0005000E,
        "UPnPCannotAddMapping": 0x0005000F,
        "NatPMPCannotInit": 0x00050010,
        "NatPMPCannotAddMapping": 0x00050011,
        "UnsupportedNAT": 0x00050013,
        "DNSError": 0x00050014,
        "ProxyError": 0x00050015,
        "DataRemaining": 0x00050016,
        "NoBuffer": 0x00050017,
        "NotFound": 0x00050018,
        "TemporaryServerError": 0x00050019,
        "PermanentServerError": 0x0005001A,
        "ServiceUnavailable": 0x0005001B,
        "ReliableSendBufferFull": 0x0005001C,
        "InvalidStation": 0x0005001D,
        "InvalidSubStreamID": 0x0005001E,
        "PacketBufferFull": 0x0005001F,
        "NatTraversalError": 0x00050020,
        "NatCheckError": 0x00050021
    }

    DOCore = {
        "StationNotReached": 0x00060001,
        "TargetStationDisconnect": 0x00060002,
        "LocalStationLeaving": 0x00060003,
        "ObjectNotFound": 0x00060004,
        "InvalidRole": 0x00060005,
        "CallTimeout": 0x00060006,
        "RMCDispatchFailed": 0x00060007,
        "MigrationInProgress": 0x00060008,
        "NoAuthority": 0x00060009,
        "NoTargetStationSpecified": 0x0006000A,
        "JoinFailed": 0x0006000B,
        "JoinDenied": 0x0006000C,
        "ConnectivityTestFailed": 0x0006000D,
        "Unknown": 0x0006000E,
        "UnfreedReferences": 0x0006000F,
        "JobTerminationFailed": 0x00060010,
        "InvalidState": 0x00060011,
        "FaultRecoveryFatal": 0x00060012,
        "FaultRecoveryJobProcessFailed": 0x00060013,
        "StationInconsitency": 0x00060014,
        "AbnormalMasterState": 0x00060015,
        "VersionMismatch": 0x00060016
    }

    FPD = {
        "NotInitialized": 0x00650000,
        "AlreadyInitialized": 0x00650001,
        "NotConnected": 0x00650002,
        "Connected": 0x00650003,
        "InitializationFailure": 0x00650004,
        "OutOfMemory": 0x00650005,
        "RmcFailed": 0x00650006,
        "InvalidArgument": 0x00650007,
        "InvalidLocalAccountID": 0x00650008,
        "InvalidPrincipalID": 0x00650009,
        "InvalidLocalFriendCode": 0x0065000A,
        "LocalAccountNotExists": 0x0065000B,
        "LocalAccountNotLoaded": 0x0065000C,
        "LocalAccountAlreadyLoaded": 0x0065000D,
        "FriendAlreadyExists": 0x0065000E,
        "FriendNotExists": 0x0065000F,
        "FriendNumMax": 0x00650010,
        "NotFriend": 0x00650011
    }

    Shm = {
        "AlreadyRegistered": 0x001F0001,
        "NotRegistered": 0x001F0002,
        "Terminated": 0x001F0003,
        "AccessDenied": 0x001F0004,
        "VersionMismatch": 0x001F0005
    }

def get_error_code(category, error_name):
    return getattr(nexerrors, category, {}).get(error_name, None)

def is_error(error_code):
    return error_code >= error_mask

ErrorNames = {}

def error_name_from_code(error_code: int) -> str:
    name = ErrorNames.get(error_code, "")

    if not name:
        return f"Invalid Error Code: {error_code}"

    return name