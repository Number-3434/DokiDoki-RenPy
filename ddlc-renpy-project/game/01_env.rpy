init -4096 python:
    import os

    def load_env():
        try:
            with open(os.path.join(config.basedir, ".env"), "r") as f:
                parse_env(f.read())
        except FileNotFoundError:
            raise Exception("No .env file found. Please create one and add your Azure Speech API key.")

    def parse_env(env):
        for line in env.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            os.environ[key.strip()] = value.strip()

    load_env()