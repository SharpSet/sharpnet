import logging
import os
import subprocess
import time
from shutil import copyfile

from sharpnet import Sharpnet
from sharpnet.constants import (DEFAULT_INDEX_PAGE, DEFAULT_PAGE, DUMMY_CONF,
                                LOC_DUMMY_CONF, LOC_NGINX_CONF,
                                LOC_OPTIONS_SSL_NGINX_CONF, NGINX_CONF,
                                OPTIONS_SSL_NGINX_CONF, SITE_CONF)

network = Sharpnet()


def loop():
    """
    Defines a single loop of the program.
    """

    while True:

        network.get_containers()

        if network.new_containers:
            print("===========================")
            print("NEW CONTAINERS FOUND")
            print("===========================\n")
            network.run_cycle()

        # If there has been a specific error, a force restart might be called
        if network.force:
            print("Forced to Run from scratch")
            open(SITE_CONF, 'w', encoding="utf-8").close()
            network.cache = {}
            network.force = False
            network.run_cycle()

        time.sleep(1)
        network.refresh()


if __name__ == "__main__":

    if os.environ.get("DEBUG_LOGGING") == "TRUE":
        logging.basicConfig(level=logging.DEBUG)

    open(SITE_CONF, 'w', encoding="utf-8").close()

    # Add a default index page
    copyfile(DEFAULT_INDEX_PAGE, DEFAULT_PAGE)

    copyfile(LOC_NGINX_CONF, NGINX_CONF)
    copyfile(LOC_OPTIONS_SSL_NGINX_CONF, OPTIONS_SSL_NGINX_CONF)
    copyfile(LOC_DUMMY_CONF, DUMMY_CONF)

    proc = subprocess.run(
        ["nginx"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False
    )

    # check command run
    if proc.returncode == 0:
        print("Nginx started")
    loop()
