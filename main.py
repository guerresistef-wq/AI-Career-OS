from utils import title, pause
from profile_manager import create_profile, view_profiles, edit_profile
from app.services.score_service import calculate_score, show_scores
from skills import skills_gap_analyzer


def get_number(prompt):
    value = input(prompt).strip()

    if value == "":
        return 0

    return int(value)


def show_menu():
    title("AI CAREER OS")

    print("1. Create Career Profile")
    print("2. View Saved Profiles")
    print("3. Edit Profile")
    print("4. Career Score")
    print("5. Salary Analyzer")
    print("6. Skills Gap Analyzer")
    print("7. Exit")


def create_profile_menu():
    name = input("Name: ").strip()
    role = input("Role: ").strip()
    experience = get_number("Years of experience: ")
    salary = get_number("Expected salary (USD): ")

    profile = {
        "name": name,
        "role": role,
        "experience": experience,
        "salary": salary,
        "skills": []
    }

    profile["career_score"] = calculate_score(profile)

    create_profile(profile)

    print("\nProfile saved successfully!")
    print("Career Score:", profile["career_score"], "/ 100")


def salary_analyzer():
    salary = get_number("Expected monthly salary (USD): ")

    if salary >= 5000:
        print("Excellent target for enterprise roles.")
    elif salary >= 3500:
        print("Good target. Very realistic for your current profile.")
    else:
        print("Good starting point, but let's build your technical profile to aim higher.")


while True:
    show_menu()

    option = input("\nChoose an option: ").strip()

    print()

    if option == "1":
        create_profile_menu()

    elif option == "2":
        view_profiles()

    elif option == "3":
        edit_profile()

    elif option == "4":
        show_scores()

    elif option == "5":
        salary_analyzer()

    elif option == "6":
        skills_gap_analyzer()

    elif option == "7":
        print("Goodbye!")
        break

    else:
        print("Invalid option.")

    pause()
    print()
    