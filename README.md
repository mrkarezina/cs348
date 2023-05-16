# The Country Factbook

## Description
A world stats interface that allows you to learn about different countries and play games.
![image](https://user-images.githubusercontent.com/57971748/228081489-cbc4c5d8-fc1b-4e13-836f-f0b24f7e075d.png)


## Running the application

```
docker-compose up
```

This command will build the docker images, start the db and web containers, and seed the database.

The first time the containers are built, the database is completely empty. A script will automatically detect if the tables are empty and seed them with the world statistics. If the tables already exist and are populated this initialization step will be skipped.

Database Information
- [PostgreSQL](https://www.postgresql.org/download/)
- View sample queries and outputs [here](https://github.com/mrkarezina/cs348/tree/main/test)

Once the container has been build and the database populate navigate to `http://localhost:5001/` to interact with the web app.

## Updating the Country Statistics
This factbook has the unique feature of supporting a timeseries data from multiple years. To update the database with new data, first insert this new data into the appropriate CSV file in the `raw_data` folder, make sure to follow the existing format. Then, with the web app up and running, simply open a terminal and run the command:
```
docker-compose exec web python manage.py update
```

# Debugging

## Frontend
Starting the app locally:
1. Ensure the workign dir is the frontend ; `cd frontend`
2. Install dependencies ; `yarn`
3. Start the frontend ; `yarn dev`

Library Documentation Links

- [React Simple Maps](https://www.react-simple-maps.io/)
- [React Tooltip](https://react-tooltip.com/)
- [Mantine documentation](https://mantine.dev/)
- [Vite documentation](https://vitejs.dev/)

________________________________________________

## Backend
(once the project is up and running within its container)

### Web
Access the WEB service using:
```
docker-compose exec web sh
```

### PostgreSQL
Access the DB service using:
```
docker-compose exec db sh
```

Interacting with the PostgreSQL Database:

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
