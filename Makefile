bash:
	docker-compose run deb /bin/bash

build:
	docker-compose build

test:
	SMILExtract -h

launch:
	make build && make bash

edit_dockerfile:
	vim Dockerfile

edit_compose:
	vim docker-compose.yml
