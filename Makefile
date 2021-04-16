ENV ?= dev

.PHONY: carlaviz-docker-build
carlaviz-docker-build:
	docker build \
		-t carlaviz \
		-f docker/Dockerfile \
		.

.PHONY: carlaviz-docker-run
carlaviz-docker-run:
	docker run \
		-it \
		--rm \
		--name carlaviz \
		-e CARLAVIZ_HOST_IP=localhost \
		-e CARLA_SERVER_IP=host.docker.internal \
		-e CARLA_SERVER_PORT=2000 \
		-p 8080-8081:8080-8081 \
		-p 8089:8089 \
		carlaviz

.PHONY: carlaviz
carlaviz: carlaviz-docker-build carlaviz-docker-run

.PHONY: carlaviz-backend-input
carlaviz-backend-input:
	docker build \
		-t carlaviz-backend-input \
		backend_input
	docker run \
		-it \
		--rm \
		--name carlaviz-backend-input-$(ENV)  \
		-e SERVER_IP=0.0.0.0 \
		-e SERVER_PORT=13254 \
		-e CARLA_SERVER_IP=host.docker.internal \
		-e CARLA_SERVER_PORT=2000 \
		-p 13254:13254 \
		carlaviz-backend-input
