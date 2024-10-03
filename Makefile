build:
	docker compose build
rebuild:
	docker compose up -d --build
up:
	docker compose up -d
down:
	docker compose down
destroy:
	docker compose down --rmi all --volumes --remove-orphans
logs:
	docker compose logs -f
ls:
	docker compose ls

# コンテナに入るコマンド
client:
	docker compose exec client bash
api:
	docker compose exec api bash
sam:
	docker compose exec sam bash

init-local-dynamodb:
	docker compose exec api bash -c "bash /scripts/init_local_dynamodb.sh"