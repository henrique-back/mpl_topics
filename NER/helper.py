import configparser
from pathlib import Path

CONFIG_PATH = Path(__file__).with_name('configurations.ini')


# Method to read config file settings (configurations.ini next to this file, not version controlled).
# See configurations.ini.example for the expected format.
def read_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"{CONFIG_PATH} not found; copy configurations.ini.example and fill it in.")
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config
