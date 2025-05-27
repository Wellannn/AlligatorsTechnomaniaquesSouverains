import tkinter as tk
from tkinter import ttk, messagebox

class TeacherViews:
    def __init__(self, parent, main_window, username):
        self.parent = parent
        self.main_window = main_window
        self.username = username
        self.setup_ui()
    
    def setup_ui(self):
        # create header with teacher name and logout button
        header = ttk.Frame(self.parent)
        header.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(header, text=f"Teacher: {self.username}", font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        ttk.Button(header, text="Logout", command=self.main_window.show_login).pack(side=tk.RIGHT)
        
        # create navigation buttons
        nav = ttk.Frame(self.parent)
        nav.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(nav, text="Create Student", command=self.show_create).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav, text="Create Vote", command=self.show_create_vote).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav, text="Generate Groups", command=self.show_generate).pack(side=tk.LEFT, padx=5)
        
        self.content = ttk.Frame(self.parent)
        self.content.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.show_create()  # default view
    
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()
    
    def show_create(self):
        self.clear_content()
        ttk.Label(self.content, text="Create Student", font=('Arial', 12, 'bold')).pack(pady=10)
        
        ttk.Label(self.content, text="Name:").pack()
        self.name_var = tk.StringVar()
        ttk.Entry(self.content, textvariable=self.name_var).pack(pady=5)
        
        ttk.Label(self.content, text="Last Name:").pack()
        self.lastname_var = tk.StringVar()
        ttk.Entry(self.content, textvariable=self.lastname_var).pack(pady=5)
        
        ttk.Button(self.content, text="Generate Password", command=self.generate_pwd).pack(pady=5)
        
        self.pwd_var = tk.StringVar()
        ttk.Entry(self.content, textvariable=self.pwd_var, state='readonly').pack(pady=5)
        
        ttk.Label(self.content, text="Status:").pack()
        self.status_var = tk.StringVar(value="student")
        ttk.Combobox(self.content, textvariable=self.status_var, 
                    values=["student"]).pack(pady=5)
        
        ttk.Button(self.content, text="Create", command=self.create_student).pack(pady=10)
    
    def show_create_vote(self):
        self.clear_content()
        ttk.Label(self.content, text="Create Vote", font=('Arial', 12, 'bold')).pack(pady=10)
        
        ttk.Label(self.content, text="Vote Name:").pack()
        self.vote_name_var = tk.StringVar()
        ttk.Entry(self.content, textvariable=self.vote_name_var).pack(pady=5)
        
        ttk.Label(self.content, text="Group Size:").pack()
        self.group_size_var = tk.StringVar()
        ttk.Entry(self.content, textvariable=self.group_size_var).pack(pady=5)
        
        ttk.Label(self.content, text="Add Students:").pack()
        self.students_list = tk.Listbox(self.content, height=5)
        self.students_list.pack(pady=5, fill=tk.X)
        
        ttk.Button(self.content, text="Add Teacher", command=self.add_teacher).pack(pady=5)
        ttk.Button(self.content, text="Create Vote", command=self.create_vote).pack(pady=10)
    
    def show_generate(self):
        self.clear_content()
        ttk.Label(self.content, text="Generate Groups", font=('Arial', 12, 'bold')).pack(pady=10)
        
        ttk.Label(self.content, text="Same as Create Vote but with:").pack(pady=5)
        ttk.Button(self.content, text="Generate Groups", command=self.generate_groups).pack(pady=20)
    
    def generate_pwd(self):
        # generate temporary password
        self.pwd_var.set("temp123")  # TODO: Generate real password
    
    def create_student(self):
        messagebox.showinfo("Success", "Student created!")
    
    def add_teacher(self):
        messagebox.showinfo("Info", "Teacher added to vote")
    
    def create_vote(self):
        messagebox.showinfo("Success", "Vote created!")
    
    def generate_groups(self):
        messagebox.showinfo("Success", "Groups generated!")