#!/usr/bin/env python3
"""
Secrets and Configuration Loader
Loads secrets from .secrets/secrets.json and configuration from config/config.ini
"""

import json
import os
import sys
from configparser import ConfigParser
from pathlib import Path


class SecretsManager:
    """Manages secrets loading from JSON file"""
    
    def __init__(self, secrets_path=None):
        if secrets_path is None:
            # Get the project root
            project_root = Path(__file__).parent.parent
            secrets_path = project_root / ".secrets" / "secrets.json"
        
        self.secrets_path = Path(secrets_path)
        self.secrets = self._load_secrets()
    
    def _load_secrets(self):
        """Load secrets from JSON file"""
        if not self.secrets_path.exists():
            raise FileNotFoundError(
                f"Secrets file not found at {self.secrets_path}\n"
                f"Please create it from the template: .secrets/secrets.template.json"
            )
        
        try:
            with open(self.secrets_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in secrets file: {e}")
    
    def get(self, key_path, default=None):
        """
        Get a secret value using dot notation
        Example: get("naukri.username") returns secrets['naukri']['username']
        """
        keys = key_path.split('.')
        value = self.secrets
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            if default is not None:
                return default
            raise KeyError(f"Secret key not found: {key_path}")
    
    def get_all(self):
        """Get all secrets"""
        return self.secrets


class ConfigManager:
    """Manages configuration loading from INI file"""
    
    def __init__(self, config_path=None):
        if config_path is None:
            # Get the project root
            project_root = Path(__file__).parent.parent
            config_path = project_root / "config" / "config.ini"
        
        self.config_path = Path(config_path)
        self.config = ConfigParser()
        self._load_config()
    
    def _load_config(self):
        """Load configuration from INI file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found at {self.config_path}")
        
        self.config.read(self.config_path)
    
    def get(self, section, key, default=None, var_type=str):
        """
        Get a configuration value
        var_type can be: str, int, float, bool
        """
        try:
            if var_type == bool:
                return self.config.getboolean(section, key)
            elif var_type == int:
                return self.config.getint(section, key)
            elif var_type == float:
                return self.config.getfloat(section, key)
            else:
                return self.config.get(section, key)
        except:
            if default is not None:
                return default
            raise KeyError(f"Config key not found: {section}.{key}")
    
    def get_all(self, section):
        """Get all keys in a section as dictionary"""
        return dict(self.config.items(section))


# Convenience functions
_secrets = None
_config = None


def get_secrets():
    """Get or create the secrets manager"""
    global _secrets
    if _secrets is None:
        _secrets = SecretsManager()
    return _secrets


def get_config():
    """Get or create the config manager"""
    global _config
    if _config is None:
        _config = ConfigManager()
    return _config


def get_secret(key_path, default=None):
    """Convenience function to get a secret"""
    return get_secrets().get(key_path, default)


def get_config_value(section, key, default=None, var_type=str):
    """Convenience function to get a config value"""
    return get_config().get(section, key, default, var_type)


if __name__ == "__main__":
    # Test the loaders
    print("Testing Secrets Manager...")
    try:
        secrets = get_secrets()
        print(f"✓ Username: {secrets.get('naukri.username')}")
        print(f"✓ Mobile: {secrets.get('naukri.mobile')}")
        print(f"✓ Original Resume: {secrets.get('paths.original_resume')}")
    except Exception as e:
        print(f"✗ Error loading secrets: {e}")
    
    print("\nTesting Config Manager...")
    try:
        config = get_config()
        print(f"✓ Login URL: {config.get('URLs', 'NAUKRI_LOGIN_URL')}")
        print(f"✓ Headless Mode: {config.get('Settings', 'HEADLESS', var_type=bool)}")
        print(f"✓ Schedule Interval: {config.get('Scheduling', 'SCHEDULE_INTERVAL_HOURS', var_type=int)} hours")
    except Exception as e:
        print(f"✗ Error loading config: {e}")
