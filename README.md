# fixxx-omslagroute

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

To rebuild (for example, when dependencies are added requirements.txt):
```bash
docker-compose build
```

Start watching static files changes scss:

```bash
docker-compose exec web ./node_modules/.bin/node-sass -o ./assets/bundles/ static_src/sass --watch
```

Migrate database without restarting containers:

```bash
docker-compose exec web python manage.py migrate
``` 