""" Test openstack provider against live openstack
"""

from openstack_provider import OpenStackProvider
from os import environ


if __name__ == "__main__":  # pragma: nocover
    config = dict()
    config["username"] = environ["OS_USERNAME"]
    config["project_name"] = environ["OS_PROJECT_NAME"]
    config["password"] = environ["OS_PASSWORD"]
    config["auth_url"] = environ["OS_AUTH_URL"]
    config["project_domain_name"] = environ["OS_PROJECT_DOMAIN_NAME"]
    config["region_name"] = environ["OS_REGION_NAME"]
    config["user_domain_name"] = environ["OS_USER_DOMAIN_NAME"]
    config["identify_api_version"] = environ["OS_IDENTITY_API_VERSION"]
    config["interface"] = environ["OS_INTERFACE"]

    provider = OpenStackProvider()
    provider.configure(config)
