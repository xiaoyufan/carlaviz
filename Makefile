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

.PHONY: carlaviz-dev
carlaviz-dev: carlaviz-docker-build carlaviz-docker-run

.PHONY: carlaviz-backend-input-dev
carlaviz-backend-input-dev:
	docker build \
		-t carlaviz-backend-input \
		--target dev \
		backend_input
	docker run \
		-it \
		--rm \
		--name carlaviz-backend-input  \
		-p 13254:13254 \
		carlaviz-backend-input