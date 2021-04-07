.PHONY: docker-build
docker-build:
	docker build -t carlaviz -f docker/Dockerfile .

.PHONY: docker-run
docker-run:
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