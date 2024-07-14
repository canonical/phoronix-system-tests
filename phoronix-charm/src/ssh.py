"""SSH wrapper for the worker machine connections.
"""

import os
from typing import Any

from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fabric import Config, Connection

PHORONIX_PUBLIC_KEY = "phoronix-public.key"

PHORONIX_PRIVATE_KEY = "phoronix-private.key"


def install():
    if os.path.isfile(PHORONIX_PUBLIC_KEY) and os.path.isfile(PHORONIX_PRIVATE_KEY):
        return

    key = rsa.generate_private_key(
        backend=crypto_default_backend(), public_exponent=65537, key_size=2048
    )
    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.TraditionalOpenSSL,
        crypto_serialization.NoEncryption(),
    ).decode("utf-8")
    public_key = (
        key.public_key()
        .public_bytes(
            crypto_serialization.Encoding.OpenSSH, crypto_serialization.PublicFormat.OpenSSH
        )
        .decode("utf-8")
    )
    with open(PHORONIX_PUBLIC_KEY, "w") as file:
        file.write(public_key)

    descriptor = os.open(
        path=PHORONIX_PRIVATE_KEY,
        flags=(
            os.O_WRONLY  # access mode: write only
            | os.O_CREAT  # create if not exists
            | os.O_TRUNC  # truncate the file to zero
        ),
        mode=0o600,
    )

    with open(descriptor, "w") as file:
        file.write(private_key)


class SSHConnection:
    def __init__(self, user: str, host: str):
        self._user = user
        self._host = host

    def __enter__(self):
        config = Config(overrides={"sudo": {"password": "ubuntu"}})
        self.connection = Connection(
            host=self._host,
            user=self._user,
            config=config,
            connect_kwargs={"key_filename": PHORONIX_PRIVATE_KEY, "look_for_keys": "false"},
        )
        return self

    def __exit__(self, *args):
        self.connection.close()

    def execute(self, command: str, **kwargs: Any):
        if "sudo" in kwargs and kwargs["sudo"]:
            del kwargs["sudo"]
            return self.connection.sudo(command, **kwargs)
        return self.connection.run(command, **kwargs)

    def get(self, remote_file: str, local_file: str):
        self.connection.get(remote_file, local_file)

    def put(self, local_file: str, remote_file: str):
        print(f"copy {local_file} to {remote_file}")
        self.connection.put(local_file, remote_file)

    def put_dir(self, local_dir: str, remote_dir: str):
        self.execute(f"mkdir -p {remote_dir}")
        for root, dirs, files in os.walk(local_dir):
            for file in files:
                self.put(os.path.join(root, file), os.path.join(remote_dir, file))
            for dir in dirs:
                self.put_dir(os.path.join(root, dir), os.path.join(remote_dir, dir))


if __name__ == "__main__":  # pragma: nocover
    install()
