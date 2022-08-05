from datetime import date


class Sharpnet:
    """
    Special code that allows all tasks to be considered part of
    the Sharpnet Class
    """

    from sharpnet.tasks.docker import get_containers, kill, load_containers
    from sharpnet.tasks.general import (
        cache_data,
        ensure_loaded,
        refresh,
        set_error,
        set_problem_container,
    )
    from sharpnet.tasks.handlers import handle_major, handle_minor, printing
    from sharpnet.tasks.mail import mail_error
    from sharpnet.tasks.network import load, run_cycle
    from sharpnet.tasks.nginx import find_servers, run_certbot, run_nginx, get_configs

    def __init__(self):

        network = self

        # stores all containers that are currently running
        network.containers = []

        # stores all servers that were running on the last run
        network.containers_last = []

        # stores all servers that are currently running in NGINX
        network.servers = []

        # stores all servers that were loaded into sharpnets NGINX config
        network.containers_loaded = []

        # stores infomation about containers
        network.cache = {}

        # stores difference between containers and last_containers
        network.new_containers = []

        # keeps track of container with error
        network.problem_container = None

        # Stores type of error
        network.error = None

        # stores if there should be a fresh run
        network.force = False
        network.last_cert_check_date = date.today()
