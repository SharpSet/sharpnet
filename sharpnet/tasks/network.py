import os

from sharpnet.constants import DEV

def run_cycle(self):
    """
    Run Cycle that runs once every loop
    """

    print("Loading Containers")
    print("======================")

    self.load()

    print("Reloading Nginx")
    print("======================")

    self.run_nginx()

    if self.error:
        self.handle_major()

    print("\n======================")
    print("** SHARPNET ACTIVE **")
    print("======================\n")


def load(self):
    """
    Loads Docker containers and activates certbot.
    """

    config_changes = self.load_containers()

    if self.problem_container:
        self.set_error("Error Loading Container")

    if self.containers_loaded and config_changes:

        print("======================")
        certbot_success = self.run_certbot()
        print("======================\n")

        if not certbot_success:
            self.set_error("Failed to Load Certbot")

    if not config_changes:
        print("No changes to config!\n")

    if self.error:
        self.handle_minor()
