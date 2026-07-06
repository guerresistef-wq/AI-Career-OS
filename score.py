from storage import load_profiles
from utils import title


def calculate_score(profile):

    score = 0

    experience = profile["experience"]
    salary = profile["salary"]

    if experience >= 10:
        score += 40
    elif experience >= 5:
        score += 30
    elif experience >= 2:
        score += 20
    else:
        score += 10

    if salary >= 5000:
        score += 30
    elif salary >= 3500:
        score += 25
    elif salary >= 2000:
        score += 20
    else:
        score += 10

    score += 30

    return score


def show_scores():

    profiles = load_profiles()

    title("CAREER SCORES")

    if len(profiles) == 0:
        print("No profiles found.")
        return

    for i, profile in enumerate(profiles, start=1):

        score = calculate_score(profile)

        print(f"\nProfile {i}")
        print(f"Name: {profile['name']}")
        print(f"Role: {profile['role']}")
        print(f"Career Score: {score} / 100")

        if score >= 90:
            print("Level: Strong senior candidate")
        elif score >= 70:
            print("Level: Competitive candidate")
        else:
            print("Level: Needs improvement")