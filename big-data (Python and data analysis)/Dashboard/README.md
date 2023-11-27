# How to run the application

```
docker-compose up -d
```

# How to stop the application

```
docker-compose down
```

# changed the packages in requirements.txt?
When change are made in de requirements.txt we need to rebuild the docker container

First we need to stop the current docker image:
```
docker-compose down -v
```

Then we can rebuild the docker image:
```
docker-compose build
```

After that we can run the application again:
```
docker-compose up -d
```