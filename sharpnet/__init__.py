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
        self.containers = []
        self.containers_last = []
        self.servers = []
        self.containers_loaded = []
        self.cache = {}
        self.new_containers = []
        self.problem_container = None
        self.error = None
        self.force = False
        self.last_cert_check_date = date.today()
