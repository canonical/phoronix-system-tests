#!/usr/bin/env python3
# Copyright 2024 Vladimir Petko
# See LICENSE file for licensing details.

"""Charm the application."""

import logging

import ops
from openstack_provider import OpenStackProvider
from phoronix_provider import PhoronixProvider

logger = logging.getLogger(__name__)


class PhoronixCharmCharm(ops.CharmBase):
    """Charm the application."""

    provider: PhoronixProvider

    def __init__(self, framework: ops.Framework):
        super().__init__(framework)
        # Events
        event_bindings = {
            self.on.install: self._on_install,
            self.on.config_changed: self._on_config_changed,
            self.on.start: self._on_start,
            self.on.stop: self._on_stop,
        }
        # Actions
        action_bindings = {
            self.on.provision_action: self._on_provision_action,
            self.on.remove_action: self._on_remove_action,
            self.on.benchmark_action: self._on_benchmark_action,
        }
        # Observe events and actions
        for event, handler in event_bindings.items():
            self.framework.observe(event, handler)

        for action, handler in action_bindings.items():
            self.framework.observe(action, handler)

        self.provider = OpenStackProvider()

    def _on_provision_action(self, event):
        pass

    def _on_remove_action(self, event):
        pass

    def _on_benchmark_action(self, event):
        pass

    def _on_install(self, event: ops.InstallEvent):
        self.provider.configure(self.config)
        self.provider.install()

    def _on_config_changed(self, _):
        self.provider.configure(self.config)

    def _on_start(self, event: ops.StartEvent):
        """Handle start event."""
        self.unit.status = ops.ActiveStatus()

    def _on_stop(self, event: ops.StopEvent):
        """Handle stop event."""
        self.unit.status = ops.BlockedStatus("Stopped.")


if __name__ == "__main__":  # pragma: nocover
    ops.main(PhoronixCharmCharm)  # type: ignore
