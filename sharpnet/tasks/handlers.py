import time

def handle_major(self):
    """
    Triggered if the error is considered major.

    Container will instantly be killed and a force-restart will be triggered.

    In most situations this will not create downtime
    """
    if self.problem_container:
        self.printing()
        self.kill(self.problem_container)

    else:
        print("No problem containers but error raised!")

    self.problem_container = None
    self.error = None
    self.force = True

def handle_minor(self):
    """
    Triggered when a loop error is considered minor.

    This means that the container will be given one more loop to not fail

    After this "mercy" run, the error will be treated as major.
    """

    if self.problem_container:
        self.printing()
        cache = self.cache.get(self.problem_container.name)
        if cache and not cache.mercy:
            print(f"Container {self.problem_container.name} used mercy run...\n")
            self.kill(self.problem_container)

        else:
            print(f"Container {self.problem_container.name} will be will have a single mercy run...")
            print("Sleeping for 15 seconds!")
            time.sleep(15)
            self.cache_data(self.problem_container, mercy=False)
            self.load()

    else:
        print("No problem containers but error raised!")
        self.force = True

    self.problem_container = None
    self.error = None


def printing(self):
    print(f"ERRORS FOUND [{self.problem_container.name}]")
    print("======================")
    print(f"[{self.error}]")
