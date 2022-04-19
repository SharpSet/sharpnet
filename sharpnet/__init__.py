from datetime import date

class Sharpnet():
    """
    Special code that allows all tasks to be considered part of
    the Sharpnet Class
    """

    from sharpnet.tasks.docker import get_containers, load_containers, kill
    from sharpnet.tasks.general import (cache_data, ensure_loaded,
                                        refresh, set_problem_container, set_error)
    from sharpnet.tasks.nginx import run_certbot, run_nginx, find_servers
    from sharpnet.tasks.network import run_cycle, load
    from sharpnet.tasks.handlers import handle_minor, handle_major, printing
    from sharpnet.tasks.mail import mail_error

    def __init__(self):

        # stores all containers that are currently running
        self.containers = []

        # stores all servers that were running on the last run
        self.containers_last = []

        # stores all servers that are currently running in NGINX
        self.servers = []

        # stores all servers that were loaded into sharpnets NGINX config
        self.containers_loaded = []

        # stores infomation about containers
        self.cache = {}

        # stores difference between containers and last_containers
        self.new_containers = []

        # keeps track of container with error
        self.problem_container = None

        # Stores type of error
        self.error = None

        # stores if there should be a fresh run
        self.force = False
        self.last_cert_check_date = date.today()
