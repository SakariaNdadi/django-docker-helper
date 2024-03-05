# Django Docker

Django Docker is a Django package that simplifies the creation of Dockerfile and docker-compose.yml files for Django projects.

## Features

- Easily generate Dockerfile and docker-compose.yml files.
- Interactively configure Docker services.
- Seamlessly integrate Docker support into your Django projects.

### Current Services
- PostgeSQL
- MySQL
- Redis
- Rabbitmq
- Nginx

## Requirements
- Docker

## Installation

1. You can install Django Docker using pip:

```bash
pip install django-docker-helper
```

2. Add "django_docker_helper" to your installed apps

### Creating a Dockerfile

```bash
python manage.py docker_file generate
```

### Building the Dockerfile image

```bash
python manage.py docker_file build
```

### Creating a docker-compose.yml file

```bash
python manage.py docker_compose generate
```

### Building the docker-compose.yml image

```bash
python manage.py docker_compose up
```

or

```bash
python manage.py docker_compose up --build
```

to build Docker images before starting containers.

### Stopping and removing resources

```bash
python manage.py docker_compose down
```

or

```bash
python manage.py docker_compose down --remove-orphans
```

remove containers for services not defined in the Compose file


# Documentation and addition of more services underway.... 