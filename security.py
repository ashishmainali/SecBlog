

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


from Crypto.Cipher import AES
import base64, os

def generate_public_private_key(size=2048):
    # generate private/public key pair
    key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, \
        key_size=size)

    # get public key in OpenSSH format
    public_key = key.public_key().public_bytes(serialization.Encoding.OpenSSH, \
        serialization.PublicFormat.OpenSSH)

    # get private key in PEM container format
    pem = key.private_bytes(encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption())

    # decode to printable strings
    private_key_str = pem.decode('utf-8')
    public_key_str = public_key.decode('utf-8')
    key = {'public':public_key_str,'private':private_key_str}
    return key


def generate_secret_key_for_AES_cipher(AES_key_length = 64):
    # AES key length must be either 16, 24, or 32 bytes long
     # use larger value in production
    # generate a random secret key with the decided key length
    # this secret key will be used to create AES cipher for encryption/decryption
    secret_key = os.urandom(AES_key_length)
    # encode this secret key for storing safely in database
    encoded_secret_key = base64.b64encode(secret_key)
    return encoded_secret_key.decode()
