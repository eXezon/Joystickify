import yaml
import logging
from pynput.keyboard import Key, KeyCode

def load_config(config_file='config.yaml'):
    """
    Load configuration from a YAML file.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        dict: Configuration parameters.
    """
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

def get_hotkey(key_str):
    """
    Convert a string representation of a key to a pynput Key or KeyCode.

    Args:
        key_str (str): String representation of the key.

    Returns:
        Key or KeyCode: Corresponding pynput key object.
    """
    key_mappings = {
        'F1': Key.f1,
        'F2': Key.f2,
        'F3': Key.f3,
        'F4': Key.f4,
        'F5': Key.f5,
        'F6': Key.f6,
        'F7': Key.f7,
        'F8': Key.f8,
        'F9': Key.f9,
        'F10': Key.f10,
        'F11': Key.f11,
        'F12': Key.f12,
        'esc': Key.esc,
        'tab': Key.tab,
        'shift': Key.shift,
        'ctrl': Key.ctrl,
        'alt': Key.alt,
        'space': Key.space,
    }

    key_str = key_str.strip().upper()
    if key_str in key_mappings:
        return key_mappings[key_str]
    elif len(key_str) == 1:
        return KeyCode(char=key_str)
    else:
        raise ValueError(f"Unsupported hotkey: {key_str}")

def setup_logging(enabled, level):
    """
    Set up logging configuration.

    Args:
        enabled (bool): Enable or disable logging.
        level (str): Logging level.
    """
    if not enabled:
        logging.disable(logging.CRITICAL)
        return

    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid logging level: {level}")

    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )