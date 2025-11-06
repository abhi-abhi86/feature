import logging
import logging.config
from pathlib import Path


def setup_logging(config_path: str):
    """
    Sets up logging for the entire application using the provided config file.
    """
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Logging config file not found: {config_file}")

    logging.config.fileConfig(config_file)
    logger = logging.getLogger(__name__)
    logger.info("Logging setup completed.")
