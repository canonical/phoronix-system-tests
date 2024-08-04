"""Provisioning interface."""


class ProvisioningProvider:
    """Provisioning interface."""

    def install(self, config):
        """Install provider on the machine."""
        pass

    def configure(self, config):
        """Configure provider with the charm config.

        Args:
            config (_type_): _description_
        """
        pass

    def provision(self, config) -> bool:
        """Provision Phoronix workers.

        Args:
            config (_type_): _description_
        """
        return False

    def remove(self, event):
        """Remove Phoronix workers.

        Args:
            event (_type_): _description_
        """
        pass
