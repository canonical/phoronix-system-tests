"""OpenStack-based test run orchestrator."""

from phoronix_provider import PhoronixProvider


class OpenStackProvider(PhoronixProvider):
    """OpenStack-based test run orchestrator."""

    def provision(self, event):
        """Provision Phoronix workers.

        Args:
            event (_type_): _description_
        """
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
