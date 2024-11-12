def write_to(value, writable):
    """Write the uint64 value to the given writable."""
    writable.write_primitive_uint64_le(value)

def extract_from(value, readable):
    """Extract the uint64 value from the given readable."""
    result, err = readable.read_primitive_uint64_le()
    if err:
        return None, err
    return result, None

def copy(value):
    """Return a copy of the uint64 value."""
    return new_primitive_u64(value)

def equals(value1, value2):
    """Check if the two uint64 values are equal."""
    return value1 == value2

def to_string(value):
    """Return a string representation of the uint64 value."""
    return str(value)

def and_op(value1, value2):
    """Run a bitwise AND operation on two uint64 values."""
    return new_primitive_u64(value1 & value2)

def pand(value1, value2):
    """Primitive AND operation on two uint64 values."""
    return value1 & value2

def or_op(value1, value2):
    """Run a bitwise OR operation on two uint64 values."""
    return new_primitive_u64(value1 | value2)

def por(value1, value2):
    """Primitive OR operation on two uint64 values."""
    return value1 | value2

def xor_op(value1, value2):
    """Run a bitwise XOR operation on two uint64 values."""
    return new_primitive_u64(value1 ^ value2)

def pxor(value1, value2):
    """Primitive XOR operation on two uint64 values."""
    return value1 ^ value2

def not_op(value):
    """Run a bitwise NOT operation on a uint64 value."""
    return new_primitive_u64(~value)

def pnot(value):
    """Primitive NOT operation on a uint64 value."""
    return ~value

def andnot(value1, value2):
    """Run a bitwise AND-NOT operation on two uint64 values."""
    return new_primitive_u64(value1 & ~value2)

def pandnot(value1, value2):
    """Primitive AND-NOT operation on two uint64 values."""
    return value1 & ~value2

def lshift(value1, value2):
    """Run a left shift operation on two uint64 values."""
    return new_primitive_u64(value1 << value2)

def plshift(value1, value2):
    """Primitive left shift operation on two uint64 values."""
    return value1 << value2

def rshift(value1, value2):
    """Run a right shift operation on two uint64 values."""
    return new_primitive_u64(value1 >> value2)

def prshift(value1, value2):
    """Primitive right shift operation on two uint64 values."""
    return value1 >> value2

def new_primitive_u64(value):
    """Return a new PrimitiveU64."""
    return value