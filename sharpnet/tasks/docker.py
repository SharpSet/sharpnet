import json
import subprocess

from sharpnet.classes import Container
from sharpnet.constants import SITE_CONF, NETWORK


def get_containers(network):
    """
    Gets all containers on sharpnet network

    Also sets all new containers
    """

    format_json = '{"Name":"{{.Names}}","State":"{{.State}}"}'
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
            network.containers.append(container)

    network.new_containers = [
        container
        for container in network.containers
        if container not in network.containers_last
    ]


def load_containers(network):

    """
    Attempts to "load" all containers that were found.

    "loading" includes:
        - checking for a sharpnet nginx configuration
        - checking the config has no errors
        - adding all domains from the config into storage
    """

    configs = []

    for container in network.containers:

        print(f"\n** [LOADING {container.name}] **")

        con_servers = []
        loaded = False
        ignoring = False

        result = subprocess.run(
            ["sh", "-c", f"docker exec {container.name} cat /sharpnet/nginx.conf"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
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
                network.set_problem_container(container)
        else:
            con_servers = network.find_servers(config)
            if not con_servers:
                network.set_problem_container(container)
                continue

            print(f"Making sure {container.name} is ready.")
            loaded = network.ensure_loaded(config)

        if loaded:
            configs.append(config)
            print(f"Loaded container {container.name}'s' config")
            network.containers_loaded.append(container)
            network.cache_data(container, servers=con_servers)

            for server in con_servers:
                network.servers.append(server)

        if not loaded and not ignoring:
            print(f"Failed to load {container.name}'s' config")
            print(config)
            network.set_problem_container(container)

    # empty SITE_CONF
    with open(SITE_CONF, "w", encoding="utf-8") as f:
        f.write("")

    # write all configs to SITE_CONF
    with open(SITE_CONF, "a", encoding="utf-8") as f:
        for config in configs:
            f.write(config)
            f.write("\n")


def kill(network, container):
    """
    Kills a container
    """

    print(f"Shutting down {container.name} remotely...")
    subprocess.run(
        ["sh", "-c", f"docker stop {container.name}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    try:
        network.containers.remove(container)
        network.containers_loaded.remove(container)
    except ValueError:
        pass
    print(f"{container.name} was killed.\n")
    network.mail_error(container)
