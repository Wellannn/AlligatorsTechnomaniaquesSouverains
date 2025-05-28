import tkinter as tk
from tkinter import ttk, messagebox
from src.domain.vote import Vote
from datetime import datetime, timedelta
import random

class TeacherViews:
    def __init__(self, parent, main_window, username):
        self.main_window = main_window
        self.username = username

        # Notebook for tabs
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.student_tab = ttk.Frame(notebook)
        self.vote_tab = ttk.Frame(notebook)
        notebook.add(self.student_tab, text="Create Student")
        notebook.add(self.vote_tab, text="Create Vote")

        # Header
        ttk.Label(parent, text=f"Teacher: {username}").pack(pady=10)
        ttk.Button(parent, text="Logout", command=main_window.show_login).pack()

        # --- Create Student tab ---
        ttk.Label(self.student_tab, text="Create Student:").pack(pady=10)
        self.name_var = tk.StringVar()
        ttk.Entry(self.student_tab, textvariable=self.name_var, width=30).pack(pady=2)
        ttk.Button(self.student_tab, text="Create", command=self.create_student).pack(pady=5)

        # --- Create Vote tab ---
        ttk.Label(self.vote_tab, text="Create Vote:").pack(pady=10)
        self.vote_title = tk.StringVar()
        ttk.Entry(self.vote_tab, textvariable=self.vote_title, width=30).pack(pady=2)
        self.group_size = tk.StringVar(value="3")
        ttk.Entry(self.vote_tab, textvariable=self.group_size, width=10).pack(pady=2)
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
        import subprocess
        subprocess.Popen(["python3", "src/ihm/gui/create_vote.py"])
    
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