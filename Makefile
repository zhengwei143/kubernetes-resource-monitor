.PHONY: api verifier watcher clear_redis
SHELL := /bin/bash

create_env:
	touch development.env

api: create_env
	{ \
	source development.env ;\
	python3 servers/app_api.py ;\
	}

verifier: create_env
	{ \
	source development.env ;\
	python3 servers/app_verifier.py ;\
	}

watcher: create_env
	{ \
	source development.env ;\
	python3 servers/app_watcher.py ;\
	}

aggregator: create_env
	{ \
	source development.env ;\
	python3 servers/app_aggregator.py ;\
	}
