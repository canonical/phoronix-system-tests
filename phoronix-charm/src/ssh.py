""" SSH wrapper for the worker machine connections.
"""
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
import os
from fabric import Connection

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

    descriptor = os.open(
        path="phoronix-private.key",
        flags=(
            os.O_WRONLY  # access mode: write only
            | os.O_CREAT  # create if not exists
            | os.O_TRUNC  # truncate the file to zero
        ),
        mode=0o600
    )

    with open(descriptor, "w") as file:
        file.write(private_key)

class SSHConnection:
    def __init__(self, user:str, host:str):
        self._user = user
        self._host = host
        with open("phoronix-public.key") as file:
            self.public = file.read()
        with open("phoronix-private.key") as file:
            self.private = file.read()

    def __enter__(self):
        self.connection = Connection(host = self._host, user= self._user, connect_kwargs={
            "key_filename" : "phoronix-private.key",
            "look_for_keys": "false"
        })
        return self.connection

    def __exit__(self, *args):
        self.connection.close()

if __name__ == "__main__":  # pragma: nocover
    install()
