"""Publish routing changes only after every backend and certificate is ready."""
from copy import deepcopy
from pathlib import Path
import time

from sharpnet.constants import SITE_CONF


def run_cycle(network):
    if time.monotonic() < getattr(network, "next_retry_at", 0):
        network.force = True
        return
    config = Path(SITE_CONF)
    previous = config.read_text(encoding="utf-8") if config.exists() else ""
    previous_cache = deepcopy(network.cache)
    certificate_attempted = False
    try:
        network.load_containers()
        if network.problem_container or network.error:
            raise RuntimeError("A backend is not ready")
        if network.containers_loaded:
            certificate_attempted = True
            if not network.run_certbot():
                raise RuntimeError("Certificate configuration failed")
        network.run_nginx()
        if network.error:
            raise RuntimeError("Nginx reload failed")
    except Exception as error:
        config.write_text(previous, encoding="utf-8")
        network.cache = previous_cache
        network.problem_container = None
        network.error = None
        network.force = True
        network.next_retry_at = time.monotonic() + 30
        if previous and certificate_attempted:
            # The Nginx Certbot plugin may already have reloaded its candidate.
            try:
                network.run_nginx()
            except Exception as restore_error:
                print(f"Previous configuration reload failed: {restore_error}")
            network.error = None
        print(f"Keeping the last working configuration; retrying: {error}")
        return
    print("** SHARPNET ACTIVE **")


def load(network):
    """Retain the public method while using the same transactional cycle."""
    run_cycle(network)
