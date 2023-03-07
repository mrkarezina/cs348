# CS 348 Project

## Description


## Building the Project
Build all images and start containers:
```
docker-compose up
```


## Initializing the Database

### Database Information
- [PostgreSQL](https://www.postgresql.org/download/)

### Create tables
```
docker-compose exec web python manage.py create_db
```

### Load CSV

See [format script](csv_format_utilities/README.md) for how `formatted_data` folder was created.

```
docker-compose exec web python manage.py populate_db
```

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

### Interacting with the PostgreSQL Database
Once the project is up and running within its container, run the following command to access the PostgreSQL CLI.
```
docker-compose exec db psql --username=user --dbname=world_factbook
```


To view tables in the database, use 
```
\dt
```

Run the following SQL command to check if the data inside the population table was loaded successfully.
```
TABLE population;
```



## Debugging
(once the project is up and running within its container)

Access the WEB service using:
```
docker-compose exec web sh
```

Access the DB service using:
```
docker-compose exec db sh
```

Run script
```
python manage.py create_db
```


## Flask Backend
Once the web container is started navigate to `http://localhost:5001/` to see the hello world message.
