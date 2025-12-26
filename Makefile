
PYTHON := python3
PIP := $(PYTHON) -m pip

install:  ## Install dependencies
	$(PIP) install -r requirements.txt --target=ddlc-renpy-project/lib
