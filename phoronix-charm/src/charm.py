#!/usr/bin/env python3
# Copyright 2024 Vladimir Petko
# See LICENSE file for licensing details.

"""Charm the application."""

import logging

import ops

logger = logging.getLogger(__name__)


class PhoronixCharmCharm(ops.CharmBase):
    """Charm the application."""

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
            self.on.provision: self._on_provision_action,
            self.on.remove: self._on_remove_action,
            self.on.benchmark: self._on_benchmark_action
        }

    def _on_provision_action(self, event):
        pass

    def _on_remove_action(self, event):
        pass

    def _on_benchmark_action(self, event):
        pass

    def _on_install(self, event: ops.InstallEvent):
        pass

    def _on_start(self, event: ops.StartEvent):
        """Handle start event."""
        self.unit.status = ops.ActiveStatus()

    def _on_stop(self, event: ops.StopEvent):
        """Handle stop event."""
        self.unit.status = ops.BlockedStatus("Stopped.")


if __name__ == "__main__":  # pragma: nocover
    ops.main(PhoronixCharmCharm)  # type: ignore
