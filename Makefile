build:
	docker build -t region_task_bot_image .
run:
	docker run -it -d --env-file .env --restart=unless-stopped --name region_task_bot region_task_bot_image
stop:
	docker stop region_task_bot
attach:
	docker attach region_task_bot
dell:
	docker rm region_task_bot