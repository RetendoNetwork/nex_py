import reflect
import strconv


error_mask = 1 << 31

class ResultCodes:
    def __init__(self):
        self.Core = self.Core()
        self.DDL = self.DDL()
        self.RendezVous = self.RendezVous()

    class Core:
        def __init__(self):
            self.Unknown = 0
            self.NotImplemented = 0
            self.InvalidPointer = 0
            self.OperationAborted = 0
            self.Exception = 0
            self.AccessDenied = 0
            self.InvalidHandle = 0
            self.InvalidIndex = 0
            self.OutOfMemory = 0
            self.InvalidArgument = 0
            self.Timeout = 0
            self.InitializationFailure = 0
            self.CallInitiationFailure = 0
            self.RegistrationError = 0
            self.BufferOverflow = 0
            self.InvalidLockState = 0
            self.InvalidSequence = 0
            self.SystemError = 0
            self.Cancelled = 0

    class DDL:
        def __init__(self):
            self.InvalidSignature = 0
            self.IncorrectVersion = 0

    class RendezVous:
        def __init__(self):
            self.ConnectionFailure = 0
            self.NotAuthenticated = 0
            self.InvalidUsername = 0
            self.InvalidPassword = 0
            self.UsernameAlreadyExists = 0
            self.AccountDisabled = 0
            self.AccountExpired = 0
            self.InvalidPID = 0

ResultNames = {
    0x00010001: "Unknown",
    0x00010002: "Not Implemented",
    0x00010003: "Invalid Pointer",
    0x00010004: "Operation Aborted",
    0x00010005: "Exception",
    0x00010006: "Access Denied",
    0x00010007: "Invalid Handle",
    0x00010008: "Invalid Index",
    0x00010009: "Out of Memory",
    0x0001000A: "Invalid Argument",
    0x0001000B: "Timeout",
    0x0001000C: "Initialization Failure",
    0x0001000D: "Call Initiation Failure",
    0x0001000E: "Registration Error",
    0x0001000F: "Buffer Overflow",
    0x00010010: "Invalid Lock State",
    0x00010011: "Invalid Sequence",
    0x00010012: "System Error",
    0x00010013: "Cancelled",
    0x00020001: "Invalid Signature",
    0x00020002: "Incorrect Version",
    0x00030001: "Connection Failure",
    0x00030002: "Not Authenticated",
    0x00030064: "Invalid Username",
    0x00030065: "Invalid Password",
    0x00030066: "Username Already Exists",
    0x00030067: "Account Disabled",
    0x00030068: "Account Expired",
    0x0003006B: "Invalid PID"
}

resultCodes = ResultCodes()

def init_result_codes():
    resultCodes.Core.Unknown = 0x00010001
    resultCodes.Core.NotImplemented = 0x00010002
    resultCodes.Core.InvalidPointer = 0x00010003
    resultCodes.Core.OperationAborted = 0x00010004
    resultCodes.Core.Exception = 0x00010005
    resultCodes.Core.AccessDenied = 0x00010006
    resultCodes.Core.InvalidHandle = 0x00010007
    resultCodes.Core.InvalidIndex = 0x00010008
    resultCodes.Core.OutOfMemory = 0x00010009
    resultCodes.Core.InvalidArgument = 0x0001000A
    resultCodes.Core.Timeout = 0x0001000B
    resultCodes.Core.InitializationFailure = 0x0001000C
    resultCodes.Core.CallInitiationFailure = 0x0001000D
    resultCodes.Core.RegistrationError = 0x0001000E
    resultCodes.Core.BufferOverflow = 0x0001000F
    resultCodes.Core.InvalidLockState = 0x00010010
    resultCodes.Core.InvalidSequence = 0x00010011
    resultCodes.Core.SystemError = 0x00010012
    resultCodes.Core.Cancelled = 0x00010013

    resultCodes.DDL.InvalidSignature = 0x00020001
    resultCodes.DDL.IncorrectVersion = 0x00020002

    resultCodes.RendezVous.ConnectionFailure = 0x00030001
    resultCodes.RendezVous.NotAuthenticated = 0x00030002
    resultCodes.RendezVous.InvalidUsername = 0x00030064
    resultCodes.RendezVous.InvalidPassword = 0x00030065
    resultCodes.RendezVous.UsernameAlreadyExists = 0x00030066
    resultCodes.RendezVous.AccountDisabled = 0x00030067
    resultCodes.RendezVous.AccountExpired = 0x00030068
    resultCodes.RendezVous.InvalidPID = 0x0003006B

    for category_name, category in resultCodes.__dict__.items():
        for field_name, field_value in category.__dict__.items():
            if isinstance(field_value, int):
                ResultNames[field_value] = f"{category_name}::{field_name}"

async def result_code_to_name(result_code):
    name = ResultNames.get(result_code, "")
    
    if not name:
        return f"Invalid Result Code: {result_code}"
    
    return name