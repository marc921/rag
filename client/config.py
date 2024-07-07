from dataclasses import dataclass
import configparser
from getpass import getpass

CONFIG_FILE = "client/client.ini"

@dataclass
class Credentials:
    username: str
    password: str
    access_token: str
    
def save(creds: Credentials) -> None:
    """Saves the credentials to the config file."""
    config = configparser.ConfigParser()
    config["Credentials"] = {
        "username": creds.username,
        "password": creds.password,
        "access_token": creds.access_token,
    }

    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)


def load() -> Credentials:
    """Loads the credentials from the config file."""
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    try:
        username = config["Credentials"]["username"]
        password = config["Credentials"]["password"]
        access_token = config["Credentials"]["access_token"]
    except KeyError:
        username = None
        password = None
        access_token = None
    if not username or not password:
        username = input("Enter your username: ")
        password = getpass("Enter your password: ")
    return Credentials(
        username=username,
        password=password,
        access_token=access_token,
    )