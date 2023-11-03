# コンテナを立ち上げる
up:
	docker compose up

# コンテナを削除する
down:
	docker compose down

# apiコンテナ内に入る
bash:
	docker compose exec api bash


build:
	docker compose build