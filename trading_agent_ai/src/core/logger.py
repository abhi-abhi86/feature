import logging
import logging.config
import os


def setup_logging(config_path='config/logging.ini', default_level=logging.INFO):
    """
    Setup logging configuration
    """
    if os.path.exists(config_path):
        logging.config.fileConfig(config_path)
    else:
        logging.basicConfig(level=default_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.warning(f"Logging config file not found at {config_path}. Using basic config.")
