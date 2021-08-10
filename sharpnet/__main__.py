import subprocess
import os
import time
import requests

from sharpnet import Sharpnet
from shutil import copyfile
from sharpnet.constants import CERTBOT_COMMAND, SITE_CONF, REDIRECT_CONF, DEFAULT_SITE_CONF


def loop(network):

    while True:

        network.get_containers()

        if network.new_containers:
            print("===========================")
            print(f"NEW CONTAINERS FOUND")
            print("===========================\n")
            network.run_cycle()

        if network.force:
            print(f"Forced to run")
            network.run_cycle()
            network.force = False

        time.sleep(1)
        network.refresh()



if __name__ == "__main__":
    network = Sharpnet()

    open(SITE_CONF, 'w').close()
    # copyfile(REDIRECT_CONF, DEFAULT_SITE_CONF)
    subprocess.run(["nginx"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    loop(network)