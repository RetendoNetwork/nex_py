import hmac
import hashlib
import os
import struct
import io
from Crypto.Cipher import ARC4

from nex_types.pid import PID
from byte_stream_in import ByteStreamIn
from byte_stream_out import ByteStreamOut
from nex_types.buffer import Buffer
from nex_types.datetime import DateTime


class KerberosEncryption:
    def __init__(self, key):
        self.key = key

    def validate(self, buffer):
        data = buffer[:-16]
        checksum = buffer[-16:]
        mac = hmac.new(self.key, data, hashlib.md5)
        return hmac.compare_digest(checksum, mac.digest())

    def decrypt(self, buffer):
        if not self.validate(buffer):
            raise ValueError("Invalid Kerberos checksum (incorrect password)")

        cipher = ARC4.new(self.key)
        decrypted = cipher.decrypt(buffer[:-16])
        return decrypted

    def encrypt(self, buffer):
        cipher = ARC4.new(self.key)
        encrypted = cipher.encrypt(buffer)
        mac = hmac.new(self.key, encrypted, hashlib.md5)
        return encrypted + mac.digest()

def new_kerberos_encryption(key):
    return KerberosEncryption(key)

class KerberosTicket:
    def __init__(self):
        self.session_key = None
        self.target_pid = PID
        self.internal_data = Buffer

    def encrypt(self, key, stream: 'ByteStreamOut'):
        encryption = KerberosEncryption(key)
        stream.write(self.session_key)
        self.target_pid.write_to(stream)
        self.internal_data.write_to(stream)
        return encryption.encrypt(stream)

def new_kerberos_ticket():
    return KerberosTicket()

class KerberosTicketInternalData:
    def __init__(self, server):
        self.server = server
        self.issued = DateTime
        self.source_pid = PID
        self.session_key = None

    def encrypt(self, key, stream: 'ByteStreamOut'):
        self.issued.write_to(stream)
        self.source_pid.write_to(stream)
        stream.write(self.session_key)
        data = stream

        if self.server.kerberos_ticket_version == 1:
            ticket_key = os.urandom(16)
            hash_key = hashlib.md5(key + ticket_key).digest()
            encryption = KerberosEncryption(hash_key)
            encrypted = encryption.encrypt(data)
            return ticket_key + encrypted

        encryption = KerberosEncryption(key)
        return encryption.encrypt(data)

    def decrypt(self, stream: 'ByteStreamIn', key):
        if self.server.kerberos_ticket_version == 1:
            ticket_key = stream.read(16)
            data = stream.read()
            hash_key = hashlib.md5(key + ticket_key).digest()
            key = hash_key

        encryption = KerberosEncryption(key)
        decrypted = encryption.decrypt(stream.read())
        stream = io.BytesIO(decrypted)

        self.issued = DateTime(stream)
        self.source_pid = PID(stream)
        self.session_key = stream.read(self.server.session_key_length)

def new_kerberos_ticket_internal_data(server):
    return KerberosTicketInternalData(server)

def derive_kerberos_key(pid, password):
    iteration_count = 65000 + pid % 1024
    key = password
    for _ in range(iteration_count):
        key = hashlib.md5(key).digest()
    return key