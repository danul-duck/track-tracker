imageName := trackmania-tracker
version ?= 3.2.2
build-image:
	docker build -t $(imageName):$(version) .

package: 
	 python -m build --wheel

run: 
	docker run \
		-v data:/opt/trackmania-tracker/data \
		-p 8080:8080 \
		-e TRACK_PASSWORD="" \
		-e TRACK_USERNAME="" \
		$(imageName):$(version)

local-run:
	python3 -m flask run

save-image: 
	docker save -o images/$(imageName):$(version).tar $(imageName):$(version)
