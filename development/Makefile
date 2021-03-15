##########################################################################
# This is the development environment's Makefile.
##########################################################################

##########################################################################
# VARIABLES
##########################################################################

PWD = $(shell pwd)
HOME := $(shell echo ~)
POSTGRES_DIR = $(shell pwd)/postgres
POSTGRES_DATA_DIR = $(shell pwd)/postgres/data

# Load from env file
include env
export $(shell sed 's/=.*//' env)

##########################################################################
# MENU
##########################################################################

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

################################################################################
# DATABASE
################################################################################

.PHONY: postgres-stop
postgres-stop:: ##@postgres	stop postgres
	@docker container stop ddd-postgres || true
	@docker container rm ddd-postgres || true

.PHONY: postgres-deploy
postgres-deploy:: postgres-stop ##@postgres	deploy postgres
	@docker run \
		--restart unless-stopped \
		--name ddd-postgres \
		--network $(NETWORK) \
		--log-opt max-size=$(LOGS_MAX_SIZE) \
		--log-opt max-file=$(LOGS_MAX_FILE) \
		-p "5434:5432" \
		-e "POSTGRES_PASSWORD=$(POSTGRES_PASSWORD)" \
		-v $(POSTGRES_DATA_DIR):/var/lib/postgresql/data \
		-v $(POSTGRES_DIR)/postgresql.conf:/etc/postgresql/postgresql.conf \
		-d \
			postgres:10 -c 'config_file=/etc/postgresql/postgresql.conf'

.PHONY: postgres-setup
postgres-setup:: ##@postgres	setup the database (for tests)
	docker exec -t ddd-postgres psql -U postgres -c <<< echo "create database test;"
	docker exec -t ddd-postgres psql -U postgres -c <<< echo "create user test with encrypted password '$(POSTGRES_TEST_PASSWORD)';"
	docker exec -t ddd-postgres psql -U postgres -c <<< echo "grant all privileges on database test to test;"
