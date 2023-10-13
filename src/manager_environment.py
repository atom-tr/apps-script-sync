from os import getenv, environ


class EnvironmentManager:
    """
    Class for handling all environmental variables used by the action.
    For all boolean variables a 'truthy'-list is checked (not only true/false, but also 1, t, y and yes are accepted).
    """

    _TRUTHY = ["true", "1", "t", "y", "yes"]

	# Google Script
    PROJECT_ID = environ["PROJECT_ID"]
    PROJECT_NAME = environ["PROJECT_NAME"]
    PROJECT_PATH = environ["PROJECT_PATH"]
    # Google app
    CLIENT_TYPE = environ["CLIENT_TYPE"]
    CLIENT_ID = environ["CLIENT_ID"]
    CLIENT_SECRET = environ["CLIENT_SECRET"]
    REFRESH_TOKEN = environ["REFRESH_TOKEN"]

    TimeZone = getenv("TimeZone", "Asia/Ho_Chi_Minh")
    
    