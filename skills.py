import json
from utils import title


SKILLS_FILE = "skills_database.json"


def load_skills_database():
    try:
        with open(SKILLS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def skills_gap_analyzer():
    skills_database = load_skills_database()

    role = input("\nTarget role: ").strip().lower()
    skills = skills_database.get(role)

    print()
    title("SKILLS REPORT")
    print(f"Target role: {role.title()}\n")

    if skills:
        print("Recommended skills:")

        for skill in skills:
            print(f"- {skill}")
    else:
        
        print("Role not found in database.")