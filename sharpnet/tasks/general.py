import re
import requests
import subprocess
import time
from sharpnet.classes import CacheData, Container
from sharpnet.constants import TEST_SITE_CONF, DUMMY_CONF

def cache_data(self, container, servers=None, mercy=None):
    data = self.cache.get(container.name)

    if data is None:
        data = CacheData()

    if servers is not None:
        data.servers = servers

    if mercy is not None:
        data.mercy = mercy

    self.cache[container.name] = data


def ensure_loaded(self, config):

    with open(TEST_SITE_CONF, "w+") as file:
        file.write(config)

    result = subprocess.run(["nginx", "-c", DUMMY_CONF, "-t"])
    if result.returncode != 0:
        return False

    else:
        return True


def refresh(self):
    self.containers_last = self.containers
    self.containers = []
    self.containers_loaded = []
    self.servers = []


def set_problem_container(self, container):
    if not self.problem_container:
        self.problem_container = container


def set_error(self, error):
    if not self.error:
        self.error = error