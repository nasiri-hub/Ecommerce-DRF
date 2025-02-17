build:
	docker compose up --build --remove-orphans api
logs:
	docker compose logs
down:
	docker compose down -v
bash:
	docker compose exec -it api bash 