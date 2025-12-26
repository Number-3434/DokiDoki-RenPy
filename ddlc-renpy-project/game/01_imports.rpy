init -65536 python:
    import os, sys

    # Add packages from /lib to sys.path
    sys.path.insert(0, os.path.join(config.basedir, "lib"))

    def import_check(*targets: str):
        import importlib

        for target in targets:
            try:
                importlib.import_module(target)
            except Exception as e:
                raise Exception(
                    f"Could not find the module '{target}'. "
                    f"Please add it to the 'requirements.txt' file, then run 'make install'.\n"
                    f"Original error: {e}"
                )

    def import_error(e: Exception):
        raise Exception("An error occured loading external modules. Try running 'make install'. You may need to install 'make' first. Additionally, note that this project requires the ren'py 8.5 SDK or greater.") from e
