import tkinter as tk
from tkinter import ttk

def main():
    root = tk.Tk()
    root.title("Test Tkinter")

    ttk.Label(root, text="Tkinter fonctionne !").pack(padx=20, pady=20)
    ttk.Button(root, text="Fermer", command=root.destroy).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()