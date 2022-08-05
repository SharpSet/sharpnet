import subprocess
import logging
from datetime import date

from sharpnet.classes import CacheData
from sharpnet.constants import DUMMY_CONF, TEST_SITE_CONF


def cache_data(network, container, servers=None, mercy=None):
    """
    Cache that stores data for a container

    This is used to make sure that the container is not a restarted on a mercy run
    """

    data = network.cache.get(container.name)

    if data is None:
        data = CacheData()

    if servers is not None:
        data.servers = servers

    if mercy is not None:
        data.mercy = mercy

    logging.debug("Data was cached for %s", container.name)
    network.cache[container.name] = data


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


def refresh(network):
    """
    Remove all data that is meant for one loop

    Check if network should update certs
    """

    network.containers_last = network.containers
    network.containers = []
    network.containers_loaded = []
    network.servers = []

    if network.last_cert_check_date != date.today():
        logging.debug("New Day!")
        network.last_cert_check_date = date.today()
        network.force = True


def set_problem_container(network, container):
    """
    Sets the current loops problem container

    If it is already set, it will not override.
    """
    if not network.problem_container:
        network.problem_container = container


def set_error(network, error):
    """
    Sets the current loops error

    Will be used on its own if error not related to a container
    """

    if not network.error:
        network.error = error
