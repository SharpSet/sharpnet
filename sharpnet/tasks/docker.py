import json
import logging
import subprocess

from sharpnet.classes import Container
from sharpnet.constants import SITE_CONF, NETWORK


def get_containers(self):
    """
    Gets all containers on sharpnet network

    Also sets all new containers
    """

    format_json = (
        '{"Name":"{{.Names}}","State":"{{.State}}"}'
    )
    out = subprocess.check_output(
        ["docker", "ps", "--filter", f"network={NETWORK}", "--format", f"{format_json}"]
    )

    out = out.decode("utf-8").replace("\n", ",\n")[:-2]
    out = f"[\n{out}\n]"
    data = json.loads(f"{out}")

    for con_dict in data:
        container = Container(con_dict["Name"])

        running = con_dict["State"] == "running"
        host = "sharpnet" in con_dict["Name"]

        if running and not host:
            self.containers.append(container)

    self.new_containers = [
        container for container in self.containers if container not in self.containers_last
    ]


def load_containers(self):

    """
    Attempts to "load" all containers that were found.

    "loading" includes:
        - checking for a sharpnet nginx configuration
        - checking the config has no errors
        - adding all domains from the config into storage
    """

    changes = False

    for container in self.containers:

        print(f"\n** [LOADING {container.name}] **")

        con_servers = []
        loaded = False
        ignoring = False

        with open(SITE_CONF, 'a') as out:

            result = subprocess.run(
                ["sh", "-c", f"docker exec {container.name} cat /sharpnet/nginx.conf"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False
            )

            config = result.stdout.decode("utf-8")
            err = result.stderr.decode("utf-8")

            # Error finding the nginx conf
            if result.returncode != 0:

                # No config file, this is okay
                if "No such file or directory" in err:
                    print(f"{container.name} did not have a nginx config file, ignoring\n")
                    ignoring = True
                else:
                    print(f"Error in {container.name} not recognized, attempting to skip")
                    print(err, config)
                    self.set_problem_container(container)
            else:

                with open(SITE_CONF, 'r') as full_config:
                    full_config = full_config.read()

                    con_servers = self.find_servers(config)
                    if not con_servers:
                        self.set_problem_container(container)
                        continue

                    print(f"Making sure {container.name} is ready.")
                    loaded = self.ensure_loaded(config)

            if loaded:
                print(f"Loaded container {container.name}'s' config")
                self.containers_loaded.append(container)
                self.cache_data(container, servers=con_servers)

                # check if config has been previously loaded
                if any(server in full_config for server in con_servers):
                    # Now we need to make sure that if the config
                    # has changed, that it is removed.
                    # Get the configs
                    old_configs = self.get_configs(full_config)

                    relavent_old_config = ""

                    # Find the one we are interested in
                    for old_config in old_configs:

                        old_servers = self.find_servers(old_config)

                        if sorted(old_servers) == sorted(con_servers):
                            relavent_old_config = old_config
                            break

                    # if relavent_old_config and config do not match
                    # remove config from full_config

                    configs_are_different = (
                        relavent_old_config.replace("\n", "") != config.replace("\n", "")
                    )

                    configs_are_same = (
                        relavent_old_config.replace("\n", "") == config.replace("\n", "")
                    )

                    if not relavent_old_config:
                        print("Unable to find old config, adding new config")

                    elif relavent_old_config and configs_are_different:
                        print(f"Removing old config from {container.name}")
                        full_config = full_config.replace(relavent_old_config, "")

                    elif relavent_old_config and configs_are_same:
                        print("Configuration has not changed... ignoring")
                        logging.debug("The new config is the same as the old config")

                    else:
                        print("ERROR - Something went wrong!")
                        self.handle_major()

                # If config is not already loaded...
                if config not in full_config:
                    logging.debug("Config for %s was added.", container.name)
                    changes = True

                    out.write(config + "\n")

                else:
                    logging.debug("Config for %s was already added.", container.name)

                for server in con_servers:
                    self.servers.append(server)

            if not loaded and not ignoring:
                print(f"Failed to load {container.name}'s' config")
                print(config)
                self.set_problem_container(container)

    return changes


def kill(self, container):
    """
    Kills a container
    """

    print(f"Shutting down {container.name} remotely...")
    subprocess.run(
        ["sh", "-c", f"docker stop {container.name}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False
    )

    try:
        self.containers.remove(container)
        self.containers_loaded.remove(container)
    except ValueError:
        pass
    print(f"{container.name} was killed.\n")
    self.mail_error(container)
