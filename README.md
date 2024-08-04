# phoronix-system-tests

This repository contains scripts to run image benchmarking using Phoronix test suite on Openstack cloud.

# Build and install

```
git submodule init
gi submodule update
(cd phoronix-charm/ && python3 -m build)
```

Create orchestrator machine, e.g. using `foundations-bastion-ps6`. 

```
$ssh foundations-bastion-ps6.internal
foundations-bastion-ps6$ sudo -iu stg-ubuntu-benchmark-testing-machine-model se stg-ubuntu-benchmark-testing-machine-model
foundations-bastion-ps6$ openstack security group rule create --protocol tcp --dst-port 22 default
foundations-bastion-ps6$ openstack keypair create local --public-key ~/.ssh/id_ed25519.pub
foundations-bastion-ps6$ openstack server create --key-name local --flavor staging-cpu1-ram4-disk20 --image 'auto-sync/ubuntu-noble-24.04-amd64-server-20240725-disk1.img' orchestrator
```

Copy the repository tree to the orchestrator machine.

Install scripts on the orchestrator machine:

```
$ apt install python3-venv
$ python -m venv runner
$ source ./runner/bin/activate
$ https_proxy=squid.ps6.internal:3128 pip install phoronix-system-tests/phoronix-charm/dist/phoronix_system_test-0.0.1-py3-none-any.whl
```

# Provisioning

On orchestrator machine

```
$ source ~/runner/bin/activate
$ <export variables with your openstack credentials>
$ python3 -m deploy -b ~/phoronix-system-tests noble-o3.yaml
```

This will create the test runner machine from the yaml config, copy the repository to the runner machine and install phoronix tests.

# Running tests. 


On orchestrator machine

```
$ source ~/runner/bin/activate
$ <export variables with your openstack credentials>
$ python3 -m run_suite -b ~/phoronix-system-tests -s -b ~/phoronix-system-tests/alltests/suite-definition.xml test-noble-o3.yaml

```

This runs a test suite defined in `~/phoronix-system-tests/alltests/suite-definition.xml` using yaml config `test-noble-o3.yaml`. 
The config lists test images, e.g. noble-o3 image, or baseline noble image, with the list of test runners configured with this image. 
The test suite it split between test runners with the same image and executed.The results are stored in `./<test-image>/composite.xml`, e.g. `./noble-o3/composite.xml`. 

# Viewing test results

Copy results into `~/.phoronix-test-suite/test-results` and use phoronix test suite, e.g. `phoronix-test-suite show-result noble-o3` to view it. 


# Notes

The Phoronix test suite configured as a submodule contains a [patch](https://github.com/phoronix-test-suite/phoronix-test-suite/commit/a1c0cc826bfc98fbc544abd7144dad7719952ef3) to automatically enable the batch mode when it is configured to avoid command line prompts when running tests.

# Further work

- Charm the orchestrator so that it can be deployed using the terraform profile. 
- Automate test runner discovery by querying the deployed image.
- Configure CI

