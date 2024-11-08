import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
from ui.initial_panel_details import initial_panel_details


#### Initialize the main window
root = TkinterDnD.Tk()  # TkinterDnD enabled root
root.title("Tableau Utilities")
root.geometry("600x650")



##### Initial Panel (Drag and Drop, File Selection)
initial_panel = tk.Frame(root)  # Do not chain .pack() here
initial_panel.pack(pady=10)  # Pack separately to retain reference

# Variable to store the file path
file_path = tk.StringVar()

initial_panel_details(initial_panel)


script_panel = tk.Frame(root)
script_panel.pack(pady=20, fill="both", expand=True)



##### Start the Tkinter loop
root.mainloop()