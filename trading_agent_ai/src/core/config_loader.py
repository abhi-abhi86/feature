import configparser
import json
import os
from pathlib import Path


class ConfigLoader:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.main_config = configparser.ConfigParser()
        self.logging_config = configparser.ConfigParser()
        self.prompts = {}

        self._load_main_config()
        self._load_logging_config()
        self._load_prompts()

    def _load_main_config(self):
        config_path = self.config_dir / "main_config.ini"
        if config_path.exists():
            self.main_config.read(config_path)
        else:
            raise FileNotFoundError(f"Main config file not found: {config_path}")

    def _load_logging_config(self):
        logging_path = self.config_dir / "logging.ini"
        if logging_path.exists():
            self.logging_config.read(logging_path)
        else:
            raise FileNotFoundError(f"Logging config file not found: {logging_path}")

    def _load_prompts(self):
        prompts_path = self.config_dir / "prompts.json"
        if prompts_path.exists():
            with open(prompts_path, 'r') as f:
                self.prompts = json.load(f)
        else:
            # Default empty prompts if file not found
            self.prompts = {}

    def get_main_config(self, section: str, key: str, fallback=None):
        return self.main_config.get(section, key, fallback=fallback)

    def get_logging_config(self):
        return self.logging_config

    def get_prompt(self, key: str, fallback=None):
        return self.prompts.get(key, fallback)
