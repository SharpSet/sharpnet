import time

def handle_major(self):
    self.printing()
    self.kill(self.problem_container)

    self.problem_container = None
    self.error = None
    self.force = True

def handle_minor(self):
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

    self.problem_container = None
    self.error = None


def printing(self):
    print(f"ERRORS FOUND [{self.problem_container.name}]")
    print("======================")
    print(f"[{self.error}]")
