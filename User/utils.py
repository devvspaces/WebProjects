from cryptography.fernet import Fernet
#Getting a key
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat import primitives
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

def create_user_key(instance):
	password=instance.user.password
	encode=password.encode()

	salt=os.urandom(16)

	obj=PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=salt,
		iterations=10000,
		backend=default_backend()
	)

	key=base64.urlsafe_b64encode(obj.derive(encode))
	return key.decode()

def crypt(key, message='', encrypted=''):
	key = key.encode()
	fernet=Fernet(key)
	if message:
		message = message.encode()
		enc=fernet.encrypt(message)
		return enc.decode()
	else:
		dec=fernet.decrypt(encrypted.encode()).decode()
		return dec
def get_key(key):
	return os.environ.get(key)