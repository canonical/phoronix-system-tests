"""OpenStack-based test run orchestrator."""


import openstack

from phoronix_provider import PhoronixProvider
from ssh import PHORONIX_PUBLIC_KEY
from ssh import PHORONIX_PRIVATE_KEY
from ssh import SSHConnection

KEYPAIR_NAME = "local"


class OpenStackProvider(PhoronixProvider):
    """OpenStack-based test run orchestrator."""

    def install(self):
        keypair = self.connection.compute.find_keypair(KEYPAIR_NAME)
        if not keypair:
            keypair = self.connection.compute.create_keypair(name=KEYPAIR_NAME)
            with open(PHORONIX_PUBLIC_KEY, "w") as public_key_file:
                public_key_file.write(keypair.public_key)
            with open(PHORONIX_PRIVATE_KEY, "w") as private_key_file:
                private_key_file.write(keypair.private_key)
#       try:
        self.connection.create_security_group_rule(
            "allow_ssh", protocol="tcp", port_range_min=22, port_range_max=22)
#       except Err:

    def configure(self, config):
        """Configure provider with the charm config.

        Args:
            config (_type_): _description_
        """
        self.connection = openstack.connect(
            auth_url=config['auth_url'],
            project_name=config['project_name'],
            username=config['username'],
            password=config['password'],
            region_name=config['region_name'],
            user_domain_name=config['user_domain_name'],
            project_domain_name=config['project_domain_name'],
            app_name='phoronix',
            app_version='1.0')
        self._servers = self.connection.list_servers()

    def provision(self, event):
        """Provision Phoronix workers.

        Args:
            event (_type_): _description_
        """
        name = event.params['profile']
        image = event.params['image']
        flavor = event.params['flavor']

        server = self.connection.create_server(
            name, image=image, flavor=flavor)
        self.connection.wait_for_server(server)
        self._servers.append(server)
        pass

    def remove(self, event):
        """Remove Phoronix workers.

        Args:
            event (_type_): _description_
        """
        for server in self._servers:
            self.connection.delete_server(server, force=True)
        pass

    def benchmark(self, event):
        """Run benchmark on Phoronix workers.

        Args:
            event (_type_): _description_
        """
        # connect to servers
        # submit jobs
        # wait for completion
        # return results

        pass
