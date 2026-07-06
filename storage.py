import json
import os


PROFILES_FILE = "profiles.json"


def load_profiles():
    if not os.path.exists(PROFILES_FILE):
        return []

    with open(PROFILES_FILE, "r") as file:
        return json.load(file)


def save_profiles(profiles):
    with open(PROFILES_FILE, "w") as file:
        json.dump(profiles, file, indent=4)