#!/usr/bin/python3
"""Run phoronix suite.

test-profile1:
    - ip1
    - ip2
    - ip3
test-profile2:
    - ip1
    - ip2
    - ip3
"""
import argparse
from subprocess import run

import yaml
from suite_run_provider import SuiteRunProvider, TestProfile


def run_test_suite():
    """Run Phoronix test suite using yaml configuration."""
    parser = argparse.ArgumentParser(
        prog="deploy", description="Deploy openstack server and install phoronix suite"
    )

    parser.add_argument("-s", "--suite", help="Path to the test suite")
    parser.add_argument("-b", "--base", help="Path to phoronix-system-test root")
    parser.add_argument("config", help="yaml configuration of the server")
    args = parser.parse_args()

    base = args.base

    with open(args.suite, "r") as suite_file:
        suite_text = suite_file.read()

    with open(args.config, "r") as input:
        config = yaml.safe_load(input)
        profiles = []
        for key in config["profiles"].keys():
            profiles.append(TestProfile(name=key, hosts=config["profiles"][key]))
        runner = SuiteRunProvider(config["user"], base)
        for profile in profiles:
            profile_result = runner.run_suite(profile.name, suite_text, profile)
            run(f"mkdir -p {profile.name}")
            with open(f"{profile.name}/composite.xml", "w") as result_file:
                result_file.write(profile_result)


if __name__ == "__main__":
    run_test_suite()
