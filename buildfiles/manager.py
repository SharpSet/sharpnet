import subprocess
from flask import Flask, request


class Server():
    def __init__(self, values):
        self.domain = values["domain"]
        self.phpcontainer = values["server"]
        self.root = values["root"]

    def active(self):
        return True


class Servers():
    def __init__(self):
        self.list = []

    def save(self, certbot):
        config = ""

        for server in self.list:
            if server.active():
                config += (
                    f"server {{\n"
                    f"  listen 80;\n"
                    f"  server_name {server.domain};\n"
                    f"  root {server.root};\n"
                    f"  index index.php;\n"

                    f"  location / {{\n"
    	            f"    include fastcgi_params;\n"
                    f"    fastcgi_pass {server.phpcontainer}:9000;\n"
                    f"    fastcgi_param SCRIPT_FILENAME /code/{server.phpcontainer}/app.php;\n"
                    f"  }}\n"

                    f"  location ~ \.(jpg|png|css|js|html|json|svg|jpeg) {{"
                    f"    try_files $uri =404;\n"
                    f"  }}\n"
                    "}\n"

                )

                certbot += f" -d {server.domain}"

            else:
                self.list.remove(server)

        with open("/etc/nginx/conf.d/site.conf", 'w+') as out:
            out.write(config + "\n")

        return certbot


app = Flask(__name__)


@app.route('/', methods=["POST"])
def add_server():

    certbot = "certbot --nginx --email adam@mcaq.me --agree-tos --redirect --noninteractive --expand"

    server = Server(request.values)
    if server not in servers.list:
        servers.list.append(server)
    certbot = servers.save(certbot)

    subprocess.run(["service", "nginx", "stop"])
    subprocess.run(["nginx"])
    subprocess.run(certbot.split(" "))
    # print(certbot)
    subprocess.run(["service", "nginx", "stop"])

    proc = subprocess.run(["nginx", "-g", "daemon off;"])
    if proc.returncode != 0:
        print(proc.stderr)
        exit(1)


servers = Servers()
app.run(host='0.0.0.0', port=5777)