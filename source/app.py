import subprocess
import traceback
import os
import time
import json
import re
from shutil import copyfile

previous_run = 0
new = True
containers = 0
config = ""
error = False

if os.environ.get("DEV") == "TRUE":
    network = "sharpnet_testing"

else:
    network = "sharpnet"

while True:
    servers = []
    out = subprocess.check_output(["sh", "-c", f"docker network inspect {network}"])
    data = json.loads(out)[0]

    if len(data["Containers"]) > previous_run:
        open("/etc/nginx/conf.d/site.conf", 'w').close()
        copyfile('/source/default.conf', '/etc/nginx/nginx.conf')
        print("New containers detected!!")
        print("Waiting 5 Seconds for boot...")
        time.sleep(5)

        for container in data["Containers"].values():
            name = container["Name"]

            with open("/etc/nginx/conf.d/site.conf", 'a') as out:
                result = subprocess.run(["sh", "-c", f"docker exec {name} cat /sharpnet/nginx.conf"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                config = result.stdout.decode("utf-8")
                err = result.stderr.decode("utf-8")

                if result.returncode != 0:
                    if "No such file or directory" in err:
                        print(f"{name} did not have a nginx config file, ignoring")
                    else:
                        print(f"Error in {name} not regonized, attempting to skip")
                        print(err, config)

                else:
                    out.write(config + "\n")

                    matches = re.findall('server_name(.*);', config)
                    if matches is None:
                        print("No server_name variable found, skipping")
                    else:
                        for server in matches:
                            for subdomain in server.strip().split(" "):
                                servers.append(subdomain.replace(" ", ""))
                        print(f"Taken container {name}'s nginx config")
                        containers += 1

        if containers != 0:

            # If a new run
            if new or error:
                subprocess.run(["nginx"])
                new = False

            certbot = "certbot --nginx --email adam@mcaq.me --cert-name mcadesigns.co.uk --agree-tos --redirect --noninteractive --expand"

            for server in servers:
                certbot += (f" -d {server}")

            if os.environ.get("DEV") == "TRUE":
                print(certbot)

            else:
                subprocess.run(certbot.split(" "))

            result = subprocess.run(["service", "nginx", "reload"], stdout=subprocess.PIPE)

            if result.returncode != 0:
                print("Nginx Failed to Reload, skipping")
                error = True

            print("SHARPNET ACTIVE")

    previous_run = len(data["Containers"])

    time.sleep(1)
