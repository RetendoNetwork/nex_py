import hmac
import hashlib
import binascii
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("[HPP]")

# HPPPacket data storage
hpp_packet_data = {
    'access_key_signature': None,
    'password_signature': None,
    'rmc_request': None,
    'payload': None
}

# Set the access key signature
def set_access_key_signature(access_key_signature):
    try:
        access_key_signature_bytes = binascii.unhexlify(access_key_signature)
        hpp_packet_data['access_key_signature'] = access_key_signature_bytes
    except binascii.Error:
        logger.error("Failed to convert AccessKeySignature to bytes")

# Get the access key signature
def get_access_key_signature():
    return hpp_packet_data['access_key_signature']

# Set the password signature
def set_password_signature(password_signature):
    try:
        password_signature_bytes = binascii.unhexlify(password_signature)
        hpp_packet_data['password_signature'] = password_signature_bytes
    except binascii.Error:
        logger.error("Failed to convert PasswordSignature to bytes")

# Get the password signature
def get_password_signature():
    return hpp_packet_data['password_signature']

# Validate the access key signature
def validate_access_key(sender, rmc_request):
    access_key = sender['server']['access_key']
    buffer = rmc_request

    try:
        access_key_bytes = binascii.unhexlify(access_key)
    except binascii.Error as e:
        raise ValueError("[HPP] Invalid access key format") from e

    calculated_signature = calculate_signature(buffer, access_key_bytes)
    if calculated_signature != hpp_packet_data['access_key_signature']:
        raise ValueError("[HPP] Access key signature is not valid")

# Validate the password signature
def validate_password(sender, rmc_request):
    if not sender['server'].get('password_from_pid_handler'):
        raise ValueError("[HPP] Missing passwordFromPIDHandler!")

    pid = sender['pid']
    buffer = rmc_request

    password = sender['server']['password_from_pid_handler'](pid)
    if not password:
        raise ValueError("[HPP] PID does not exist")

    password_bytes = password.encode()
    password_signature_key = derive_kerberos_key(pid, password_bytes)

    calculated_signature = calculate_signature(buffer, password_signature_key)
    if calculated_signature != hpp_packet_data['password_signature']:
        raise ValueError("[HPP] Password signature is invalid")

# Calculate HMAC signature
def calculate_signature(buffer, key):
    mac = hmac.new(key, buffer, hashlib.md5)
    return mac.digest()

# Derive a key based on Kerberos method (for illustration, replace with real method)
def derive_kerberos_key(pid, password_bytes):
    return hashlib.md5(password_bytes + pid.encode()).digest()  # Example derivation

# Initialize a new HPPPacket
def new_hpp_packet(client, data):
    if data:
        hpp_packet_data['payload'] = data
        hpp_packet_data['rmc_request'] = data  # Placeholder for RMC request data setup

        # Simulate parsing the RMC request
        try:
            hpp_packet_data['rmc_request'] = data  # Replace with actual RMC parsing logic
        except Exception as e:
            raise ValueError("[HPP] Error parsing RMC request: " + str(e))