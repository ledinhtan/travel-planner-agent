import sys
import yaml
from typing import Dict, Optional
from exception.exceptionhandling import CustomException
from logger.logging import logging

logger = logging.getLogger(__name__)

def load_config(config_path: str = "config/config.yml") -> Optional[Dict]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to the YAML configuration file
    
    Returns:
        Dictionary containing configuration, or None if error
    
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If YAML parsing fails
    """
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        custom_error = CustomException(e, sys)
        logger.error(custom_error)
        raise custom_error  