import os
import requests

from sharpnet.constants import DEV

def run_cycle(self):

    print("Loading Containers")
    print("======================")

    self.load()

    print("Reloading Nginx")
    print("======================")

    self.run_nginx()

    if self.error:
        self.handle_major()

    self.post_checks()

    if self.error:
        self.handle_major()

    print("\n======================")
    print("** SHARPNET ACTIVE **")
    print("======================\n")


def load(self):

    config_changes = self.load_containers()

    if self.problem_container:
        self.error = "Error loading container"

    if self.containers_loaded and config_changes:

        print("======================")
        certbot_success = self.run_certbot()
        print("======================\n")

        if not certbot_success:
            self.error = "Failed to Load Certbot"

    if not config_changes:
        print("No changes to config!\n")

    if self.error:
        self.handle_minor()



def post_checks(self):
    for container in self.containers:
        data = self.cache.get(container.name)
        if data:
            for server in data.servers:

                if DEV:
                    scheme = "http"
                    port = "180"
                else:
                    scheme = "https"
                    port = ""

                try:
                    r = requests.head(f"{scheme}://{server}:{port}")
                    r.raise_for_status()

                    if r.status_code != 200:
                        print("Status code not 200")
                        raise requests.exceptions.HTTPError()

                except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
                    self.problem_container = (container)
                    self.error = "Some containers failed to connect"