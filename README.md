# CS 348 Project

## Description
A world stats interface that allows you to learn about different countries and play games.

## Frontend
## Start the app
1. Ensure the workign dir is the frontend ; `cd frontend`
2. Install dependencies ; `yarn`
3. Start the frontend ; `yarn dev`

### Library Documentation Links

- [React Simple Maps](https://www.react-simple-maps.io/)
- [React Tooltip](https://react-tooltip.com/)
- [Mantine documentation](https://mantine.dev/)
- [Vite documentation](https://vitejs.dev/)


## Backend
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
```
docker-compose exec web python manage.py populate_db
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