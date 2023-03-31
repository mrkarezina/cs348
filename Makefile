default: help

.PHONY: help
help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: setup
setup: # run all commands to initialize and populate the database
	make create-all-tables
	make populate-all-tables

.PHONY: create-all-tables
create-all-tables: # creates all tables in the database
	docker-compose exec web python manage.py create_static_tables
	docker-compose exec web python manage.py create_stat_tables
	docker-compose exec web python manage.py create_recent_stat_tables

.PHONY: populate-all-tables
populate-all-tables: # populates all tables in the database (requires tables to be created)
	docker-compose exec web python manage.py populate_static_tables
	docker-compose exec web python manage.py populate_stat_tables
	docker-compose exec web python manage.py populate_recent_stat_tables

.PHONY: update
update: # updates stat tables with new data from the raw_data folder
	docker-compose exec web python manage.py create_stat_tables
	docker-compose exec web python manage.py create_recent_stat_tables
	docker-compose exec web python manage.py populate_stat_tables
	docker-compose exec web python manage.py populate_recent_stat_tables

