import binascii
import unittest

from kerberos import KerberosEncryption, KerberosTicket, KerberosTicketInternalData, new_kerberos_encryption, new_kerberos_ticket, new_kerberos_ticket_internal_data, derive_kerberos_key
from type.pid import PID


async def test_derive_guest_key(self):
        pid = PID(100)
        password = b"MMQea3n!fsik"
        result = derive_kerberos_key(pid, password)
        self.assertEqual(binascii.hexlify(result).decode(), "9ef318f0a170fb46aab595bf9644f9e1")
        
if __name__ == '__main__': 
    unittest.main()