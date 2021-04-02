#===============================================================
# IBM Confidential
#
# OCO Source Materials
#
# Copyright IBM Corp. 2018,2019
#
# The source code for this program is not published or otherwise
# divested of its trade secrets, irrespective of what has been
# deposited with the U.S. Copyright Office.
#===============================================================

.PHONY: build run


S3FS_ENV_ATTRS=-e S3FS_BUCKET=${S3FS_BUCKET} -e S3FS_ACCESS_KEY=${S3FS_ACCESS_KEY} -e S3FS_SECRET_KEY=${S3FS_SECRET_KEY} -e S3FS_URL=${S3FS_URL}
NB_PORT:=8888
PROJECT=amhairc
NAMESPACE=fd4b_agrotech_incubation
PROJECT_VERSION:=$(shell sed -n '/version/,/version/p' setup.py | head -1 | awk -F'version=' '{ print $$2}' | awk -F',' '{print $$1}' | sed "s/^'\(.*\)'$$/\1/")

BASE_PROJECT_VERSION=0.1.0
BASE-IMAGE-OS=ubuntu:18.04

DATA_PATH=$${HOME}/IdeaProjects/amhairc/data/

.env:
	@touch .env

DUMMYINCLUDE:=$(shell if [ ! -z "cicd/Makefile.release.mk" ]; then mkdir -p cicd && touch cicd/Makefile.release.mk; fi)
DUMMYINCLUDE:=$(shell if [ ! -z ".env" ]; then touch .env; fi)

include .env
include cicd/Makefile.release.mk

help: # http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@echo $(PROJECT):$(PROJECT_VERSION)
	@echo "==========================================================="
	@echo $(DESC)
	@echo
	@echo The targets available in this project are:
	@grep -h -E '^[a-zA-Z0-9_%/-\.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\t\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo

env-%:
	@if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

build-base: ## Build docker base image
build-base:
	docker build -t $(PROJECT)-base:$(BASE_PROJECT_VERSION) -f Dockerfile.base .

build-base-integrated: ## Build docker base image
build-base-integrated:
	docker build -t $(PROJECT)-base:$(BASE_PROJECT_VERSION) -f Dockerfile.intbase .

build: .env
build: BASE-IMAGE=$(PROJECT)-base:$(BASE_PROJECT_VERSION)
build:
	docker build --build-arg BASE_IMAGE=$(BASE-IMAGE) \
				--build-arg PROJECT_VERSION=$(PROJECT_VERSION) \
				-t $(PROJECT):$(PROJECT_VERSION) .

build-api: .env
build-api: BASE-IMAGE=$(PROJECT)-base:$(BASE_PROJECT_VERSION)
build-api:
	docker build --build-arg BASE_IMAGE=$(BASE-IMAGE) \
				--build-arg PROJECT_VERSION=$(PROJECT_VERSION) \
				-t $(PROJECT)-api:$(PROJECT_VERSION) -f Dockerfile.api .

build-web: .env
build-web: BASE-IMAGE=$(PROJECT)-base:$(BASE_PROJECT_VERSION)
build-web:
	docker build --build-arg BASE_IMAGE=$(BASE-IMAGE) \
				--build-arg PROJECT_VERSION=$(PROJECT_VERSION) \
				-t $(PROJECT)-web:$(PROJECT_VERSION) -f Dockerfile.web .

run-it: ## Execute locally in interactive mode
run-it:
	docker run -p 80:5000 -it --privileged  $(PROJECT)-api:$(PROJECT_VERSION) bash

run-local:
	docker run $(S3FS_ENV_ATTRS) -v $(DATA_PATH):/opt/data/ -e "STAGE_SCRIPT=python3 /opt/amhairc.py" --privileged $(PROJECT):$(PROJECT_VERSION)

run-api:
	docker run -p 80:4500 --privileged -v $(DATA_PATH):/opt/data/ $(PROJECT)-api:$(PROJECT_VERSION)

run-web:
	docker run -p 81:5000 --privileged -v $(DATA_PATH):/opt/data/ $(PROJECT)-web:$(PROJECT_VERSION)

interactive: env-S3FS_ACCESS_KEY env-S3FS_SECRET_KEY env-S3FS_URL env-S3FS_BUCKET
	docker run $(S3FS_ENV_ATTRS)  -it --privileged $(PROJECT):$(PROJECT_VERSION) bash

