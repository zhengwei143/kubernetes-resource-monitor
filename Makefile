.PHONY: build test_api api verifier streamer aggregator clear_redis
SHELL := /bin/bash

DOCKER_REGISTRY = docker-registry:5000
KRM_IMAGE = krm-app
KRM_TAG = latest

build:
	{ \
	docker build --rm -t $(DOCKER_REGISTRY)/$(KRM_IMAGE):$(KRM_TAG) . ;\
	docker push $(DOCKER_REGISTRY)/$(KRM_IMAGE):$(KRM_TAG) ;\
	}

create_env:
	touch development.env

test_api:
	{ \
	source development.env ;\
	python3 app/test_api.py ;\
	}

api: create_env
	{ \
	source development.env ;\
	python3 app/app_api.py ;\
	}

verifier: create_env
	{ \
	source development.env ;\
	python3 app/app_verifier.py ;\
	}

streamer: create_env
	{ \
	source development.env ;\
	python3 app/app_streamer.py ;\
	}

aggregator: create_env
	{ \
	source development.env ;\
	python3 app/app_aggregator.py ;\
	}
