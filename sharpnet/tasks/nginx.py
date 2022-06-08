import subprocess
import re

from sharpnet.constants import CERTBOT_COMMAND, DEV


def run_certbot(self):
    """
    Uses all stored domains from sharpnet file to generate SSL certificates for each of them
    """

    certbot_command = CERTBOT_COMMAND

    for server in self.servers:
        certbot_command += (f" -d {server}")

    if DEV:
        print(certbot_command)

    else:
        result = subprocess.run(["certbot", "renew"], check=False)
        if result.returncode != 0:
            return False

        result = subprocess.run(certbot_command.split(" "), check=False)
        if result.returncode != 0:
            return False

    return True


def run_nginx(self):
    """
    Reloads nginx to install new sharpnet full config
    """

    result = subprocess.run(
        ["service", "nginx", "reload"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False
    )

    if result.returncode != 0:
        self.set_error("Failed to run Nginx")


def find_servers(self, config):
    """
    Find all servers in a nginx configuartion using regex
    """

    con_servers = []

    matches = re.findall('server_name(.*);', config)
    if matches is None:
        self.set_error("Failed to find any servers")
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
            configs.append(full_config[last_start_index:index + 1])
            last_start_index = index + 1
            started = False

    return configs
