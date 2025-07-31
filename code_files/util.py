import os
import sys

def resource_path(relative_path):
    """
    Function to get the absolute path to the images/sounds for PyInstaller to use
    :param relative_path: the relative path of the resource
    :return: the absolute path of the resource
    """
    try:
        # PyInstaller temporary folder
        base_path = sys._MEIPASS
    # # In cases where the .py file is run instead of the app (_MEIPASS doesn't exist)
    except AttributeError:
        # Sets the base_path to the current working directory
        base_path = os.path.abspath(".")
    # The absolute path of the resource passed in is returned
    # Combine base path with relative_path
    return os.path.join(base_path, relative_path)