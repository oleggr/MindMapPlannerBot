PROJECT_NAME ?= MindMapPlannerBot
PROJECT_NAMESPACE ?= oleggr
REGISTRY_IMAGE ?= $(PROJECT_NAMESPACE)/$(PROJECT_NAME)

all:
	@echo "make docker   - Run all docker containers"
	@echo "make down  	 - Run all docker containers"
	@echo "make bot  	 - Run bot locally"
	@exit 0

docker:
	docker-compose up -d --build

down:
	docker-compose down

bot:
	python3 bot.py
