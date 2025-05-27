import tkinter as tk
from tkinter import ttk, messagebox

class LoginView:
    def __init__(self, parent, main_window):
        self.main_window = main_window
        
        frame = ttk.Frame(parent, padding="30")
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Login", font=('Arial', 14, 'bold')).pack(pady=10)
        
        ttk.Label(frame, text="Username:").pack()
        self.username_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.username_var).pack(pady=5)
        
        ttk.Label(frame, text="Password:").pack()
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, show="*").pack(pady=5)
        
        ttk.Button(frame, text="Login", command=self.login).pack(pady=20)
    
    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        if self.main_window.auth_service.login_user(username, password):
            user = self.main_window.storage_service.get_user(username)
            status = user.get('status', 'student')
            
            if status == "owner":
                self.main_window.show_owner_views(username)
            elif status == "teacher":
                self.main_window.show_teacher_views(username)
            else:
                self.main_window.show_student_views(username)
        else:
            messagebox.showerror("Error", "Invalid login")