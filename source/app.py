import subprocess
import traceback
import os
import time
import json
import re

previous_run = 0
containers = 0
config = ""
servers = []
while True:
    out = subprocess.check_output(["sh", "-c", "docker network inspect sharpnet"])
    data = json.loads(out)[0]

    if len(data["Containers"]) > previous_run:
        open('/etc/nginx/conf.d/site.conf', 'w').close()
        print("New containers detected!!")

        for container in data["Containers"].values():
            name = container["Name"]

            with open("/etc/nginx/conf.d/site.conf", 'a') as out:
                result = subprocess.run(["sh", "-c", f"docker exec {name} cat /sharpnet/nginx.conf"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                config = result.stdout.decode("utf-8")
                err = result.stderr.decode("utf-8")

                if result.returncode != 0:
                    if "/sharpnet/nginx.conf: No such file or directory" in err:
                        print(f"{name} did not have a nginx config file, ignoring")
                    else:
                        print("Error not regonized, attempting to skip")
                        print(err)

                else:
                    out.write(config + "\n")

                    print(f"Taken container {name}'s nginx config")
                    containers += 1

                    server = re.search('server_name(.*);', config)
                    servers.append(server.group(1).replace(" ", ""))

        if containers != 0:

            # If a new run
            if previous_run == 0:
                subprocess.run(["nginx"])

            certbot = "certbot --nginx --email adam@mcaq.me --agree-tos --redirect --noninteractive --expand"

            for server in servers:
                certbot += (f" -d {server}")
            # subprocess.run(certbot.split(" "))
            print(certbot)

            subprocess.run(["service", "nginx", "reload"])


        previous_run = len(data["Containers"])

    else:
        print("no new containers")
    time.sleep(5)
