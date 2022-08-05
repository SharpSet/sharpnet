def run_cycle(network):
    """
    Run Cycle that runs once every loop
    """

    print("Loading Containers")
    print("======================")

    network.load()

    print("Reloading Nginx")
    print("======================")

    network.run_nginx()

    if network.error:
        network.handle_major()

    print("\n======================")
    print("** SHARPNET ACTIVE **")
    print("======================\n")


def load(network):
    """
    Loads Docker containers and activates certbot.
    """

    network.load_containers()

    if network.problem_container:
        network.set_error("Error Loading Container")

    if network.containers_loaded:

        print("======================")
        certbot_success = network.run_certbot()
        print("======================\n")

        if not certbot_success:
            network.set_error("Failed to Load Certbot")

    if network.error:
        network.handle_minor()
