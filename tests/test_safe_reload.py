import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

for key in ("SENDER_EMAIL", "RECEIVER_EMAIL", "DOMAIN"):
    os.environ.setdefault(key, "example.invalid")

from sharpnet.tasks import network as controller
from sharpnet.tasks import nginx


class FakeNetwork:
    def __init__(self, path, failure=None):
        self.path = path
        self.failure = failure
        self.cache = {"working": "original"}
        self.problem_container = None
        self.error = None
        self.force = False
        self.containers_loaded = ["backend"]
        self.reloads = []
        self.certificate_calls = 0

    def load_containers(self):
        self.path.write_text("candidate HTTP")
        self.cache = {"new": "candidate"}
        if self.failure == "backend":
            self.problem_container = "temporarily stopped backend"
        if self.failure == "exception":
            raise OSError("Docker temporarily unavailable")

    def run_certbot(self):
        self.certificate_calls += 1
        self.path.write_text("candidate HTTPS")
        return self.failure != "certificate"

    def run_nginx(self):
        self.reloads.append(self.path.read_text())
        if self.failure == "reload" and self.path.read_text() != "working HTTPS":
            self.error = "reload failed"

    def kill(self, *args):
        raise AssertionError("The controller must never stop a backend")


class SafeReloadTests(unittest.TestCase):
    def run_case(self, failure):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        path = Path(temporary.name) / "site.conf"
        path.write_text("working HTTPS")
        network = FakeNetwork(path, failure)
        with patch.object(controller, "SITE_CONF", str(path)):
            controller.run_cycle(network)
        return path, network

    def test_temporary_backend_failure_keeps_https_and_skips_certbot(self):
        path, network = self.run_case("backend")
        self.assertEqual(path.read_text(), "working HTTPS")
        self.assertEqual(network.certificate_calls, 0)
        self.assertEqual(network.reloads, [])
        self.assertEqual(network.cache, {"working": "original"})
        self.assertTrue(network.force)

    def test_docker_error_preserves_https(self):
        path, network = self.run_case("exception")
        self.assertEqual(path.read_text(), "working HTTPS")
        self.assertTrue(network.force)

    def test_certificate_failure_restores_and_reloads_https(self):
        path, network = self.run_case("certificate")
        self.assertEqual(path.read_text(), "working HTTPS")
        self.assertEqual(network.reloads, ["working HTTPS"])

    def test_reload_failure_restores_previous_configuration(self):
        path, network = self.run_case("reload")
        self.assertEqual(path.read_text(), "working HTTPS")
        self.assertEqual(network.reloads, ["candidate HTTPS", "working HTTPS"])

    def test_success_publishes_https(self):
        path, network = self.run_case(None)
        self.assertEqual(path.read_text(), "candidate HTTPS")
        self.assertEqual(network.reloads, ["candidate HTTPS"])
        self.assertFalse(network.force)

    def test_failures_back_off_before_retrying_certificate_requests(self):
        path, network = self.run_case("certificate")
        with patch.object(controller, "SITE_CONF", str(path)):
            controller.run_cycle(network)
        self.assertEqual(network.certificate_calls, 1)
        self.assertTrue(network.force)

    def test_certificate_domain_arguments_are_unique(self):
        network = FakeNetwork(Path("unused"))
        network.servers = ["example.invalid", "example.invalid", "www.example.invalid"]
        with patch.object(nginx, "DEV", False), patch.object(nginx.subprocess, "run") as run:
            run.return_value.returncode = 0
            self.assertTrue(nginx.run_certbot(network))
        arguments = run.call_args.args[0]
        self.assertEqual(arguments.count("-d"), 2)


if __name__ == "__main__":
    unittest.main()
