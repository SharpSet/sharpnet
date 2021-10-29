import os
import subprocess
import time
from shutil import copyfile

import requests

from sharpnet import Sharpnet
from sharpnet.classes import Container
from sharpnet.constants import (DEFAULT_CONF, NETWORK, NGINX_CONF,
                                OPTIONS_SSL_NGINX_CONF, SECURITY_CONF,
                                SITE_CONF, TEST_CONF, DUMMY_CONF)


def loop(network):

    while True:

        network.get_containers()

        if network.new_containers:
            print("===========================")
            print(f"NEW CONTAINERS FOUND")
            print("===========================\n")
            network.run_cycle()

        # If there has been a specific error, a force restart might be called
        if network.force:
            print(f"Forced to Run from scratch")
            open(SITE_CONF, 'w').close()
            network.cache = {}
            network.force = False
            network.run_cycle()

        time.sleep(1)
        network.refresh()


if __name__ == "__main__":
    network = Sharpnet()

    open(SITE_CONF, 'w').close()

    # Disabled due to not having expected behavior
    # copyfile(REDIRECT_CONF, DEFAULT_SITE_CONF)

    copyfile(DEFAULT_CONF, NGINX_CONF)
    copyfile(SECURITY_CONF, OPTIONS_SSL_NGINX_CONF)
    copyfile(TEST_CONF, DUMMY_CONF)

    subprocess.run(["nginx"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    loop(network)
