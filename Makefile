DOCKER_REGISTRY := placeholder.github.com
DOCKER_IMAGE_TAG := latest
DOCKER_IMAGE_PATH := tattle-tale:$(DOCKER_IMAGE_TAG)
DOCKER_SAVE_FILE := tattle-tale-$(DOCKER_IMAGE_TAG)

docker-build:
	docker build -t $(DOCKER_REGISTRY)/$(DOCKER_IMAGE_PATH) .

docker-push:
	docker login $(DOCKER_REGISTRY)
	docker push $(DOCKER_REGISTRY)/$(DOCKER_IMAGE_PATH)

docker-save:
	docker save $(DOCKER_REGISTRY)/$(DOCKER_IMAGE_PATH) | gzip > $(DOCKER_SAVE_FILE).gz

