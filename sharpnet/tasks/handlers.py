import time


def handle_major(network):
    """
    Triggered if the error is considered major.

    Container will instantly be killed and a force-restart will be triggered.

    In most situations this will not create downtime
    """
    if network.problem_container:
        network.printing()
        network.kill(network.problem_container)

    else:
        print("No problem containers but error raised!")

    network.problem_container = None
    network.error = None
    network.force = True


def handle_minor(network):
    """
    Triggered when a loop error is considered minor.

    This means that the container will be given one more loop to not fail

    After this "mercy" run, the error will be treated as major.
    """

    if network.problem_container:
        network.printing()
        cache = network.cache.get(network.problem_container.name)
        if cache and not cache.mercy:
            print(f"Container {network.problem_container.name} used mercy run...\n")
            network.kill(network.problem_container)

        else:
            print(
                f"Container {network.problem_container.name} will be will have a single mercy run..."
            )
            print("Sleeping for 15 seconds!")
            time.sleep(15)
            network.cache_data(network.problem_container, mercy=False)
            network.load()

    else:
        print("No problem containers but error raised!")
        network.force = True

    network.problem_container = None
    network.error = None


def printing(network):
    """
    Prints the current state of the containers
    """

    print(f"ERRORS FOUND [{network.problem_container.name}]")
    print("======================")
    print(f"[{network.error}]")
