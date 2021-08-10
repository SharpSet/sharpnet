import re
import requests
import time
from sharpnet.classes import CacheData, Container

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

    runs = 0

    while True:
        matches = re.findall('proxy_pass(.*);', config)
        for address in matches:
            address = address.replace(" ", "")

            try:
                r = requests.head(address)
                r.raise_for_status()
                return True

            except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
                pass

        time.sleep(1)
        runs += 1

        if runs > 20:
            return False


def refresh(self):
    self.containers_last = self.containers
    self.containers = []
    self.containers_loaded = []
    self.servers = []
    self.problem_container = None