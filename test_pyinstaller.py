import tkinter as tk
from tkinter import messagebox

def show_message():
    messagebox.showinfo("Greeting", "Hello, World!")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sample App")
    button = tk.Button(root, text="Click Me", command=show_message)
    button.pack(pady=20)
    root.mainloop()