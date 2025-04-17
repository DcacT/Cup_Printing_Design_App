import os
import sys

def restart_app():
    """
    Callback function to restart the app.
    Closes the current instance and starts a new one.
    """
    python = sys.executable
    os.execl(python, python, *sys.argv)