import tkinter as tk
from tkinter import ttk, messagebox

class RegisterView:
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        frame = ttk.Frame(self.parent, padding="30")
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Register New User", font=('Arial', 14, 'bold')).pack(pady=10)
        
        ttk.Label(frame, text="Username:").pack()
        self.username_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.username_var, width=25).pack(pady=5)
        
        ttk.Label(frame, text="First Name:").pack()
        self.firstname_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.firstname_var, width=25).pack(pady=5)
        
        ttk.Label(frame, text="Last Name:").pack()
        self.lastname_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.lastname_var, width=25).pack(pady=5)
        
        ttk.Label(frame, text="Email:").pack()
        self.email_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.email_var, width=25).pack(pady=5)
        
        ttk.Label(frame, text="Role:").pack()
        self.role_var = tk.StringVar(value="student")
        ttk.Combobox(frame, textvariable=self.role_var, 
                    values=["student", "teacher"], state="readonly").pack(pady=5)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Register", command=self.register).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Back to Login", command=self.main_window.show_login).pack(side=tk.LEFT, padx=5)
    
    def register(self):
        username = self.username_var.get()
        firstname = self.firstname_var.get()
        lastname = self.lastname_var.get()
        email = self.email_var.get()
        role = self.role_var.get()
        
        if not all([username, firstname, lastname, email]):
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        password = self.main_window.auth_service.create_user(username, firstname, lastname, email, role)
        
        if password:
            messagebox.showinfo("Success", f"User created! Password: {password}")
            self.main_window.show_login()
        else:
            messagebox.showerror("Error", "Username already exists")