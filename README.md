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

# Loading Data

First build the image
```
docker-compose build
```

Then start the containers
```
docker-compose up
```

## Create Tables

```
docker-compose exec web python manage.py create_db
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

## Check tables

Run `\l` inside of the psql CLI.

```
docker-compose exec db psql --username=hello_flask --dbname=hello_flask_dev
```

# Flask Backend

Once the web container is started navigate to `http://localhost:5001/` to see the hello world message.