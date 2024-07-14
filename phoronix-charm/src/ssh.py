""" SSH wrapper for the worker machine connections.
"""
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
import os

from fabric import Connection
from typing import Any

PHORONIX_PUBLIC_KEY = "phoronix-public.key"

PHORONIX_PRIVATE_KEY = "phoronix-private.key"


def install():
    if os.path.isfile(PHORONIX_PUBLIC_KEY) and os.path.isfile(PHORONIX_PRIVATE_KEY):
        return

    key = rsa.generate_private_key(
        backend=crypto_default_backend(), public_exponent=65537, key_size=2048)
    private_key = key.private_bytes(crypto_serialization.Encoding.PEM,
                                    crypto_serialization.PrivateFormat.TraditionalOpenSSL,
                                    crypto_serialization.NoEncryption()
                                    ).decode("utf-8")
    public_key = key.public_key().public_bytes(crypto_serialization.Encoding.OpenSSH,
                                               crypto_serialization.PublicFormat.OpenSSH
                                               ).decode("utf-8")
    with open(PHORONIX_PUBLIC_KEY, "w") as file:
        file.write(public_key)

    descriptor = os.open(
        path=PHORONIX_PRIVATE_KEY,
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
    def __init__(self, user: str, host: str):
        self._user = user
        self._host = host

    def __enter__(self):
        self.connection = Connection(host=self._host, user=self._user, connect_kwargs={
            "key_filename": PHORONIX_PRIVATE_KEY,
            "look_for_keys": "false"
        })
        return self

    def __exit__(self, *args):
        self.connection.close()

    def execute(self, command: str, **kwargs: Any):
        return self.connection.run(command, kwargs)

    def get(self, remote_file: str, local_file: str):
        self.connection.get(remote_file, local_file)

    def put(self, local_file: str, remote_file: str):
        self.connection.put(local_file, remote_file)


if __name__ == "__main__":  # pragma: nocover
    install()
