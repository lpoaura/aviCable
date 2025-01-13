run:
	docker compose -f docker-compose.yml -f docker-compose.debug.yml up --build


docker_graphviz:
	docker compose -f docker-compose.yml -f docker-compose.debug.yml up --build alpha viz --networks --ports | dot -Tsvg > docker_model.svg


build-docs:
	cd docs && poetry run make html

graph-models:
	cd backend && poetry run python -m manage graph_models -g --language fr --output ../database_model.png  cables commons custom_content geo_area map_layers media mortality species users

docs: build-docs graph-models

# backend-requirements:
# 	cd backend && \
# 	poetry export --without-hashes --format requirements.txt -o requirements.txt && \
# 	poetry export --without-hashes --with=dev --format requirements.txt -o requirements-dev.txt
