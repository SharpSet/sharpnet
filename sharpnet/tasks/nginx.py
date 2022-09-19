import subprocess
import re
import copy

from sharpnet.constants import CERTBOT_COMMAND, DEV, DOMAIN


def run_certbot(network):
    """
    Uses all stored domains from sharpnet file to generate SSL certificates for each of them
    """

    certbot_command = CERTBOT_COMMAND

    servers = copy.deepcopy(network.servers)

    if DOMAIN in servers:
        servers.remove(DOMAIN)
        servers.insert(0, DOMAIN)

    # sort servers in alphabetical order
    servers.sort()

    for server in servers:
        certbot_command += f" -d {server}"

    print(certbot_command)

    if not DEV:

        result = subprocess.run(certbot_command.split(" "), check=False)
        if result.returncode != 0:
            return False

    return True


def run_nginx(network):
    """
    Reloads nginx to install new sharpnet full config
    """

    result = subprocess.run(
        ["service", "nginx", "reload"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )

    if result.returncode != 0:
        network.set_error("Failed to run Nginx")


def find_servers(network, config):
    """
    Find all servers in a nginx configuartion using regex
    """

    con_servers = []

    matches = re.findall("server_name(.*);", config)
    if matches is None:
        network.set_error("Failed to find any servers")
    else:
        for server in matches:
            for domain in server.strip().split(" "):
                domain = domain.replace(" ", "")
                con_servers.append(domain)

    return con_servers


def get_configs(_, full_config):
    """
    Get all configs from a full config
    """

    configs = []
    open_bracket = 0
    last_start_index = 0
    started = False

    for index, char in enumerate(full_config):
        if char == "{":
            open_bracket += 1
            started = True

        if char == "}":
            open_bracket -= 1

        if open_bracket == 0 and started:
            configs.append(full_config[last_start_index : index + 1])
            last_start_index = index + 1
            started = False

    return configs
