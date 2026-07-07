import customtkinter as ctk
from tkinter import messagebox

from profile_manager import create_profile
from storage import load_profiles, save_profiles
from score import calculate_score


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def open_create_profile():
    window = ctk.CTkToplevel(app)
    window.title("Create Profile")
    window.geometry("420x460")

    ctk.CTkLabel(window, text="Create Profile", font=("Arial", 28, "bold")).pack(pady=20)

    name_entry = ctk.CTkEntry(window, width=280, placeholder_text="Name")
    name_entry.pack(pady=10)

    role_entry = ctk.CTkEntry(window, width=280, placeholder_text="Role")
    role_entry.pack(pady=10)

    experience_entry = ctk.CTkEntry(window, width=280, placeholder_text="Years of experience")
    experience_entry.pack(pady=10)

    salary_entry = ctk.CTkEntry(window, width=280, placeholder_text="Expected Salary (USD)")
    salary_entry.pack(pady=10)

    def save_profile_from_gui():
        try:
            profile = {
                "name": name_entry.get().strip(),
                "role": role_entry.get().strip(),
                "experience": int(experience_entry.get()),
                "salary": int(salary_entry.get()),
                "skills": []
            }

            profile["career_score"] = calculate_score(profile)
            create_profile(profile)

            messagebox.showinfo(
                "Success",
                f"Profile saved successfully!\nCareer Score: {profile['career_score']} / 100"
            )

            window.destroy()

        except ValueError:
            messagebox.showerror("Error", "Experience and Salary must be numbers.")

    ctk.CTkButton(
        window,
        text="Save Profile",
        width=220,
        height=40,
        command=save_profile_from_gui
    ).pack(pady=20)


def open_dashboard():
    window = ctk.CTkToplevel(app)
    window.title("Dashboard")
    window.geometry("650x500")

    ctk.CTkLabel(
        window,
        text="AI Career OS Dashboard",
        font=("Arial", 28, "bold")
    ).pack(pady=25)

    profiles = load_profiles()

    if len(profiles) == 0:
        ctk.CTkLabel(
            window,
            text="No profiles available yet.",
            font=("Arial", 16)
        ).pack(pady=40)
        return

    total_profiles = len(profiles)
    avg_score = sum(profile.get("career_score", 0) for profile in profiles) / total_profiles
    avg_salary = sum(profile.get("salary", 0) for profile in profiles) / total_profiles
    avg_experience = sum(profile.get("experience", 0) for profile in profiles) / total_profiles
    highest_salary = max(profile.get("salary", 0) for profile in profiles)
    latest_profile = profiles[-1]

    metrics_frame = ctk.CTkFrame(window)
    metrics_frame.pack(pady=10, padx=30, fill="both", expand=True)

    def metric_card(parent, title_text, value_text):
        card = ctk.CTkFrame(parent)
        card.pack(fill="x", padx=20, pady=8)

        ctk.CTkLabel(
            card,
            text=title_text,
            font=("Arial", 14)
        ).pack(anchor="w", padx=15, pady=(10, 2))

        ctk.CTkLabel(
            card,
            text=value_text,
            font=("Arial", 22, "bold")
        ).pack(anchor="w", padx=15, pady=(0, 10))

    metric_card(metrics_frame, "Total Profiles", str(total_profiles))
    metric_card(metrics_frame, "Average Career Score", f"{avg_score:.1f} / 100")
    metric_card(metrics_frame, "Average Salary", f"{avg_salary:.0f} USD")
    metric_card(metrics_frame, "Highest Salary", f"{highest_salary} USD")
    metric_card(metrics_frame, "Average Experience", f"{avg_experience:.1f} years")
    metric_card(metrics_frame, "Latest Profile", latest_profile.get("name", "Unknown"))


def open_view_profiles():
    window = ctk.CTkToplevel(app)
    window.title("View Profiles")
    window.geometry("650x560")

    ctk.CTkLabel(
        window,
        text="Saved Profiles",
        font=("Arial", 28, "bold")
    ).pack(pady=20)

    scroll_frame = ctk.CTkScrollableFrame(window, width=570, height=420)
    scroll_frame.pack(pady=10)

    def refresh_profiles():
        for widget in scroll_frame.winfo_children():
            widget.destroy()

        profiles = load_profiles()

        if len(profiles) == 0:
            ctk.CTkLabel(
                scroll_frame,
                text="No profiles saved yet.",
                font=("Arial", 16)
            ).pack(pady=40)
            return

        for index, profile in enumerate(profiles):
            card = ctk.CTkFrame(scroll_frame)
            card.pack(fill="x", padx=10, pady=10)

            name = profile.get("name", "Unknown")
            role = profile.get("role", "N/A")
            experience = profile.get("experience", 0)
            salary = profile.get("salary", 0)
            score = profile.get("career_score", 0)

            ctk.CTkLabel(card, text=f"👤 {name}", font=("Arial", 20, "bold")).pack(anchor="w", padx=15, pady=(12, 5))
            ctk.CTkLabel(card, text=f"💼 Role: {role}", font=("Arial", 14)).pack(anchor="w", padx=15)
            ctk.CTkLabel(card, text=f"🕒 Experience: {experience} years", font=("Arial", 14)).pack(anchor="w", padx=15)
            ctk.CTkLabel(card, text=f"💰 Salary: {salary} USD", font=("Arial", 14)).pack(anchor="w", padx=15)
            ctk.CTkLabel(card, text=f"⭐ Career Score: {score} / 100", font=("Arial", 14, "bold")).pack(anchor="w", padx=15, pady=(5, 5))

            progress = ctk.CTkProgressBar(card, width=420)
            progress.pack(anchor="w", padx=15, pady=(0, 10))
            progress.set(score / 100)

            def delete_profile(profile_index=index):
                confirm = messagebox.askyesno(
                    "Delete Profile",
                    "Are you sure you want to delete this profile?"
                )

                if confirm:
                    profiles = load_profiles()
                    profiles.pop(profile_index)
                    save_profiles(profiles)
                    refresh_profiles()

            ctk.CTkButton(
                card,
                text="Delete",
                width=120,
                command=delete_profile
            ).pack(anchor="e", padx=15, pady=(0, 12))

    refresh_profiles()


def show_score():
    messagebox.showinfo("Career Score", "Dashboard already includes Career Score.")


def show_skills():
    messagebox.showinfo("Skills Gap", "Next step: visual Skills Gap Analyzer.")


app = ctk.CTk()
app.title("AI Career OS")
app.geometry("720x560")

ctk.CTkLabel(
    app,
    text="AI Career OS",
    font=("Arial", 36, "bold")
).pack(pady=25)

ctk.CTkLabel(
    app,
    text="Your personal career intelligence platform",
    font=("Arial", 16)
).pack()

frame = ctk.CTkFrame(app)
frame.pack(pady=25)

ctk.CTkButton(frame, text="Dashboard", width=280, height=42, command=open_dashboard).pack(pady=8)
ctk.CTkButton(frame, text="Create Profile", width=280, height=42, command=open_create_profile).pack(pady=8)
ctk.CTkButton(frame, text="View Profiles", width=280, height=42, command=open_view_profiles).pack(pady=8)
ctk.CTkButton(frame, text="Career Score", width=280, height=42, command=show_score).pack(pady=8)
ctk.CTkButton(frame, text="Skills Gap Analyzer", width=280, height=42, command=show_skills).pack(pady=8)
ctk.CTkButton(frame, text="Exit", width=280, height=42, command=app.destroy).pack(pady=8)

app.mainloop()