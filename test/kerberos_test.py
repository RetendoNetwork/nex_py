from kerberos import KerberosEncryption, KeyDerivationNew, KeyDerivationOld
from type.pid import PID


async def TestDeriveGuestKey():
	pid = PID(100)
	password = bytes("MMQea3n!fsik")
	result = KeyDerivationNew.derive_key(pid, password)
	# assert.Equal(t, "9ef318f0a170fb46aab595bf9644f9e1", hex.EncodeToString(result))
