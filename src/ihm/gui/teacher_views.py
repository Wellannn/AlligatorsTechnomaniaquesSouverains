import tkinter as tk
from tkinter import ttk, messagebox
from src.domain.vote import Vote
from datetime import datetime, timedelta
import random

class TeacherViews:
    def __init__(self, parent, main_window, username):
        self.main_window = main_window
        self.username = username
        self.user, _ = self.main_window.storage_service.get_user_by_username(username)

        # Notebook for tabs
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.student_tab = ttk.Frame(notebook)
        self.vote_tab = ttk.Frame(notebook)
        notebook.add(self.student_tab, text="Create Student")
        notebook.add(self.vote_tab, text="Create Vote")

        # Header
        ttk.Label(parent, text=f"Teacher: {self.user.firstname} {self.user.lastname}").pack(pady=10)
        ttk.Button(parent, text="Logout", command=main_window.show_login).pack()

        # --- Create Student tab ---
        ttk.Label(self.student_tab, text="Create Student:").pack(pady=10)
        self.name_var = tk.StringVar()
        ttk.Entry(self.student_tab, textvariable=self.name_var, width=30).pack(pady=2)
        ttk.Button(self.student_tab, text="Create", command=self.create_student).pack(pady=5)

        # --- Create Vote tab ---
        ttk.Label(self.vote_tab, text="Create Vote:").pack(pady=10)
        ttk.Label(self.vote_tab, text="Vote Title:").pack()
        self.vote_title = tk.StringVar()
        ttk.Entry(self.vote_tab, textvariable=self.vote_title, width=30).pack(pady=2)

        ttk.Label(self.vote_tab, text="Group Size:").pack()
        self.group_size = tk.StringVar(value="3")
        ttk.Entry(self.vote_tab, textvariable=self.group_size, width=10).pack(pady=2)

        ttk.Label(self.vote_tab, text="End Date (YYYY-MM-DD):").pack()
        self.end_date = tk.StringVar()
        ttk.Entry(self.vote_tab, textvariable=self.end_date, width=20).pack(pady=2)

        ttk.Label(self.vote_tab, text="Add Students to Vote:").pack()
        self.students_listbox = tk.Listbox(self.vote_tab, selectmode=tk.MULTIPLE, height=6)
        self.students_listbox.pack(pady=5, fill=tk.X, padx=10)

        # Populate listbox with student usernames and ids
        users = self.main_window.storage_service.get_all_users()
        self.student_display = []
        self.student_usernames = []
        self.student_ids = []

        for user in users.values():
            if user.get('status') == 'student':
                display = f"{user['firstname']} {user['lastname']}"
                self.student_display.append(display)
                self.student_usernames.append(user['username'])
                self.student_ids.append(user['id'])
                self.students_listbox.insert(tk.END, display)

        ttk.Button(self.vote_tab, text="Create Vote", command=self.create_vote).pack(pady=5)
        # Generate groups button and results in vote tab
        ttk.Button(self.vote_tab, text="Generate Groups", command=self.generate_groups).pack(pady=20)
        self.result_text = tk.Text(self.vote_tab, height=8, state=tk.DISABLED)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=20)

    def create_student(self):
        name = self.name_var.get()
        if name:
            password = self.main_window.auth_service.create_user(name, name, "Student", f"{name}@test.com", "student")
            if password:
                messagebox.showinfo("Success", f"Student created! Password: {password}")
                self.name_var.set("")

    def create_vote(self):
        title = self.vote_title.get().strip()
        group_size_str = self.group_size.get().strip()
        end_date_str = self.end_date.get().strip()
        selected_indices = self.students_listbox.curselection()
        selected_students = [self.student_ids[i] for i in selected_indices]
        preferences = {student: {other: 0 for other in selected_students if other != student} for student in selected_students}

        if not title or not group_size_str or not end_date_str or not selected_students:
            messagebox.showerror("Error", "All fields must be filled and at least one student selected.")
            return

        try:
            group_size = int(group_size_str)
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid group size or date format.")
            return

        vote = Vote(title=title, group_size=group_size, end_date=end_date, eligible_students=selected_students, preference=preferences, teachers=self.user)
        self.main_window.storage_service.create_vote(vote)

        messagebox.showinfo("Success", "Vote created successfully!")

        self.vote_title.set("")
        self.group_size.set("3")
        self.end_date.set("")
        self.students_listbox.selection_clear(0, tk.END)
    
    def generate_groups(self):
        # Get all votes
        votes = self.main_window.storage_service.get_all_votes()
        if not votes:
            messagebox.showerror("Error", "No votes found")
            return
        
        # Use first vote
        vote_id, vote_data = list(votes.items())[0]
        
        # Get students
        users = self.main_window.storage_service.get_all_users()
        students = [u['username'] for u in users.values() if u.get('status') == 'student']
        
        if not students:
            messagebox.showerror("Error", "No students found")
            return
        
        # Simple random grouping
        random.shuffle(students)
        group_size = vote_data.get('group_size', 3)
        groups = [students[i:i+group_size] for i in range(0, len(students), group_size)]
        
        # Save groups
        self.main_window.storage_service.save_generated_group(vote_id, groups)
        
        # Display results
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        for i, group in enumerate(groups, 1):
            self.result_text.insert(tk.END, f"Group {i}: {', '.join(group)}\n")
        self.result_text.config(state=tk.DISABLED)
        
        messagebox.showinfo("Success", "Groups generated!")