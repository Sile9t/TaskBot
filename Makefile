run:
	docker run -it -d --env-file .env --restart=unless-stopped --name tiar_smm_bot tiar_smm_bot_image
stop:
	docker stop tiar_smm_bot
attach:
	docker attach tiar_smm_bot
dell:
	docker rm tiar_smm_bot