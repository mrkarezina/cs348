# CS 348 Project

## Database Information

- [PostgreSQL](https://www.postgresql.org/download/)

### Loading the dataset

```sh
python[3] db_cli.py
Database Commands:
init_db
population <country>
> init_db
> population canada
('Canada', 'canada', 38232593, '2022 est.', 38, 'North America')
> q
```

# Building Project

First build the image
```
docker-compose build
```

Then start the containers
```
docker-compose up
```

## Load Data

### Create tables
```
docker-compose exec web python manage.py create_db
```

### Load CSV

See [format script](csv_format_utilities/README.md) for how `formatted_data` folder was created.

```
docker-compose exec web python manage.py populate_db
```

### Check tables

Run `\c world_factbook`, followed by `\dt` inside of the psql CLI.

```
docker-compose exec db psql --username=user --dbname=world_factbook
```

Run the following SQL command to check if the data inside the population table was loaded successfully.
```
TABLE population;
```

### Debugging

Open a shell, make sure you ran `docker compose up` first.
```
docker-compose exec web sh
```

Run script
```
python manage.py create_db
```

# Flask Backend

Once the web container is started navigate to `http://localhost:5001/` to see the hello world message.
