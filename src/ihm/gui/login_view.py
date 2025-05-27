import tkinter as tk
from tkinter import ttk, messagebox

class LoginView:
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        # create main frame with padding
        frame = ttk.Frame(self.parent, padding="30")
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Login", font=('Arial', 14, 'bold')).pack(pady=10)
        
        ttk.Label(frame, text="Name:").pack()
        self.name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.name_var, width=25).pack(pady=5)
        
        ttk.Label(frame, text="Password:").pack()
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, show="*", width=25).pack(pady=5)
        
        ttk.Label(frame, text="Key:").pack()
        self.key_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.key_var, width=25).pack(pady=5)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Validate", command=self.login).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="New", command=self.new_user).pack(side=tk.LEFT, padx=5)
    
    def login(self):
        # check if user is teacher or student
        # TODO: Call core authentication
        name = self.name_var.get()
        if "teacher" in name.lower():
            self.main_window.show_teacher_views(name)
        else:
            self.main_window.show_student_views(name)
    
    def new_user(self):
        # TODO: Handle first connection
        messagebox.showinfo("Info", "First connection feature")