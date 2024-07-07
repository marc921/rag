include .env
export

.PHONY: build
build:
	docker build -t $(COMPONENT) -f images/$(COMPONENT).dockerfile .
	docker tag $(COMPONENT) $(DOCKER_USER)/$(COMPONENT):latest
	@docker login -u $(DOCKER_USER) -p "$(DOCKER_PASS)"
	docker push $(DOCKER_USER)/$(COMPONENT):latest

.PHONY: k8s-up
k8s-up:
	minikube status 2>/dev/null | grep -q Running || minikube start

.PHONY: k8s-down
k8s-down:
	kubectl delete all --all
	minikube stop

.PHONY: docker-up
docker-up:
	open -a Docker

.PHONY: helm-apply
helm-apply:
	@helm upgrade --install $(RELEASE) ./helmchart \
		--set postgres.password=$(PG_PASSWORD) \
		--set scaleway.model_url=$(MODEL_URL) \
		--set scaleway.secret_key=$(SCALEWAY_SECRET_KEY)
		--set api.auth_secret=$(AUTH_SECRET)


.PHONY: all
all:
	make k8s-up
	make build COMPONENT=api
	make helm-apply RELEASE=release
	kubectl rollout restart deployment api-deployment