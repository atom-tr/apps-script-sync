from os import getenv, environ


class EnvironmentManager:
    """
    Class for handling all environmental variables used by the action.
    For all boolean variables a 'truthy'-list is checked (not only true/false, but also 1, t, y and yes are accepted).
    """

    _TRUTHY = ["true", "1", "t", "y", "yes"]

    GH_TOKEN = getenv("INPUT_GH_TOKEN")
    GITHUB_REPOSITORY = getenv("GITHUB_REPOSITORY")
    # Google Script
    PROJECT_ID = environ["INPUT_PROJECT_ID"]
    PROJECT_NAME = environ["INPUT_PROJECT_NAME"]
    PROJECT_PATH = environ["INPUT_PROJECT_PATH"]
    # Google app
    CLIENT_TYPE = environ["INPUT_CLIENT_TYPE"]
    CLIENT_ID = environ["INPUT_CLIENT_ID"]
    CLIENT_SECRET = environ["INPUT_CLIENT_SECRET"]
    REFRESH_TOKEN = environ["INPUT_REFRESH_TOKEN"]

    TIMEZONE = getenv("INPUT_TIMEZONE", "Asia/Ho_Chi_Minh")
