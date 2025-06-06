import tkinter as tk
from src.ihm.gui.login_view import LoginView
from src.service.auth_service import AuthService
from src.service.storage_service import StorageService
from src.ihm.gui.student_views import StudentViews
from src.ihm.gui.owner_views import OwnerViews
from src.ihm.gui.teacher_views import TeacherViews
from src.storage.storage_json import StorageJSON

class MainWindow:
    def __init__(self):
        self.storage_service = StorageService()
        self.auth_service = AuthService(storage=self.storage_service)
        
        self.root = tk.Tk()
        self.root.title("Clustering de Camarades")
        self.root.geometry("800x600")
        self.show_login()
    
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login(self):
        self.clear()
        LoginView(self.root, self)
    
    def show_student_views(self, username):
        self.clear()
        StudentViews(self.root, self, username)
    
    def show_teacher_views(self, username):
        self.clear()
        TeacherViews(self.root, self, username)
    
    def show_owner_views(self, username):
        self.clear()
        OwnerViews(self.root, self, username)
    
    def run(self):
        self.root.mainloop()