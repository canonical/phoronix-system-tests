""" SSH wrapper for the worker machine connections.
"""
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
import os

class SSH:
    """ SSH wrapper for the worker machine connections.
    """
    def install():
        key = rsa.generate_private_key(
            backend=crypto_default_backend(), public_exponent=65537, key_size=2048)
        private_key = key.private_bytes(crypto_serialization.Encoding.PEM,
                                        crypto_serialization.PrivateFormat.TraditionalOpenSSL,
                                        crypto_serialization.NoEncryption()
                                        ).decode("utf-8")
        public_key = key.public_key().public_bytes(crypto_serialization.Encoding.OpenSSH,
                                                   crypto_serialization.PublicFormat.OpenSSH
                                                   ).decode("utf-8")
        with open("phoronix-public.key", "w") as file:
            file.write(public_key)

        with open("phoronix-private.key", "w") as file:
            file.write(public_key)

    def execute(ip, script):
        pass
