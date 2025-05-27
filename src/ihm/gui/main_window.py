import tkinter as tk
from login_view import LoginView

class MainWindow:
    def __init__(self, core_controller):
        self.core = core_controller
        self.root = tk.Tk()
        self.root.title("Clustering de Camarades")
        self.root.geometry("600x400")
        self.current_view = None
        self.show_login()
    
    def clear(self):
        # remove all widgets from window
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login(self):
        self.clear()
        self.current_view = LoginView(self.root, self)
    
    def show_student_views(self, username):
        # switch to student interface
        self.clear()
        from student_views import StudentViews
        self.current_view = StudentViews(self.root, self, username)
    
    def show_teacher_views(self, username):
        # switch to teacher interface
        self.clear()
        from teacher_views import TeacherViews
        self.current_view = TeacherViews(self.root, self, username)
    
    def run(self):
        # start the application main loop
        self.root.mainloop()