push: ## Pushes image to registry
push: env-DOCKER_REGISTRY_URL
	@echo 'Pushes image to the private docker registry registry'
	@docker tag $(PROJECT):$(PROJECT_VERSION) $(DOCKER_REGISTRY_URL)/$(NAMESPACE)/$(PROJECT):$(PROJECT_VERSION)
	@docker push $(DOCKER_REGISTRY_URL)/$(NAMESPACE)/$(PROJECT):$(PROJECT_VERSION)

push-base: ## Pushes base image to registry
push-base: env-DOCKER_REGISTRY_URL 
	@echo 'Pushes image to the private docker registry registry'
	@docker tag $(PROJECT)-base:$(PROJECT_VERSION) $(DOCKER_REGISTRY_URL)/$(NAMESPACE)/$(PROJECT)-base:$(PROJECT_VERSION)
	@docker push $(DOCKER_REGISTRY_URL)/$(NAMESPACE)/$(PROJECT)-base:$(PROJECT_VERSION)


pull: ## Pulls base image from registry
pull: BASE-IMAGE=$(BASE-IMAGE-DEFAULT)
pull: env-DOCKER_REGISTRY_URL 
	@echo 'Pull image from the private docker registry registry'
	@docker pull $(DOCKER_REGISTRY_URL)/$(NAMESPACE)/$(BASE-IMAGE)
	@docker tag  $(DOCKER_REGISTRY_URL)/$(NAMESPACE)/$(BASE-IMAGE) $(BASE-IMAGE)

run: env-DOCKER_REGISTRY_URL
	docker pull $(DOCKER_REGISTRY_URL)/$(NAMESPACE)/$(PROJECT):$(DEPLOY_VERSION)
	docker tag $(DOCKER_REGISTRY_URL)/$(NAMESPACE)/$(PROJECT):$(DEPLOY_VERSION) $(DOCKER_REGISTRY_URL)/$(NAMESPACE)/$(PROJECT):$(DEPLOY_VERSION)-run
	docker push $(DOCKER_REGISTRY_URL)/$(NAMESPACE)/$(PROJECT):$(DEPLOY_VERSION)-run

# Example:
# $ docker images|grep veg
# analytics-vegetation-management                            2.0.8                da0824012402        10 days ago         5.68GB
# $ make retag TAG=2.0.8
# Retagging version 2.0.8 as 2.0.10
# docker tag analytics-vegetation-management:2.0.8 analytics-vegetation-management:2.0.10

retag: ## Retags existing image with TAG in the registry with latest PROJECT_VERSION number from setup.py
retag: env-TAG
	@echo Retagging version $(TAG) as $(PROJECT_VERSION)
	docker tag $(PROJECT):$(TAG) $(PROJECT):$(PROJECT_VERSION)

retag-run: ## Retags existing image in the registry with -run postfix
retag-run: ## Expecting BUILDTAG to match MAJOR.MINOR.PATCH-run<Anything> tag (filtered by .travis.yml pattern)
retag-run: env-DOCKER_REGISTRY_URL  env-NAMESPACE env-BUILDTAG
	$(eval DEPLOY_VERSION := $(shell echo $(BUILDTAG)|sed s/-run.*//g))
	@echo Retagging version $(DEPLOY_VERSION) as $(BUILDTAG)
	@docker pull $(DOCKER_REGISTRY_URL)/$(NAMESPACE)/$(PROJECT):$(DEPLOY_VERSION)
	docker tag $(DOCKER_REGISTRY_URL)/$(NAMESPACE)/$(PROJECT):$(DEPLOY_VERSION) $(DOCKER_REGISTRY_URL)/$(NAMESPACE)/$(PROJECT):$(BUILDTAG)
	docker push $(DOCKER_REGISTRY_URL)/$(NAMESPACE)/$(PROJECT):$(BUILDTAG)

checkout-deps: ### Checkouts scripts required for proper ci cd flow.
checkout-deps: env-GITHUB_TOKEN
	@git clone --branch=master https://$(GITHUB_TOKEN)@github.ibm.com/fd4b-agrotech/deployment-tools.git deployment-tools
	@cp -pr deployment-tools/* .
	@cp -pr deployment-tools/cicd/* ./cicd/
	@rm -rf deployment-tools

checkout-deps-local: CICD_DIR="../deployment-tools"
checkout-deps-local:
	@mkdir -p cicd
	@cp -pr $(CICD_DIR)/cicd/* ./cicd/
