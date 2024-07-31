"""Test Runner."""

import asyncio
import random
import string

from src.ssh import SSHProvider
from src.suite_splitter import merge_suite, split_suite


class TestProfile:
    """List of hosts in the test profile."""

    hosts: list[str]
    name: str

    def __init__(self, name: str, hosts: list[str]):
        self.hosts = hosts
        self.name = name


class SuiteRunProvider:
    """Runs Phoronix test suite."""

    user: str

    def __init__(self, user, suite_base):
        self.user = user
        self.suite_base = suite_base

    async def run_suite(self, suite: str, profile: TestProfile) -> str:
        """Execute phoronix test suite.

        Args:
            suite (str): _description_
            profile (TestProfile): profiles

        Returns:
            str: _description_
        """
        tasks = []
        slices = split_suite(suite, len(profile.hosts))
        async with asyncio.TaskGroup() as tg:
            for host, suite_slice in zip(profile.hosts, slices):
                ssh_provider = SSHProvider()
                ssh_provider.setup_phoronix_suite(self.user, host, self.suite_base)
                slice_name = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
                ssh_provider.setup_new_suite(self.user, host, slice_name, suite_slice)
                tasks.append(tg.create_task(self.run_suite_slice(slice_name, host)))
        return merge_suite([x.result() for x in tasks])

    async def run_suite_slice(self, suite: str, host: str) -> str:
        """Run part of the test suite."""
        ssh_provider = SSHProvider()
        return ssh_provider.run_suite(self.user, host, suite)
