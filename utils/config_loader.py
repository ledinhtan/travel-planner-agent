import yaml
from typing import Dict, Optional

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
    except FileNotFoundError:
        print(f"❌ Config file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        print(f"❌ Error parsing YAML: {e}")
        raise