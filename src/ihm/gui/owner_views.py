import tkinter as tk
from tkinter import ttk, messagebox

class OwnerViews:
    def __init__(self, parent, main_window, username):
        self.parent = parent
        self.main_window = main_window
        self.username = username
        self.setup_ui()
    
    def setup_ui(self):
        # header
        header = ttk.Frame(self.parent)
        header.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(header, text=f"Owner: {self.username}", font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        ttk.Button(header, text="Logout", command=self.main_window.show_login).pack(side=tk.RIGHT)
        
        # buttons
        nav = ttk.Frame(self.parent)
        nav.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(nav, text="Teachers", command=self.show_teachers).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav, text="Students", command=self.show_students).pack(side=tk.LEFT, padx=5)
        
        # content
        self.content = ttk.Frame(self.parent)
        self.content.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.show_teachers()
    
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()
    
    def show_teachers(self):
        self.clear_content()
        ttk.Label(self.content, text="Manage Teachers", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # create new teacher
        frame1 = ttk.Frame(self.content)
        frame1.pack(pady=10)
        
        ttk.Label(frame1, text="Name:").pack(side=tk.LEFT)
        self.teacher_name = tk.StringVar()
        ttk.Entry(frame1, textvariable=self.teacher_name).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame1, text="Create", command=self.create_teacher).pack(side=tk.LEFT, padx=5)
        
        # list teachers
        ttk.Label(self.content, text="All Teachers:").pack(pady=(20,5))
        self.teacher_list = tk.Listbox(self.content, height=6)
        self.teacher_list.pack(fill=tk.X, pady=5)
        
        # fake data
        self.teacher_list.insert(tk.END, "Mr. Smith")
        self.teacher_list.insert(tk.END, "Ms. Johnson")
        
        ttk.Button(self.content, text="Delete", command=self.delete_teacher).pack(pady=10)
    
    def show_students(self):
        self.clear_content()
        ttk.Label(self.content, text="Manage Students", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # create new student
        frame1 = ttk.Frame(self.content)
        frame1.pack(pady=10)
        
        ttk.Label(frame1, text="Name:").pack(side=tk.LEFT)
        self.student_name = tk.StringVar()
        ttk.Entry(frame1, textvariable=self.student_name).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame1, text="Create", command=self.create_student).pack(side=tk.LEFT, padx=5)
        
        # list students
        ttk.Label(self.content, text="All Students:").pack(pady=(20,5))
        self.student_list = tk.Listbox(self.content, height=6)
        self.student_list.pack(fill=tk.X, pady=5)
        
        # fake data
        self.student_list.insert(tk.END, "Alice")
        self.student_list.insert(tk.END, "Bob")
        self.student_list.insert(tk.END, "Charlie")
        
        ttk.Button(self.content, text="Delete", command=self.delete_student).pack(pady=10)
    
    def create_teacher(self):
        messagebox.showinfo("OK", "Teacher created!")
    
    def create_student(self):
        messagebox.showinfo("OK", "Student created!")
    
    def delete_teacher(self):
        messagebox.showinfo("OK", "Teacher deleted!")
    
    def delete_student(self):
        messagebox.showinfo("OK", "Student deleted!")