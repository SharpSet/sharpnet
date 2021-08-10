import json
import subprocess
from shutil import copyfile

from sharpnet.classes import Container
from sharpnet.constants import SITE_CONF, NETWORK


def get_containers(self):
    format_json = (
        '{"Name":"{{.Names}}","State":"{{.State}}"}'
    )
    out = subprocess.check_output(["docker", "ps", "--filter", f"network={NETWORK}", "--format", f"{format_json}"])
    out = out.decode("utf-8").replace("\n", ",\n")[:-2]
    out = f"[\n{out}\n]"
    data = json.loads(f"{out}")

    for con_dict in data:
        container = Container(con_dict["Name"])

        running = con_dict["State"] == "running"
        host = "sharpnet" in con_dict["Name"]

        if running and not host:
            self.containers.append(container)

    self.new_containers = [container for container in self.containers if container not in self.containers_last]


def load_containers(self):

    changes = False

    for container in self.containers:

        print(f"** [LOADING {container.name}] **")

        con_servers = []
        loaded = False
        ignoring = False

        with open(SITE_CONF, 'a') as out:

            result = subprocess.run(["sh", "-c", f"docker exec {container.name} cat /sharpnet/nginx.conf"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            config = result.stdout.decode("utf-8")
            err = result.stderr.decode("utf-8")

            if result.returncode != 0:
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
                print(f"Loaded container {container.name}'s' config\n")
                self.containers_loaded.append(container)
                self.cache_data(container, servers=con_servers)

                if config not in full_config:
                    changes = True

                    out.write(config + "\n")

                for server in con_servers:
                    self.servers.append(server)

            if not loaded and not ignoring:
                print(f"Failed to load {container.name}'s' config\n")
                self.set_problem_container(container)

    return changes


def kill(self, container):
    print(f"Shutting down {container.name} remotely...")
    subprocess.run(["sh", "-c", f"docker stop {container.name}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        self.containers.remove(container)
        self.containers_loaded.remove(container)
    except ValueError:
        pass
    print(f"{container.name} was killed.\n")
