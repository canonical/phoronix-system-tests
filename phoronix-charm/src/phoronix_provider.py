"""Test run orchestrator interface."""


class PhoronixProvider:
    """Test run orchestrator interface."""

    def install(self, config):
        """Install provider on the machine."""
        pass

    def configure(self, config):
        """Configure provider with the charm config.

        Args:
            config (_type_): _description_
        """
        pass

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
