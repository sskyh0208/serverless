NVM_DIR = /root/.nvm
CDK_PATH = /root/.nvm/versions/node/v22.8.0/bin/cdk
NODE_VERSION = v22.8.0

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

init-local-dynamodb:
	docker compose exec api bash -c "bash /scripts/init_local_dynamodb.sh"

cdk:
	docker compose exec cdk bash

# cdkコマンド
cdk-bootstrap-%:
	docker compose exec cdk /bin/bash -c "source $(NVM_DIR)/nvm.sh && nvm use $(NODE_VERSION) && $(CDK_PATH) bootstrap --all -c environment=$* --profile $*"
cdk-synth-%:
	docker compose exec cdk /bin/bash -c "source $(NVM_DIR)/nvm.sh && nvm use $(NODE_VERSION) && $(CDK_PATH) synth --all -c environment=$* --profile $*"
cdk-deploy-%:
	docker compose exec cdk /bin/bash -c "source $(NVM_DIR)/nvm.sh && nvm use $(NODE_VERSION) && $(CDK_PATH) deploy --all -c environment=$* --profile $*"
cdk-destroy-%:
	docker compose exec cdk /bin/bash -c "source $(NVM_DIR)/nvm.sh && nvm use $(NODE_VERSION) && $(CDK_PATH) destroy --all -c environment=$* --profile $*"

dev-deploy:
	@make cdk-bootstrap-dev
	@make cdk-synth-dev
	@make cdk-deploy-dev

dev-destroy:
	@make cdk-destroy-dev

stg-deploy:
	@make cdk-bootstrap-stg
	@make cdk-synth-stg
	@make cdk-deploy-stg

stg-destroy:
	@make cdk-destroy-stg