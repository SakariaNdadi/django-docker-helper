from django.core.management.base import BaseCommand
import os
import subprocess
import argparse
from ..path import find_django_project_path
from ..docker_services import services


def generate_docker_compose_file(project_path):
    """
    Generates a docker-compose.yml file based on user input for configuring Docker services.

    Args:
        project_path (str): The path to the Django project directory.
    """

    docker_compose_content = """
version: "3.9"

services:
"""

    # Collect dependencies for the web service
    web_depends_on = []

    # Iterate over services and add them dynamically based on user input
    for service_name, service_config in services.items():
        try:
            while True:
                add_service = input(
                    f"Do you want to use {service_name.capitalize()}? (yes/no): "
                ).lower()

                if add_service in ["yes", "y"]:
                    # Add service definition with proper indentation
                    docker_compose_content += f"""
  {service_name}:
    image: {service_config['image']}
"""

                    # Add environment variables if they exist
                    if "environment" in service_config:
                        docker_compose_content += "    environment:\n"
                        for env_key, env_value in service_config["environment"].items():
                            # Proper indentation for environment variables
                            docker_compose_content += f"      - {env_key}={env_value}\n"

                    # Add ports if they exist
                    if "ports" in service_config:
                        docker_compose_content += "    ports:\n"
                        for port in service_config["ports"]:
                            # Proper indentation for ports
                            docker_compose_content += f"      - '{port}'\n"

                    # Add restart policy if it exists
                    if "restart" in service_config:
                        docker_compose_content += (
                            f"    restart: {service_config['restart']}\n"
                        )

                    # Collect dependencies for the web service
                    if service_name != "web":
                        depends_on_web = input(
                            f"Does your web service depend on {service_name}? (yes/no): "
                        ).lower()
                        if depends_on_web in ["yes", "y"]:
                            web_depends_on.append(service_name)

                    break
                elif add_service in ["no", "n"]:
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
                    continue

        except Exception as e:
            print(f"Error occurred: {e}")

    # Add web service definition with proper indentation
    docker_compose_content += """
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - '8000:8000'
"""

    # Add collected dependencies to the web service
    if web_depends_on:
        docker_compose_content += "    depends_on:\n"
        for dependency in web_depends_on:
            # Proper indentation for dependencies
            docker_compose_content += f"      - {dependency}\n"

    # Write to docker-compose.yml.temp file
    with open(
        os.path.join(project_path, "docker-compose.yml"), "w"
    ) as docker_compose_file:
        docker_compose_file.write(docker_compose_content.strip())


def build_docker_compose(project_path, build=False):
    """
    Builds the Docker Compose configuration.

    Args:
        project_path (str): The path to the Django project directory.
    """
    docker_compose_path = os.path.join(project_path, "docker-compose.yml")
    if os.path.exists(docker_compose_path):
        try:
            command = ["docker-compose", "up"]
            if build:
                command.append("--build")
            # subprocess.run(["docker-compose", "up"])
            subprocess.run(command)
        except subprocess.CalledProcessError as e:
            print(f"Error running docker-compose up: {e}")
    else:
        print("Dockerfile not found.")


def stop_and_remove_resources(project_path, remove_orphans=False):
    """
    Builds the Docker Compose configuration.

    Args:
        project_path (str): The path to the Django project directory.
    """
    docker_compose_path = os.path.join(project_path, "docker-compose.yml")
    if os.path.exists(docker_compose_path):
        try:
            command = ["docker-compose", "down"]
            if remove_orphans:
                command.append("--remove-orphans")
            subprocess.run(command)
        except subprocess.CalledProcessError as e:
            print(f"Error running docker-compose down: {e}")
    else:
        print("Dockerfile not found.")


class Command(BaseCommand):
    """
    Command to manage Docker Compose configuration for a Django project.
    """

    help = "Create docker-compose.yml"

    def add_arguments(self, parser):
        """
        Adds command line arguments for the manage.py command.

        Args:
            parser: Argument parser instance.
        """
        # Define the command-line arguments
        parser.add_argument(
            "action",
            choices=["generate", "up", "down"],
            help="Action to perform: generate a docker-compose file, start containers, or stop containers.",
        )
        parser.add_argument(
            "--build",
            action="store_true",
            help="Build Docker images before starting containers.",
        )
        parser.add_argument(
            "--remove-orphans",
            action="store_true",
            help="Remove containers for services not defined in the Compose file",
        )

    def handle(self, *args, **options):
        """
        Handles the execution of the manage.py command.

        Args:
            *args: Additional command arguments.
            **options: Additional options.
        """
        action = options["action"]
        project_path = find_django_project_path()

        if project_path:
            dockerfile_path = os.path.join(project_path, "Dockerfile")
            compose_file_path = os.path.join(project_path, "docker-compose.yml")

            if action == "generate":
                if not os.path.exists(dockerfile_path):
                    self.stdout.write(
                        self.style.ERROR(
                            "Dockerfile not found. Please create the Dockerfile first.'python manage.py docker_file generate'"
                        )
                    )
                else:
                    if os.path.exists(compose_file_path):
                        user_input = input(
                            "A docker-compose.yml already exists. Do you want to overwrite it? (yes/no):"
                        )
                        if user_input in ["yes", "y"]:
                            generate_docker_compose_file(project_path)
                            self.stdout.write(
                                self.style.SUCCESS(
                                    "docker-compose.yml successfully overwritten."
                                )
                            )
                        else:
                            pass
                    else:
                        try:
                            generate_docker_compose_file(project_path)
                            self.stdout.write(
                                self.style.SUCCESS(
                                    "Successfully created docker-compose.yml"
                                )
                            )
                        except Exception as e:
                            self.stderr.write(
                                f"Failed to create docker-compose.yml: {e}"
                            )

            elif action == "up":
                if not os.path.exists(dockerfile_path):
                    self.stdout.write(
                        self.style.ERROR(
                            "Dockerfile not found. Please create the Dockerfile first.'python manage.py docker_file generate'"
                        )
                    )
                try:
                    if not os.path.exists(compose_file_path):
                        self.stdout.write(
                            self.style.ERROR(
                                "docker-compose.yml file not found. Please create the docker-compose.yml first.'python manage.py docker_compose generate'"
                            )
                        )
                    else:
                        build = options.get("build", False)
                        build_docker_compose(project_path, build)
                except Exception as e:
                    self.stderr.write(f"Failed to build docker-compose: {e}")

            elif action == "down":
                try:
                    if os.path.exists(compose_file_path):
                        remove_orphans = options.get("remove_orphans", False)
                        stop_and_remove_resources(project_path, remove_orphans)
                except Exception as e:
                    self.stderr.write(f"Failed to stop and remove resources: {e}")

        else:
            self.stderr.write("Django project path not found.")
