import os


def find_django_project_path():
    """
    Finds the Django project path containing manage.py file.
    Returns the project path or None if not found.
    """
    current_path = os.getcwd()  # Get the current working directory
    while not os.path.exists(os.path.join(current_path, "manage.py")):
        # Move up one directory until 'manage.py' is found or until the root directory is reached
        current_path = os.path.dirname(current_path)
        if current_path == os.path.dirname(current_path):  # Reached the root directory
            return None
    return current_path
