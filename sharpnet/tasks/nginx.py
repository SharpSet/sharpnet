import subprocess
import os
import re

from sharpnet.constants import CERTBOT_COMMAND, DEV

def run_certbot(self):
    certbot_command = CERTBOT_COMMAND

    for server in self.servers:
        certbot_command += (f" -d {server}")

    if DEV:
        print(certbot_command)

    else:
        result = subprocess.run(certbot_command.split(" "))
        if result.returncode != 0:
            return False

    return True


def run_nginx(self):
    result = subprocess.run(["service", "nginx", "reload"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if result.returncode != 0:
        self.error = "Failed to run Nginx"
        self.handle_minor()


def find_servers(self, config):

    con_servers = []

    matches = re.findall('server_name(.*);', config)
    if matches is None:
        self.error = "Failed to find any servers"
    else:
        for server in matches:
            for domain in server.strip().split(" "):
                domain = domain.replace(" ", "")
                self.servers.append(domain)
                con_servers.append(domain)

    return con_servers