import tkinter as tk
from tkinter import ttk, messagebox
from src.domain.vote import Vote
from datetime import datetime

class StudentViews:
    def __init__(self, parent, main_window, username):
        self.main_window = main_window
        self.username = username

        self.total_points = 10
        self.points_remaining = self.total_points
        self.votes_data = {}

        # Zone principale scrollable
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Widgets dans le scrollable_frame
        ttk.Label(scrollable_frame, text=f"Student: {username}").pack(pady=5)
        ttk.Button(scrollable_frame, text="Logout", command=main_window.show_login).pack()

        self.points_label = ttk.Label(scrollable_frame, text=f"Points remaining: {self.points_remaining}")
        self.points_label.pack(pady=5)

        for student in self.get_students():
            frame = ttk.Frame(scrollable_frame)
            frame.pack(fill=tk.X, pady=2, padx=10)

            ttk.Label(frame, text=student["username"]).pack(side=tk.LEFT)

            var = tk.IntVar(value=0)
            combo = ttk.Combobox(frame, textvariable=var, width=5, state="readonly")
            combo["values"] = list(range(0, self.total_points + 1))
            combo.pack(side=tk.RIGHT)

            combo.bind("<<ComboboxSelected>>", lambda e, v=var: self.update_remaining_points())
            self.votes_data[student["username"]] = (var, combo)

        ttk.Button(scrollable_frame, text="Submit", command=self.submit_votes).pack(pady=10)

        ttk.Label(scrollable_frame, text="Your Groups:").pack(pady=10)
        self.groups_text = tk.Text(scrollable_frame, height=6, state=tk.DISABLED)
        self.groups_text.pack(fill=tk.BOTH, expand=True, padx=20)

        self.load_groups()

    def get_students(self):
        return [
            u for u in self.main_window.storage_service.get_all_users_by_role("student")
            if u["username"] != self.username
        ]

    def update_remaining_points(self):
        total_given = sum(var.get() for var, _ in self.votes_data.values())
        self.points_remaining = max(0, self.total_points - total_given)
        self.points_label.config(text=f"Points remaining: {self.points_remaining}")

        for student, (var, combo) in self.votes_data.items():
            current_val = var.get()
            max_value = min(current_val + self.points_remaining, self.total_points)
            combo["values"] = list(range(0, max_value + 1))
            if current_val > max_value:
                var.set(max_value)

    def submit_votes(self):
        vote = self.main_window.storage_service.get_vote_by_title("les groupes de travail")
        if not vote:
            messagebox.showerror("Error", "Vote not found.")
            return

        vote_dict = vote.to_dict() if hasattr(vote, "to_dict") else vars(vote)

        prefs = {}
        for student_username, (var, _) in self.votes_data.items():
            weight = var.get()
            if weight > 0:
                prefs[student_username] = weight

        if not prefs:
            messagebox.showwarning("Warning", "You must assign at least one point.")
            return

        vote_dict["preferennces"][self.username] = prefs

        self.main_window.storage_service.update_vote_preferences(vote_dict["id"], vote_dict["preferennces"])

        messagebox.showinfo("Success", "Votes submitted successfully!")


    def load_groups(self):
        self.groups_text.config(state=tk.NORMAL)
        self.groups_text.insert(tk.END, "No groups generated yet.\n")
        self.groups_text.config(state=tk.DISABLED)
