from django.core.management.base import BaseCommand
import os
import subprocess
from ..path import find_django_project_path


def generate_dockerfile(project_path):
    """
    Generates a Dockerfile in the given project path.

    Args:
        project_path (str): The path to the Django project.

    Returns:
        None
    """
    if not project_path:
        print("Django project path not found.")
        return

    # Dockerfile content template
    dockerfile_content = f"""
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into container
COPY . /code/
"""

    # Write Dockerfile content to file
    with open(os.path.join(project_path, "Dockerfile"), "w") as dockerfile:
        dockerfile.write(dockerfile_content.strip())


def build_docker_image(project_path):
    """
    Builds the Docker image using the Dockerfile in the project path.

    Args:
        project_path (str): The path to the Django project.

    Returns:
        None
    """
    dockerfile_path = os.path.join(project_path, "Dockerfile")
    if os.path.exists(dockerfile_path):
        try:
            # Build Docker image using Dockerfile
            subprocess.run(["docker", "build", project_path])
        except subprocess.CalledProcessError as e:
            print(f"Error building Docker image: {e}")
    else:
        print("Dockerfile not found.")


def is_docker_running():
    """
    Checks if Docker is running.

    Returns:
        bool: True if Docker is running, False otherwise.
    """
    try:
        # Check if Docker daemon is running
        subprocess.run(
            ["docker", "info"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except subprocess.CalledProcessError:
        return False


class Command(BaseCommand):
    """
    Management command to generate and build Dockerfile for Django project.
    """

    help = "Create Dockerfile"

    def add_arguments(self, parser):
        """
        Adds command line arguments.

        Args:
            parser: The ArgumentParser instance.

        Returns:
            None
        """
        parser.add_argument("action", choices=["generate", "g", "build", "b"])

    def handle(self, *args, **options):
        """
        Handles the command execution.

        Args:
            *args: Additional positional arguments.
            **options: Additional keyword arguments.

        Returns:
            None
        """
        action = options["action"]
        project_path = find_django_project_path()
        if project_path:
            if action in ["generate", "g"]:
                try:
                    if os.path.exists(os.path.join(project_path, "Dockerfile")):
                        # Prompt user to confirm overwriting existing Dockerfile
                        user_input = input(
                            "A Dockerfile already exists. Do you want to overwrite it? (yes/no):"
                        )
                        if user_input in ["yes", "y"]:
                            generate_dockerfile(project_path)
                            self.stdout.write(
                                self.style.SUCCESS(
                                    "Dockerfile successfully overwritten."
                                )
                            )
                        else:
                            pass
                    else:
                        # Generate Dockerfile if not exists
                        generate_dockerfile(project_path)
                        self.stdout.write(
                            self.style.SUCCESS(
                                "Dockerfile successfully generated. Check your root directory"
                            )
                        )
                except Exception as e:
                    self.stderr.write(f"Failed to create Dockerfile: {e}")

            if action in ["build", "b"]:
                try:
                    if not os.path.exists(os.path.join(project_path, "Dockerfile")):
                        # If Dockerfile does not exist, prompt user to generate it
                        self.stdout.write(
                            self.style.ERROR(
                                "Dockerfile missing. Generate a Dockerfile using this command 'python manage.py docker_file generate' "
                            )
                        )
                    elif not os.path.exists(os.path.join(project_path, "requirements.txt")):
                        self.stdout.write(self.style.ERROR("requirements.txt file is missing. Generate a requirements.txt using this command 'pip freeze > requirements.txt'."))
                    else:
                        if is_docker_running():
                            # Build Docker image if Docker daemon is running
                            build_docker_image(project_path)
                            self.stdout.write(
                                self.style.SUCCESS(
                                    "***********Image Built*****************"
                                )
                            )
                        else:
                            self.stderr.write(
                                self.style.ERROR(
                                    "Start Docker daemon before building the image."
                                )
                            )
                except Exception as e:
                    self.stderr.write(
                        f"Failed to create Dockerfile and build Docker image: {e}"
                    )
        else:
            self.stderr.write("Django project path not found.")
