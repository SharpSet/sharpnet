import subprocess
import logging
from datetime import date

from sharpnet.classes import CacheData
from sharpnet.constants import DUMMY_CONF, TEST_SITE_CONF


def cache_data(self, container, servers=None, mercy=None):
    """
    Cache that stores data for a container

    This is used to make sure that the container is not a restarted on a mercy run
    """

    data = self.cache.get(container.name)

    if data is None:
        data = CacheData()

    if servers is not None:
        data.servers = servers

    if mercy is not None:
        data.mercy = mercy

    logging.debug("Data was cached for %s", container.name)
    self.cache[container.name] = data


def ensure_loaded(_, config):
    """
    Makes sure the sharpnet config from a container is valid

    If it is not, it will not be loaded to avoid errors.
    """

    with open(TEST_SITE_CONF, "w+") as file:
        file.write(config)

    result = subprocess.run(["nginx", "-c", DUMMY_CONF, "-t"], check=False)
    if result.returncode != 0:
        return False

    else:
        return True

    # Delete TEST_SITE_CONF file
    subprocess.run(["rm", TEST_SITE_CONF], check=False)


def refresh(self):
    """
    Remove all data that is meant for one loop

    Check if network should update certs
    """

    self.containers_last = self.containers
    self.containers = []
    self.containers_loaded = []
    self.servers = []

    if self.last_cert_check_date != date.today():
        logging.debug("New Day!")
        self.last_cert_check_date = date.today()
        self.force = True


def set_problem_container(self, container):
    """
    Sets the current loops problem container

    If it is already set, it will not override.
    """
    if not self.problem_container:
        self.problem_container = container


def set_error(self, error):
    """
    Sets the current loops error

    Will be used on its own if error not related to a container
    """

    if not self.error:
        self.error = error
