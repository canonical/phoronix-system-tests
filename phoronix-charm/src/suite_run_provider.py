"""Test Runner."""

import random
import string
from multiprocessing import Pool

from ssh import SSHProvider
from suite_splitter import merge_suite, split_suite


class TestProfile:
    """List of hosts in the test profile."""

    hosts: list[str]
    name: str

    def __init__(self, name: str, hosts: list[str]):
        self.hosts = hosts
        self.name = name

class WorkItem:
    host: str
    slice_text: str

    def __init__(self, host:str, slice_text:str):
        self.host = host
        self.slice_text = slice_text

class SuiteRunProvider:
    """Runs Phoronix test suite."""

    user: str

    def __init__(self, user, suite_base):
        self.user = user
        self.suite_base = suite_base

    def run_suite(self, suite: str, profile: TestProfile) -> str:
        """Execute phoronix test suite.

        Args:
            suite (str): _description_
            profile (TestProfile): profiles

        Returns:
            str: _description_
        """
        slices = split_suite(suite, len(profile.hosts))

        result = []

        mapping = [WorkItem(host,slice) for host,slice in zip(profile.hosts, slices)]
        with Pool(len(slices)) as pool:
            result = pool.map(self.worker, mapping)
        return merge_suite(result)

    def worker(self, item: WorkItem):
        """Worker for the suite execution.

        Args:
            item (WorkItem): work item to process
        """
        slice_name = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
        self.setup_new_suite(item.host, slice_name, item.slice_text)
        return self.run_suite_slice(slice_name, item.host)

    def setup_new_suite(self, host: str, slice_name: str, suite_slice: str):
        """Setup phoronix suite on a remote machine.

        Args:
            host (str): remote host
            slice_name (str): name of the suite
            suite_slice (str): suite contents
        """
        ssh_provider = SSHProvider()
        ssh_provider.setup_new_suite(self.user, host, slice_name, suite_slice)

    def run_suite_slice(self, suite: str, host: str) -> str:
        """Run part of the test suite."""
        ssh_provider = SSHProvider()
        return ssh_provider.run_suite(self.user, host, suite)
