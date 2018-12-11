# currencyapp
API to get currency quotes information from https://hgbrasil.com/status/finance/

To get it running locally you need **Docker** and **docker-compose** installed.

https://docs.docker.com/install/

https://docs.docker.com/compose/install/

Then in the terminal simply run:

`docker-compose up`

The Dockerfile comes with a *cron* that request data of currency quotations each hour, then call this project's Django API to save data at the database.

You can run tests accessing the web container and running the django test command:

```
docker-compose run web bash
python manage.py test
```

The default port is set to 8000.
