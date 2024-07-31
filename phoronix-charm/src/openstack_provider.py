"""OpenStack-based test run orchestrator."""

import logging
from os import environ, path

import openstack
from provisioning_provider import ProvisioningProvider
from ssh import PHORONIX_PRIVATE_KEY, PHORONIX_PUBLIC_KEY, SSHProvider

KEYPAIR_NAME = "local"
DEFAULT_USER = "ubuntu"
PHORONIX_BASE = "PHORONIX_BASE"

PROFILE = "profile"
IMAGE = "image"
FLAVOR = "flavor"
SOURCES = "sources"
KEY_NAME = "key_name"
PROXY = "proxy"

logger = logging.getLogger(__name__)


class OpenStackProvider(ProvisioningProvider):
    """OpenStack-based test run orchestrator."""

    ssh_provider: SSHProvider

    def __init__(self):
        self.ssh_provider = SSHProvider()

    def __get_addr(self, server_name):
        servers = [x for x in self.connection.list_servers() if x.name == server_name]  # type: ignore
        if len(servers) == 0:
            raise RuntimeError(server_name + " not found")
        key = next(iter(servers[0].addresses.keys()))# type: ignore
        return servers[0].addresses[key][0]["addr"]  # type: ignore

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

    def provision(self, config):
        """Provision Phoronix workers.

        Args:
            config (dict): server configuration
            profile-name:
                image: <image-name-or-id>
                flavor: <flavor>
                proxy: url
                sources: |
                    Types: deb deb-src
                    URIs: http://archive.ubuntu.com/ubuntu/
                    Suites: noble
                    Components: main universe restricted multiverse
        """
        name = config["profile"]
        image = config["image"]
        flavor = config["flavor"]
        sources = config["sources"]
        key_name = config["key_name"]
        proxy = config["proxy"]
        logger.info(f"Creating server {name}")
        # check that the server is provisioned.
        # if not, try to create it
        # edge case/not supported: server exists but the ip is not assigned
        try:
            _ = self.__get_addr(name)
        except:
            try:
                server = self.connection.create_server(name, image=image, flavor=flavor, key_name=key_name)
                self.connection.wait_for_server(server)
            except:
                print(f"Server result {server}")
        logger.info(f"Server {name} is active")
        self.set_proxy_environment(name, proxy)
        logger.info(f"Set ubuntu sources for  {name}")
        self.replace_ubuntu_sources(name, sources)
        logger.info(f"Setup Phoronix suite on {name}")
        return self.setup_phoronix_suite(name)

    def set_proxy_environment(self, server_name, proxy):
        """Add proxy url to .bashrc.

        Args:
            server_name (str): server ip
            proxy (str): proxy url
        """
        ip = self.__get_addr(server_name)
        self.ssh_provider.execute(DEFAULT_USER, ip, f"echo export https_proxy={proxy} >> ~/.bashrc" )
        self.ssh_provider.execute(DEFAULT_USER, ip, f"echo export http_proxy={proxy} >> ~/.bashrc" )

    def replace_ubuntu_sources(self, server_name, sources):
        """Write ubuntu.sources to the target server.

        Args:
            server_name (str): name of the target server
            sources (str): content of ubuntu.sources
        """
        ip = self.__get_addr(server_name)
        self.ssh_provider.setup_ubuntu_sources(DEFAULT_USER, ip, sources)

    def setup_phoronix_suite(self, server_name):
        """Set up Phoronix test suite on the specified server.

        Args:
            server_name (_type_): openstack server name
        """
        ip = self.__get_addr(server_name)
        suite_base = path.abspath(environ[PHORONIX_BASE])
        return self.ssh_provider.setup_phoronix_suite(DEFAULT_USER, ip, suite_base)

    def remove(self, event):
        """Remove Phoronix workers.

        Args:
            event (_type_): _description_
        """
        servers = self.connection.list_servers()
        for server in servers:
            self.connection.delete_server(server, wait=True)
        pass

    def list_servers(self):
        """Return openstack server names."""
        return self.connection.list_servers()

    def execute(self, server_name, command, **kwargs):
        """Execute command on the specified server.

        Args:
            server_name: name of the openstack server
            command: command to execute
            **kwargs: args
        """
        ip = self.__get_addr(server_name)
        self.ssh_provider.execute(DEFAULT_USER, ip, command, **kwargs)
