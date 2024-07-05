"""OpenStack-based test run orchestrator."""

from os import chmod
from Crypto.PublicKey import RSA

from os import environ
from os.path import expanduser
import openstack

from phoronix_provider import PhoronixProvider


class OpenStackProvider(PhoronixProvider):
    """OpenStack-based test run orchestrator."""

    def install(self):


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



    def provision(self, event):
        """Provision Phoronix workers.

        Args:
            event (_type_): _description_
        """
        profile = event.params['profile']
        flavor = event.params['flavor']
        self.connection.
        pass

    def remove(self, event):
        """Remove Phoronix workers.

        Args:
            event (_type_): _description_
        """
        pass

    def benchmark(self, event):
        """Run benchmark on Phoronix workers.

        Args:
            event (_type_): _description_
        """
        pass
