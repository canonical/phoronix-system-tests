"""OpenStack-based test run orchestrator."""

import tempfile
from os import environ, path
from subprocess import run

import openstack
from invoke.exceptions import UnexpectedExit
from openstack.compute.v2.server import Server
from phoronix_provider import PhoronixProvider
from ssh import PHORONIX_PRIVATE_KEY, PHORONIX_PUBLIC_KEY, SSHConnection

KEYPAIR_NAME = "local"
DEFAULT_USER = "ubuntu"
PHORONIX_BASE = "PHORONIX_BASE"


class OpenStackProvider(PhoronixProvider):
    """OpenStack-based test run orchestrator."""

    _servers: list[Server]

    def __get_addr(self, server_name):
        servers = [x for x in self._servers if x.name == server_name]
        if len(servers) == 0:
            raise RuntimeError(server_name + " not found")
        return servers[0].addresses["net_instances"][0]["addr"]  # type: ignore

    def install(self, config):
        """Create openstack keypair and security rules."""
        keypair = self.connection.compute.find_keypair(KEYPAIR_NAME)
        if not keypair:
            keypair = self.connection.compute.create_keypair(name=KEYPAIR_NAME)
            with open(PHORONIX_PUBLIC_KEY, "w") as public_key_file:
                public_key_file.write(str(keypair.public_key))
            with open(PHORONIX_PRIVATE_KEY, "w") as private_key_file:
                private_key_file.write(str(keypair.private_key))
        #       try:
        self.connection.create_security_group_rule(
            "allow_ssh", protocol="tcp", port_range_min=22, port_range_max=22
        )

    #       except Err:

    def configure(self, config):
        """Configure provider with the charm config.

        Args:
            config (_type_): _description_
        """
        self.connection = openstack.connect(
            auth_url=config["auth_url"],
            project_name=config["project_name"],
            username=config["username"],
            password=config["password"],
            region_name=config["region_name"],
            user_domain_name=config["user_domain_name"],
            project_domain_name=config["project_domain_name"],
            app_name="phoronix",
            app_version="1.0",
        )
        self._servers = self.connection.list_servers()  # type: ignore

    def provision(self, event):
        """Provision Phoronix workers.

        Args:
            event (_type_): _description_
        """
        name = event.params["profile"]
        image = event.params["image"]
        flavor = event.params["flavor"]

        server = self.connection.create_server(name, image=image, flavor=flavor)
        self.connection.wait_for_server(server)
        self._servers.append(server)

    def setup_phoronix_suite(self, server_name):
        """Set up Phoronix test suite on the specified server.

        Args:
            server_name (_type_): openstack server name
        """
        ip = self.__get_addr(server_name)

        suite_base = path.abspath(environ[PHORONIX_BASE])
        try:
            with SSHConnection(DEFAULT_USER, ip) as ssh:
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

    def remove(self, event):
        """Remove Phoronix workers.

        Args:
            event (_type_): _description_
        """
        for server in self._servers:
            self.connection.delete_server(server, wait=True)
        pass

    def list_servers(self):
        """Return openstack server names."""
        return [x.name for x in self._servers]

    def execute(self, server_name, command, **kwargs):
        """Execute command on the specified server.

        Args:
            server_name: name of the openstack server
            command: command to execute
            **kwargs: args
        """
        ip = self.__get_addr(server_name)
        with SSHConnection(DEFAULT_USER, ip) as ssh:
            ssh.execute(command, **kwargs)

    def benchmark(self, event):
        """Run benchmark on Phoronix workers.

        Args:
            event (_type_): _description_
        """
        for server in self._servers:
            print(server)
        # connect to servers
        # submit jobs
        # wait for completion
        # return results

        pass
