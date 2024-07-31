#!/usr/bin/python3
"""Manually deploy an openstack server using yaml configuration.

profile-name:
    image: <image-name-or-id>
    flavor: <flavor>
    sources: |
        Types: deb deb-src
        URIs: http://archive.ubuntu.com/ubuntu/
        Suites: noble
        Components: main universe restricted multiverse
"""

import argparse
import os
from os import environ

import openstack_provider
import yaml


def get_server_config():
    """Generate server configuration for deployment.

    Returns:
        list(dict): list of dicts with server configuration
    """
    parser = argparse.ArgumentParser(
        prog="deploy", description="Deploy openstack server and install phoronix suite"
    )

    parser.add_argument("-b", "--base", help="Path to phoronix-system-test root")
    parser.add_argument("config", help="yaml configuration of the server")
    args = parser.parse_args()

    os.environ[openstack_provider.PHORONIX_BASE] = args.base
    ret = []
    with open(args.config, "r") as input:
        config = yaml.safe_load(input)
        for key in config.keys():
            value = config[key]
            server = {
                openstack_provider.PROFILE: key,
                openstack_provider.IMAGE: value[openstack_provider.IMAGE],
                openstack_provider.FLAVOR: value[openstack_provider.FLAVOR],
                openstack_provider.SOURCES: value[openstack_provider.SOURCES],
                openstack_provider.KEY_NAME: value[openstack_provider.KEY_NAME],
                openstack_provider.PROXY: value[openstack_provider.PROXY],
            }
            ret.append(server)
    return ret


if __name__ == "__main__":
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

    provider = openstack_provider.OpenStackProvider()
    provider.configure(config)
    for server in get_server_config():
        provider.provision(server)
