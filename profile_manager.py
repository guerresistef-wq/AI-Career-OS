from storage import load_profiles, save_profiles
from utils import title
from score import calculate_score


def create_profile(profile):
    profiles = load_profiles()
    profiles.append(profile)
    save_profiles(profiles)


def view_profiles():
    profiles = load_profiles()

    title("SAVED PROFILES")

    if len(profiles) == 0:
        print("No profiles found.")
        return

    for i, profile in enumerate(profiles, start=1):
        print(f"\nProfile {i}")
        print(f"Name: {profile['name']}")
        print(f"Role: {profile['role']}")
        print(f"Experience: {profile['experience']} years")
        print(f"Salary: {profile['salary']} USD")
        print(f"Career Score: {profile.get('career_score', 'N/A')}")


def edit_profile():
    profiles = load_profiles()

    if len(profiles) == 0:
        print("No profiles found.")
        return

    view_profiles()

    profile_number = int(input("\nProfile number to edit: "))

    if profile_number < 1 or profile_number > len(profiles):
        print("Invalid profile number.")
        return

    profile = profiles[profile_number - 1]

    print("\nLeave blank to keep current value.")

    new_name = input(f"Name ({profile['name']}): ").strip()
    new_role = input(f"Role ({profile['role']}): ").strip()
    new_experience = input(f"Experience ({profile['experience']}): ").strip()
    new_salary = input(f"Salary ({profile['salary']}): ").strip()

    if new_name != "":
        profile["name"] = new_name

    if new_role != "":
        profile["role"] = new_role

    if new_experience != "":
        profile["experience"] = int(new_experience)

    if new_salary != "":
        profile["salary"] = int(new_salary)

    profile["career_score"] = calculate_score(profile)

    save_profiles(profiles)

    print("\nProfile updated successfully!")
    print("New Career Score:", profile["career_score"], "/ 100")