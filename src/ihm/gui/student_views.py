import tkinter as tk
from tkinter import ttk

class StudentViews:
    def __init__(self, parent, main_window, username):
        self.main_window = main_window
        self.username = username
        
        # Header
        ttk.Label(parent, text=f"Student: {username}").pack(pady=10)
        ttk.Button(parent, text="Logout", command=main_window.show_login).pack()
        
        # Vote section
        ttk.Label(parent, text="Select students to work with:").pack(pady=10)
        
        self.student_var = tk.StringVar()
        students = self.get_students()
        combo = ttk.Combobox(parent, textvariable=self.student_var, values=students)
        combo.pack(pady=5)
        
        ttk.Button(parent, text="Add", command=self.add_vote).pack(pady=5)
        
        self.vote_list = tk.Listbox(parent, height=6)
        self.vote_list.pack(pady=10, fill=tk.X, padx=20)
        
        # Groups section
        ttk.Label(parent, text="Your Groups:").pack(pady=10)
        self.groups_text = tk.Text(parent, height=6, state=tk.DISABLED)
        self.groups_text.pack(fill=tk.BOTH, expand=True, padx=20)
        
        self.load_groups()
    
    def get_students(self):
        users = self.main_window.storage_service.get_all_users()
        return [u['username'] for u in users.values() 
                if u.get('status') == 'student' and u['username'] != self.username]
    
    def add_vote(self):
        student = self.student_var.get()
        if student:
            self.vote_list.insert(tk.END, student)
    
    def load_groups(self):
        self.groups_text.config(state=tk.NORMAL)
        self.groups_text.insert(tk.END, "No groups generated yet.\n")
        self.groups_text.config(state=tk.DISABLED)