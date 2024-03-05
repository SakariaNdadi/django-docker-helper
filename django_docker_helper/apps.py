from django.apps import AppConfig


class DockerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_docker_helper'
    label = "docker"
