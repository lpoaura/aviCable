docker_graphviz:
	docker compose -f docker-compose.yml -f docker-compose.production.yml alpha viz --networks --ports | dot -Tsvg > docker_model.svg


backend-requirements:
	cd backend && \
	poetry export --without-hashes --format requirements.txt -o requirements.txt && \
	poetry export --without-hashes --with=dev --format requirements.txt -o requirements-dev.txt
