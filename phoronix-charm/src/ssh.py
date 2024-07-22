"""SSH wrapper for the worker machine connections."""

import os
from typing import Any
import tempfile
from invoke.exceptions import UnexpectedExit
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fabric import Config, Connection
from subprocess import run
from os import path

PHORONIX_PUBLIC_KEY = "phoronix-public.key"

PHORONIX_PRIVATE_KEY = "phoronix-private.key"


def install():
    """Generate ssh keys."""
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


class SSHProvider:
    """Setup Phoronix suite over ssh."""

    def execute(self, user, ip, command, **kwargs):
        with SSHConnection(user, ip) as ssh:
            ssh.execute(command, **kwargs)

    def setup_ubuntu_sources(self, user: str, ip:str, sources: str):
        with SSHConnection(user, ip) as ssh:
            with tempfile.NamedTemporaryFile(delete=True) as tmp:
                tmp.write(str.encode(sources))
                ssh.put(tmp.name, "/home/ubuntu/ubuntu.sources")
                ssh.execute("rm -f /etc/apt/sources.list")
                ssh.execute("rm -rf /etc/apt/sources.list.d/*")
                ssh.execute("cp /home/ubuntu/ubuntu.sources /etc/apt/sources.list.d/")
                ssh.execute("apt update")

    def run_suite(self, user: str, ip: str, suite_name:str) -> str:
        with SSHConnection(user, ip) as ssh:
            ssh.execute(f"/bin/sh /home/ubuntu/pts/run.sh {suite_name}")
            with tempfile.NamedTemporaryFile(delete=True) as tmp:
                ssh.get(f"/home/{user}/.phoronix-test-suite/test-results/{suite_name}/composite.xml", tmp.name)
                with open(tmp.name, "r") as input:
                    return input.read()

    def setup_new_suite(self, user: str, ip: str, suite_name:str, suite_text: str):
        with SSHConnection(user, ip) as ssh:
            with tempfile.NamedTemporaryFile(delete=True) as tmp:
                    tmp.write(str.encode(suite_text))
                    ssh.execute(f"mkdir -p /home/{user}/.phoronix-test-suite/test-results/test-suites/local/{suite_name}/")
                    ssh.put(tmp.name, f"/home/{user}/.phoronix-test-suite/test-suites/local/{suite_name}/suite-definition.xml")

    def setup_phoronix_suite(self, user: str, ip:str, suite_base:str ) -> bool:
        try:
            with SSHConnection(user, ip) as ssh:
                # transfer all files from local to the remote phoronix directory
                with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=True) as tmp:
                    run(["tar", "zcvf", tmp.name, "."], check=True, cwd=suite_base)
                    ssh.put(tmp.name, "/home/ubuntu")
                    ssh.execute("mkdir -p /home/ubuntu/pts")
                    ssh.execute(
                        f"tar xvf /home/ubuntu/{path.basename(tmp.name)} -C /home/ubuntu/pts"
                    )

                # run install script
                ssh.execute("sh /home/ubuntu/pts/install.sh", sudo=True)
            return True
        except UnexpectedExit as err:
            print(err)
            return False



class SSHConnection:
    """Wraps Fabric connection object."""

    def __init__(self, user: str, host: str):
        """Init class.

        Args:
            user (str): username
            host (str): hostname
        """
        self._user = user
        self._host = host

    def __enter__(self):
        """Create Fabric connection object."""
        config = Config(overrides={"sudo": {"password": "ubuntu"}})
        self.connection = Connection(
            host=self._host,
            user=self._user,
            config=config,
            connect_kwargs={"key_filename": PHORONIX_PRIVATE_KEY, "look_for_keys": "false"},
        )
        return self

    def __exit__(self, *args):
        """Close Fabric connection."""
        self.connection.close()

    def execute(self, command: str, **kwargs: Any):
        """Execute command.

        Args:
            command (str): command to execute
            **kwargs: sudo: True/False, other kv args to Connection.run()
        """
        if "sudo" in kwargs and kwargs["sudo"]:
            del kwargs["sudo"]
            return self.connection.sudo(command, **kwargs)
        return self.connection.run(command, **kwargs)

    def get(self, remote_file: str, local_file: str):
        """Retrieve remote file."""
        self.connection.get(remote_file, local_file)

    def put(self, local_file: str, remote_file: str):
        """Put file to remote."""
        self.connection.put(local_file, remote_file)

    def put_dir(self, local_dir: str, remote_dir: str):
        """Put directory to remote."""
        self.execute(f"mkdir -p {remote_dir}")
        for root, dirs, files in os.walk(local_dir):
            for file in files:
                self.put(os.path.join(root, file), os.path.join(remote_dir, file))
            for dir in dirs:
                self.put_dir(os.path.join(root, dir), os.path.join(remote_dir, dir))
