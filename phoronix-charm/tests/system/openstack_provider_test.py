"""Test openstack provider against live openstack."""

import unittest
from os import environ

from openstack_provider import OpenStackProvider


class OpenStackProviderTest(unittest.TestCase):

    def setUp(self):
        config = {
            "username": environ["OS_USERNAME"],
            "project_name": environ["OS_PROJECT_NAME"],
            "password": environ["OS_PASSWORD"],
            "auth_url": environ["OS_AUTH_URL"],
            "project_domain_name": environ["OS_PROJECT_DOMAIN_NAME"],
            "region_name": environ["OS_REGION_NAME"],
            "user_domain_name": environ["OS_USER_DOMAIN_NAME"],
            "identify_api_version": environ["OS_IDENTITY_API_VERSION"],
            "interface": environ["OS_INTERFACE"],
        }

        self.provider = OpenStackProvider()
        self.provider.configure(config)

    def test_openstack(self):
        servers = self.provider.list_servers()
        print(servers[0])
        self.provider.setup_phoronix_suite(servers[0])
        print("done")


if __name__ == "__main__":
    p = OpenStackProviderTest()
    p.setUp()
    p.test_openstack()
