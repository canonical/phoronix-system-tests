"""Test Runner."""

import asyncio

from src.suite_splitter import split_suite
from src.suite_splitter import merge_suite

class TestProfile:
    """List of hosts in the test profile"""

    hosts: list[str]


class SuiteRunProvider:
    async def run_suite(self, suite: str, profile: TestProfile) -> str:
        """Execute phoronix test suite.

        Args:
            suite (str): _description_

        Returns:
            str: _description_
        """
        tasks = []
        slices = split_suite(suite, len(profile.hosts))
        async with asyncio.TaskGroup() as tg:
            for host, suite_slice in zip(profile.hosts, slices):
                tasks.append(tg.create_task(self.run_suite_slice(suite_slice, host)))
        return merge_suite([x.result() for x in tasks])

    async def run_suite_slice(self, suite: str, host: str) -> str:
        pass
