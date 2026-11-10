# settings_file.py - load settings from a file, safely, and save them again
import json
import os

SETTINGS_FILE = "rover_settings.json"
DEFAULTS = {"max_speed_ms": 0.5, "gain": 1.0, "wheel_diameter_m": 0.065}


def load_settings(path):
    """Return the settings. Anything missing or damaged falls back to DEFAULTS."""
    settings = DEFAULTS.copy()
    try:
        with open(path) as f:
            settings.update(json.load(f))      # values from the file replace defaults
    except FileNotFoundError:
        print("no settings file: using defaults")
    except json.JSONDecodeError as error:
        print("settings file is damaged:", error)
    return settings


def save_settings(path, settings):
    """Write to a temporary file first, so a power cut cannot ruin the real one."""
    temp_path = path + ".tmp"
    with open(temp_path, "w") as f:
        json.dump(settings, f, indent=2)
    os.replace(temp_path, path)                # one step: old file or new file, never half


settings = load_settings(SETTINGS_FILE)
print("loaded:", settings)

settings["wheel_diameter_m"] = 0.06589         # the Chapter 16 calibration
save_settings(SETTINGS_FILE, settings)

print("again: ", load_settings(SETTINGS_FILE))
