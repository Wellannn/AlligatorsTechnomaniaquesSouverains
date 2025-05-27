import tkinter as tk
from tkinter import ttk

class StudentViews:
    def __init__(self, parent, main_window, username):
        self.parent = parent
        self.main_window = main_window
        self.username = username
        self.setup_ui()
    
    def setup_ui(self):
        # create header with student name and logout button
        header = ttk.Frame(self.parent)
        header.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(header, text=f"Student: {self.username}", font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        ttk.Button(header, text="Logout", command=self.main_window.show_login).pack(side=tk.RIGHT)
        
        # create navigation buttons
        nav = ttk.Frame(self.parent)
        nav.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(nav, text="Vote", command=self.show_vote).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav, text="Groups", command=self.show_groups).pack(side=tk.LEFT, padx=5)
        
        self.content = ttk.Frame(self.parent)
        self.content.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.show_vote()  # show vote page by default
    
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()
    
    def show_vote(self):
        self.clear_content()
        ttk.Label(self.content, text="Vote Page", font=('Arial', 12, 'bold')).pack(pady=10)
        
        ttk.Label(self.content, text="Choose your top students:").pack()
        
        # dropdown to select students
        self.student_var = tk.StringVar()
        combo = ttk.Combobox(self.content, textvariable=self.student_var, 
                            values=["Student1", "Student2", "Student3"])  # TODO: Get from core
        combo.pack(pady=10)
        
        ttk.Button(self.content, text="Add Vote", command=self.add_vote).pack(pady=5)
        
        self.vote_list = tk.Listbox(self.content, height=6)
        self.vote_list.pack(pady=10, fill=tk.X)
    
    def show_groups(self):
        self.clear_content()
        ttk.Label(self.content, text="Groups Page", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # text area to show groups
        groups_text = tk.Text(self.content, height=12, width=50)
        groups_text.pack(pady=10, fill=tk.BOTH, expand=True)
        groups_text.insert(tk.END, "Group 1: Student1, Student2, Student3\n")
        groups_text.insert(tk.END, "Group 2: Student4, Student5, Student6\n")
        groups_text.config(state=tk.DISABLED)
    
    def add_vote(self):
        # add selected student to vote list
        student = self.student_var.get()
        if student:
            self.vote_list.insert(tk.END, student)