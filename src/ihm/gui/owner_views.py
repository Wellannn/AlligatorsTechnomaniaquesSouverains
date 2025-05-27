import tkinter as tk
from tkinter import ttk, messagebox

class OwnerViews:
    def __init__(self, parent, main_window, username):
        self.main_window = main_window
        self.username = username
        
        # Header
        ttk.Label(parent, text=f"Owner: {username}").pack(pady=10)
        ttk.Button(parent, text="Logout", command=main_window.show_login).pack()
        
        # Create Teacher
        ttk.Label(parent, text="Create Teacher:").pack(pady=10)
        self.teacher_name = tk.StringVar()
        ttk.Entry(parent, textvariable=self.teacher_name, width=30).pack(pady=2)
        ttk.Button(parent, text="Create Teacher", command=self.create_teacher).pack(pady=5)
        
        # Create Student
        ttk.Label(parent, text="Create Student:").pack(pady=10)
        self.student_name = tk.StringVar()
        ttk.Entry(parent, textvariable=self.student_name, width=30).pack(pady=2)
        ttk.Button(parent, text="Create Student", command=self.create_student).pack(pady=5)
        
        # Users list
        ttk.Label(parent, text="All Users:").pack(pady=10)
        self.users_list = tk.Listbox(parent, height=10)
        self.users_list.pack(fill=tk.BOTH, expand=True, padx=20)
        
        ttk.Button(parent, text="Refresh", command=self.refresh_users).pack(pady=5)
        
        self.refresh_users()
    
    def create_teacher(self):
        name = self.teacher_name.get()
        if name:
            password = self.main_window.auth_service.create_user(name, name, "Teacher", f"{name}@test.com", "teacher")
            if password:
                messagebox.showinfo("Success", f"Teacher created! Password: {password}")
                self.teacher_name.set("")
                self.refresh_users()
    
    def create_student(self):
        name = self.student_name.get()
        if name:
            password = self.main_window.auth_service.create_user(name, name, "Student", f"{name}@test.com", "student")
            if password:
                messagebox.showinfo("Success", f"Student created! Password: {password}")
                self.student_name.set("")
                self.refresh_users()
    
    def refresh_users(self):
        self.users_list.delete(0, tk.END)
        users = self.main_window.storage_service.get_all_users()
        for user in users.values():
            status = user.get('status', 'unknown')
            username = user.get('username', 'unknown')
            self.users_list.insert(tk.END, f"{status}: {username}")