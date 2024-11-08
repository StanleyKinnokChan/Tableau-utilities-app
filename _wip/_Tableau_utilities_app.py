import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
import subprocess  # For running external scripts
from . import read_Tableau_to_xml
from . import Shapes_Files_Extract
from . import unzip_twbx
from . import Tableau_Calculation_Dependencies
import os
import webbrowser

# Initialize the main window
root = TkinterDnD.Tk()  # TkinterDnD enabled root
root.title("Tableau Utilities")
root.geometry("450x600")
print()
# Variable to store the file path
file_path = tk.StringVar()

# Function to browse files
def browse_file():
    file = filedialog.askopenfilename(title="Select a file")
    if file:
        file_path.set(file)

# Function to handle drag and drop
def drop(event):
    file_path.set(event.data.strip('{}'))

# Function to display the initial panel again
def show_initial_panel():
    script_panel.pack_forget()  # Hide the script panel
    initial_panel.pack(pady=20)  # Show the initial panel

# Function to display new panel with buttons to execute different scripts
def show_script_panel():
    # Hide the initial panel (label, entry, and buttons)
    initial_panel.pack_forget()

    # Create new panel for script execution buttons
    global script_panel
    script_panel = tk.Frame(root)
    script_panel.pack(pady=20, fill="both", expand=True)  # Ensure it fills the area properly

    # Heading for the script execution panel
    tk.Label(script_panel, text="Choose a script to execute:", font=("Arial", 14)).pack(pady=10)

    # Button to execute Script 1
    script1_button = tk.Button(script_panel, text="Unzip the package workbook (.twbx)", command=run_unzip_twbx)
    script1_button.pack(pady=5)

    # Button to execute Script 2
    script2_button = tk.Button(script_panel, text="Extract Shapes", command=run_Shapes_Files_Extract)
    script2_button.pack(pady=5)

    # Button to execute Script 3
    script3_button = tk.Button(script_panel, text="Calculation Dependency Analysis", command=run_Tableau_Calculation_Dependencies)
    script3_button.pack(pady=5)

    # Button to execute Script TBC
    scriptTBC_button = tk.Button(script_panel, text="To Be Continue...", command=run_script3)
    scriptTBC_button.pack(pady=5)

    # Add a "Return" button to go back to the initial panel
    return_button = tk.Button(script_panel, text="Return", command=show_initial_panel)
    return_button.pack(pady=50)

# Functions to execute different scripts (replace 'script_path' with actual script paths)
def run_script1():
    script_path = "path_to_script1.py"
    subprocess.run(["python", script_path])

def run_script2():
    script_path = "path_to_script2.py"
    subprocess.run(["python", script_path])

def run_script3():
    print('The next script is under development!')

def process_file(func):
    file = file_path.get()
    file = r'{}'.format(file)

    if not file:
        print("No file selected")
        return None

    try:
        return func(file)
    except Exception as e:
        print(f"Error processing the file: {e}")
        return None

def run_read_tableau_to_xml():
    return process_file(read_Tableau_to_xml)

def run_Shapes_Files_Extract():
    xml_root = run_read_tableau_to_xml()
    if xml_root:
        process_file(lambda file: Shapes_Files_Extract(file, xml_root))

def run_Tableau_Calculation_Dependencies():
    xml_root = run_read_tableau_to_xml()
    if xml_root:
        process_file(lambda file: Tableau_Calculation_Dependencies(file, xml_root))

def run_unzip_twbx():
    process_file(unzip_twbx)




# Initial Panel (Drag and Drop, File Selection)
initial_panel = tk.Frame(root)
initial_panel.pack(pady=20)

# Create and configure the label to display the file path
label = tk.Label(initial_panel, text="Drag and drop a workbook (.twb/.twbx) here or use the button below.", width=60, height=4, bg="lightgray")
label.pack(pady=20)

text_OR = tk.Label(initial_panel, text="or", font=("Arial", 8))
text_OR.pack(pady=5)  # Adjust pady as needed for spacing

# Button to browse files
browse_button = tk.Button(initial_panel, text="Browse Workbook", command=browse_file)
browse_button.pack(pady=10)

# empty space
empty_frame = tk.Frame(initial_panel, height=70)  # Adjust height as needed
empty_frame.pack()

text_yourWB = tk.Label(initial_panel, text="Your selected workbook:", font=("Arial", 8), anchor="w")  # Align text to the left
text_yourWB.pack(pady=0, fill='x')  # Use fill='x' to make the label take the full width

# Entry widget to display the file path
entry = tk.Entry(initial_panel, textvariable=file_path, width=60)
entry.pack(pady=10)

# Confirm Button to proceed to the script panel
confirm_button = tk.Button(initial_panel, text="Confirm", command=show_script_panel)
confirm_button.pack(pady=15)

######### Benchmark
# Text
text_Benchmark = tk.Label(initial_panel, text="Copyright is owned by", font=("Arial", 8))
text_Benchmark.pack(pady=5)  # Adjust pady as needed for spacing

# Function to open the URL
def open_link(event):
    webbrowser.open("https://www.linkedin.com/in/staneykinnok-chan/")  # Replace with your desired URL

# Create the hyperlink text label
hyperlink_text = tk.Label(initial_panel, text="Stanley Chan", fg="blue", cursor="hand2", font=("Arial", 8, "underline"))
hyperlink_text.pack(pady=0)

# Bind the click event to the open_link function
hyperlink_text.bind("<Button-1>", open_link)

# Construct the image file path
script_directory = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
image_path = os.path.join(script_directory, 'image', 'Linkedin QR.png')  # Construct the image path

# Load and display the image
image = tk.PhotoImage(file=image_path)  # For PNG images
image_label = tk.Label(initial_panel, image=image)
image_label.image = image  # Keep a reference to avoid garbage collection
image_label.pack(pady=1)  # Adjust pady as needed for spacing


# Bind DnD functionality to the label
label.drop_target_register(DND_FILES)
label.dnd_bind('<<Drop>>', drop)

# Start the Tkinter loop
root.mainloop()
