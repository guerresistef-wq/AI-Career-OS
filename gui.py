import customtkinter as ctk
from tkinter import messagebox, filedialog

from app.database import (
    create_tables,
    add_profile,
    get_all_profiles,
    update_profile,
    delete_profile,
)

from app.services.resume_service import analyze_resume


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def calculate_score(experience, salary):
    score = 0

    if experience >= 10:
        score += 50
    elif experience >= 5:
        score += 35
    else:
        score += 20

    if salary >= 5000:
        score += 30
    elif salary >= 3500:
        score += 25
    else:
        score += 15

    score += 20
    return score


class AICareerOSApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        create_tables()

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

        ctk.CTkButton(self.sidebar, text="Dashboard", width=180, command=self.show_dashboard).pack(pady=8)
        ctk.CTkButton(self.sidebar, text="Create Profile", width=180, command=self.show_create_profile).pack(pady=8)
        ctk.CTkButton(self.sidebar, text="View Profiles", width=180, command=self.show_profiles).pack(pady=8)
        ctk.CTkButton(self.sidebar, text="Career Score", width=180, command=self.show_scores).pack(pady=8)
        ctk.CTkButton(self.sidebar, text="Resume Analyzer", width=180, command=self.show_resume_analyzer).pack(pady=8)
        ctk.CTkButton(self.sidebar, text="Exit", width=180, command=self.destroy).pack(pady=(40, 8))

    def show_dashboard(self):
        self.clear_content()

        ctk.CTkLabel(self.content, text="Dashboard", font=("Arial", 32, "bold")).pack(pady=20)

        profiles = get_all_profiles()

        if len(profiles) == 0:
            ctk.CTkLabel(self.content, text="No profiles available yet.", font=("Arial", 18)).pack(pady=40)
            return

        total_profiles = len(profiles)
        avg_score = sum(profile[5] for profile in profiles) / total_profiles
        avg_salary = sum(profile[4] for profile in profiles) / total_profiles
        highest_salary = max(profile[4] for profile in profiles)
        latest_profile = profiles[-1][1]

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

            ctk.CTkLabel(card, text=title, font=("Arial", 15)).pack(anchor="w", padx=20, pady=(12, 2))
            ctk.CTkLabel(card, text=str(value), font=("Arial", 24, "bold")).pack(anchor="w", padx=20, pady=(0, 12))

    def show_create_profile(self):
        self.clear_content()

        ctk.CTkLabel(self.content, text="Create Profile", font=("Arial", 32, "bold")).pack(pady=20)

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
                name = name_entry.get().strip()
                role = role_entry.get().strip()
                experience = int(experience_entry.get())
                salary = int(salary_entry.get())

                if name == "" or role == "":
                    messagebox.showerror("Error", "Name and Role are required.")
                    return

                career_score = calculate_score(experience, salary)
                add_profile(name, role, experience, salary, career_score)

                messagebox.showinfo("Success", f"Profile saved successfully!\nCareer Score: {career_score} / 100")
                self.show_dashboard()

            except ValueError:
                messagebox.showerror("Error", "Experience and Salary must be numbers.")

        ctk.CTkButton(form, text="Save Profile", width=220, height=40, command=save_profile_from_form).pack(pady=20)

    def show_edit_profile(self, profile):
        self.clear_content()

        profile_id = profile[0]
        current_name = profile[1]
        current_role = profile[2]
        current_experience = profile[3]
        current_salary = profile[4]

        ctk.CTkLabel(self.content, text="Edit Profile", font=("Arial", 32, "bold")).pack(pady=20)

        form = ctk.CTkFrame(self.content)
        form.pack(pady=20)

        name_entry = ctk.CTkEntry(form, width=320)
        name_entry.insert(0, current_name)
        name_entry.pack(pady=10)

        role_entry = ctk.CTkEntry(form, width=320)
        role_entry.insert(0, current_role)
        role_entry.pack(pady=10)

        experience_entry = ctk.CTkEntry(form, width=320)
        experience_entry.insert(0, str(current_experience))
        experience_entry.pack(pady=10)

        salary_entry = ctk.CTkEntry(form, width=320)
        salary_entry.insert(0, str(current_salary))
        salary_entry.pack(pady=10)

        def save_changes():
            try:
                name = name_entry.get().strip()
                role = role_entry.get().strip()
                experience = int(experience_entry.get())
                salary = int(salary_entry.get())

                if name == "" or role == "":
                    messagebox.showerror("Error", "Name and Role are required.")
                    return

                career_score = calculate_score(experience, salary)

                update_profile(profile_id, name, role, experience, salary, career_score)

                messagebox.showinfo("Success", "Profile updated successfully!")
                self.show_profiles()

            except ValueError:
                messagebox.showerror("Error", "Experience and Salary must be numbers.")

        ctk.CTkButton(form, text="Save Changes", width=220, height=40, command=save_changes).pack(pady=10)
        ctk.CTkButton(form, text="Cancel", width=220, height=40, command=self.show_profiles).pack(pady=10)

    def show_profiles(self):
        self.clear_content()

        ctk.CTkLabel(self.content, text="Saved Profiles", font=("Arial", 32, "bold")).pack(pady=20)

        search_entry = ctk.CTkEntry(self.content, width=500, placeholder_text="Search by name or role...")
        search_entry.pack(pady=10)

        scroll = ctk.CTkScrollableFrame(self.content, width=680, height=410)
        scroll.pack(pady=10)

        def render_profiles(search_text=""):
            for widget in scroll.winfo_children():
                widget.destroy()

            profiles = get_all_profiles()

            if search_text != "":
                profiles = [
                    profile for profile in profiles
                    if search_text.lower() in profile[1].lower()
                    or search_text.lower() in profile[2].lower()
                ]

            if len(profiles) == 0:
                ctk.CTkLabel(scroll, text="No matching profiles found.", font=("Arial", 18)).pack(pady=40)
                return

            for profile in profiles:
                profile_id = profile[0]
                name = profile[1]
                role = profile[2]
                experience = profile[3]
                salary = profile[4]
                score = profile[5]

                card = ctk.CTkFrame(scroll)
                card.pack(fill="x", padx=10, pady=10)

                ctk.CTkLabel(card, text=f"👤 {name}", font=("Arial", 22, "bold")).pack(anchor="w", padx=15, pady=(12, 5))
                ctk.CTkLabel(card, text=f"💼 Role: {role}", font=("Arial", 15)).pack(anchor="w", padx=15)
                ctk.CTkLabel(card, text=f"🕒 Experience: {experience} years", font=("Arial", 15)).pack(anchor="w", padx=15)
                ctk.CTkLabel(card, text=f"💰 Salary: {salary} USD", font=("Arial", 15)).pack(anchor="w", padx=15)
                ctk.CTkLabel(card, text=f"⭐ Career Score: {score} / 100", font=("Arial", 15, "bold")).pack(anchor="w", padx=15, pady=(5, 5))

                progress = ctk.CTkProgressBar(card, width=450)
                progress.pack(anchor="w", padx=15, pady=(0, 10))
                progress.set(score / 100)

                button_row = ctk.CTkFrame(card, fg_color="transparent")
                button_row.pack(anchor="e", padx=15, pady=(0, 12))

                ctk.CTkButton(
                    button_row,
                    text="Edit",
                    width=100,
                    command=lambda selected_profile=profile: self.show_edit_profile(selected_profile)
                ).pack(side="left", padx=5)

                def delete_selected_profile(selected_id=profile_id):
                    confirm = messagebox.askyesno(
                        "Delete Profile",
                        "Are you sure you want to delete this profile?"
                    )

                    if confirm:
                        delete_profile(selected_id)
                        render_profiles(search_entry.get().strip())

                ctk.CTkButton(
                    button_row,
                    text="Delete",
                    width=100,
                    command=delete_selected_profile
                ).pack(side="left", padx=5)

        def on_search(event):
            render_profiles(search_entry.get().strip())

        search_entry.bind("<KeyRelease>", on_search)
        render_profiles()

    def show_scores(self):
        self.clear_content()

        ctk.CTkLabel(self.content, text="Career Scores", font=("Arial", 32, "bold")).pack(pady=20)

        profiles = get_all_profiles()

        if len(profiles) == 0:
            ctk.CTkLabel(self.content, text="No profiles available.", font=("Arial", 18)).pack(pady=40)
            return

        for profile in profiles:
            name = profile[1]
            score = profile[5]

            card = ctk.CTkFrame(self.content)
            card.pack(fill="x", padx=40, pady=10)

            ctk.CTkLabel(card, text=name, font=("Arial", 22, "bold")).pack(anchor="w", padx=20, pady=(15, 5))
            ctk.CTkLabel(card, text=f"{score} / 100", font=("Arial", 28, "bold")).pack(anchor="w", padx=20)

            progress = ctk.CTkProgressBar(card, width=500)
            progress.pack(anchor="w", padx=20, pady=10)
            progress.set(score / 100)

            if score >= 90:
                level = "Strong senior candidate"
            elif score >= 70:
                level = "Competitive candidate"
            else:
                level = "Needs improvement"

            ctk.CTkLabel(card, text=f"Level: {level}", font=("Arial", 15)).pack(anchor="w", padx=20, pady=(0, 15))

    def show_resume_analyzer(self):
        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="Resume Analyzer",
            font=("Arial", 32, "bold")
        ).pack(pady=20)

        result_frame = ctk.CTkScrollableFrame(self.content, width=700, height=460)
        result_frame.pack(pady=10)

        def clear_results():
            for widget in result_frame.winfo_children():
                widget.destroy()

        def upload_resume():
            file_path = filedialog.askopenfilename(
                title="Select Resume PDF",
                filetypes=[
                    ("PDF files", "*.pdf"),
                    ("All files", "*.*")
                ]
            )

            if not file_path:
                return

            clear_results()

            result = analyze_resume(file_path)

            if not result["success"]:
                ctk.CTkLabel(
                    result_frame,
                    text=result["message"],
                    font=("Arial", 18)
                ).pack(pady=20)
                return

            score = result["score"]
            keywords = result["keywords"]
            preview = result["preview"]

            ctk.CTkLabel(
                result_frame,
                text="Resume Score",
                font=("Arial", 24, "bold")
            ).pack(pady=(20, 5))

            ctk.CTkLabel(
                result_frame,
                text=f"{score} / 100",
                font=("Arial", 36, "bold")
            ).pack(pady=5)

            progress = ctk.CTkProgressBar(result_frame, width=500)
            progress.pack(pady=10)
            progress.set(score / 100)

            ctk.CTkLabel(
                result_frame,
                text=result["message"],
                font=("Arial", 18)
            ).pack(pady=10)

            ctk.CTkLabel(
                result_frame,
                text="Keywords Found",
                font=("Arial", 22, "bold")
            ).pack(pady=(25, 10))

            if keywords:
                for keyword in keywords:
                    ctk.CTkLabel(
                        result_frame,
                        text=f"✓ {keyword}",
                        font=("Arial", 15)
                    ).pack(anchor="w", padx=80)
            else:
                ctk.CTkLabel(
                    result_frame,
                    text="No known keywords found.",
                    font=("Arial", 15)
                ).pack(pady=10)

            ctk.CTkLabel(
                result_frame,
                text="Resume Preview",
                font=("Arial", 22, "bold")
            ).pack(pady=(25, 10))

            preview_box = ctk.CTkTextbox(result_frame, width=620, height=220)
            preview_box.pack(pady=10)
            preview_box.insert("1.0", preview)
            preview_box.configure(state="disabled")

        ctk.CTkButton(
            self.content,
            text="Upload Resume PDF",
            width=260,
            height=45,
            command=upload_resume
        ).pack(pady=10)


if __name__ == "__main__":
    app = AICareerOSApp()
    app.mainloop()