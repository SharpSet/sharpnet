import os
import subprocess
import time
from shutil import copyfile

from sharpnet import Sharpnet
from sharpnet.classes import Container
from sharpnet.constants import (LOC_NGINX_CONF, NETWORK, NGINX_CONF,
                                OPTIONS_SSL_NGINX_CONF, LOC_OPTIONS_SSL_NGINX_CONF,
                                SITE_CONF, LOC_DUMMY_CONF, DUMMY_CONF)


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

    copyfile(LOC_NGINX_CONF, NGINX_CONF)
    copyfile(LOC_OPTIONS_SSL_NGINX_CONF, OPTIONS_SSL_NGINX_CONF)
    copyfile(LOC_DUMMY_CONF, DUMMY_CONF)

    subprocess.run(["nginx"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    loop(network)
