IMAGE := quay.io/pantheon-public/composer-lock
TAG := latest

all: build push ## build and push all versions

build: ## build all versions
	docker build --pull -t $(IMAGE):$(TAG) .

run: ## run in a local docker container
	docker run --rm -p 5000:5000 $(IMAGE):$(TAG)

push: ## push all containers to docker registry
	docker push $(IMAGE):$(TAG)

help: ## print list of tasks and descriptions
	@grep -E '^[0-9a-zA-Z._-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

.PHONY: all build push
