import customtkinter as ctk
from tkinter import messagebox

from profile_manager import create_profile
from storage import load_profiles, save_profiles
from score import calculate_score


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AICareerOSApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Career OS")
        self.geometry("1000x650")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.content = ctk.CTkFrame(self)
        self.content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.build_sidebar()
        self.show_dashboard()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def build_sidebar(self):
        ctk.CTkLabel(
            self.sidebar,
            text="AI Career OS",
            font=("Arial", 24, "bold")
        ).pack(pady=(30, 20))

        ctk.CTkButton(
            self.sidebar,
            text="Dashboard",
            width=180,
            command=self.show_dashboard
        ).pack(pady=8)

        ctk.CTkButton(
            self.sidebar,
            text="Create Profile",
            width=180,
            command=self.show_create_profile
        ).pack(pady=8)

        ctk.CTkButton(
            self.sidebar,
            text="View Profiles",
            width=180,
            command=self.show_profiles
        ).pack(pady=8)

        ctk.CTkButton(
            self.sidebar,
            text="Career Score",
            width=180,
            command=self.show_scores
        ).pack(pady=8)

        ctk.CTkButton(
            self.sidebar,
            text="Skills Gap",
            width=180,
            command=self.show_skills
        ).pack(pady=8)

        ctk.CTkButton(
            self.sidebar,
            text="Exit",
            width=180,
            command=self.destroy
        ).pack(pady=(40, 8))

    def show_dashboard(self):
        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="Dashboard",
            font=("Arial", 32, "bold")
        ).pack(pady=20)

        profiles = load_profiles()

        if len(profiles) == 0:
            ctk.CTkLabel(
                self.content,
                text="No profiles available yet.",
                font=("Arial", 18)
            ).pack(pady=40)
            return

        total_profiles = len(profiles)
        avg_score = sum(profile.get("career_score", 0) for profile in profiles) / total_profiles
        avg_salary = sum(profile.get("salary", 0) for profile in profiles) / total_profiles
        highest_salary = max(profile.get("salary", 0) for profile in profiles)
        latest_profile = profiles[-1].get("name", "Unknown")

        metrics = [
            ("Total Profiles", total_profiles),
            ("Average Career Score", f"{avg_score:.1f} / 100"),
            ("Average Salary", f"{avg_salary:.0f} USD"),
            ("Highest Salary", f"{highest_salary} USD"),
            ("Latest Profile", latest_profile),
        ]

        for title, value in metrics:
            card = ctk.CTkFrame(self.content)
            card.pack(fill="x", padx=40, pady=8)

            ctk.CTkLabel(
                card,
                text=title,
                font=("Arial", 15)
            ).pack(anchor="w", padx=20, pady=(12, 2))

            ctk.CTkLabel(
                card,
                text=str(value),
                font=("Arial", 24, "bold")
            ).pack(anchor="w", padx=20, pady=(0, 12))

    def show_create_profile(self):
        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="Create Profile",
            font=("Arial", 32, "bold")
        ).pack(pady=20)

        form = ctk.CTkFrame(self.content)
        form.pack(pady=20)

        name_entry = ctk.CTkEntry(form, width=320, placeholder_text="Name")
        name_entry.pack(pady=10)

        role_entry = ctk.CTkEntry(form, width=320, placeholder_text="Role")
        role_entry.pack(pady=10)

        experience_entry = ctk.CTkEntry(form, width=320, placeholder_text="Years of experience")
        experience_entry.pack(pady=10)

        salary_entry = ctk.CTkEntry(form, width=320, placeholder_text="Expected Salary (USD)")
        salary_entry.pack(pady=10)

        def save_profile_from_form():
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

                self.show_dashboard()

            except ValueError:
                messagebox.showerror("Error", "Experience and Salary must be numbers.")

        ctk.CTkButton(
            form,
            text="Save Profile",
            width=220,
            height=40,
            command=save_profile_from_form
        ).pack(pady=20)

    def show_profiles(self):
        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="Saved Profiles",
            font=("Arial", 32, "bold")
        ).pack(pady=20)

        profiles = load_profiles()

        if len(profiles) == 0:
            ctk.CTkLabel(
                self.content,
                text="No profiles saved yet.",
                font=("Arial", 18)
            ).pack(pady=40)
            return

        scroll = ctk.CTkScrollableFrame(self.content, width=680, height=460)
        scroll.pack(pady=10)

        for index, profile in enumerate(profiles):
            card = ctk.CTkFrame(scroll)
            card.pack(fill="x", padx=10, pady=10)

            score = profile.get("career_score", 0)

            ctk.CTkLabel(
                card,
                text=f"👤 {profile.get('name', 'Unknown')}",
                font=("Arial", 22, "bold")
            ).pack(anchor="w", padx=15, pady=(12, 5))

            ctk.CTkLabel(
                card,
                text=f"💼 Role: {profile.get('role', 'N/A')}",
                font=("Arial", 15)
            ).pack(anchor="w", padx=15)

            ctk.CTkLabel(
                card,
                text=f"🕒 Experience: {profile.get('experience', 0)} years",
                font=("Arial", 15)
            ).pack(anchor="w", padx=15)

            ctk.CTkLabel(
                card,
                text=f"💰 Salary: {profile.get('salary', 0)} USD",
                font=("Arial", 15)
            ).pack(anchor="w", padx=15)

            ctk.CTkLabel(
                card,
                text=f"⭐ Career Score: {score} / 100",
                font=("Arial", 15, "bold")
            ).pack(anchor="w", padx=15, pady=(5, 5))

            progress = ctk.CTkProgressBar(card, width=450)
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
                    self.show_profiles()

            ctk.CTkButton(
                card,
                text="Delete",
                width=120,
                command=delete_profile
            ).pack(anchor="e", padx=15, pady=(0, 12))

    def show_scores(self):
        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="Career Scores",
            font=("Arial", 32, "bold")
        ).pack(pady=20)

        profiles = load_profiles()

        if len(profiles) == 0:
            ctk.CTkLabel(
                self.content,
                text="No profiles available.",
                font=("Arial", 18)
            ).pack(pady=40)
            return

        for profile in profiles:
            score = profile.get("career_score", 0)

            card = ctk.CTkFrame(self.content)
            card.pack(fill="x", padx=40, pady=10)

            ctk.CTkLabel(
                card,
                text=profile.get("name", "Unknown"),
                font=("Arial", 22, "bold")
            ).pack(anchor="w", padx=20, pady=(15, 5))

            ctk.CTkLabel(
                card,
                text=f"{score} / 100",
                font=("Arial", 28, "bold")
            ).pack(anchor="w", padx=20)

            progress = ctk.CTkProgressBar(card, width=500)
            progress.pack(anchor="w", padx=20, pady=10)
            progress.set(score / 100)

            if score >= 90:
                level = "Strong senior candidate"
            elif score >= 70:
                level = "Competitive candidate"
            else:
                level = "Needs improvement"

            ctk.CTkLabel(
                card,
                text=f"Level: {level}",
                font=("Arial", 15)
            ).pack(anchor="w", padx=20, pady=(0, 15))

    def show_skills(self):
        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="Skills Gap Analyzer",
            font=("Arial", 32, "bold")
        ).pack(pady=20)

        ctk.CTkLabel(
            self.content,
            text="Visual skills analyzer coming next.",
            font=("Arial", 18)
        ).pack(pady=40)


if __name__ == "__main__":
    app = AICareerOSApp()
    app.mainloop()