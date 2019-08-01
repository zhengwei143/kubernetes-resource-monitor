.PHONY: api verifier watcher clear_redis
SHELL := /bin/bash

create_env:
	touch development.env

api: create_env
	{ \
	source development.env ;\
	python3 servers/api.py ;\
	}

verifier: create_env
	{ \
	source development.env ;\
	python3 servers/verifier.py ;\
	}

watcher: create_env
	{ \
	source development.env ;\
	python3 servers/watcher.py ;\
	}

clear_redis: create_env
	{ \
	source development.env ;\
	python3 servers/clear.py ;\
	}
