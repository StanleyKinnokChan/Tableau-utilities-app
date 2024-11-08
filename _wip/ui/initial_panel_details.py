import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog, messagebox, ttk
import os
import webbrowser
from scripts.read_tableau_to_xml import read_tableau_to_xml
from scripts.Shapes_Files_Extract import Shapes_Files_Extract
from scripts.image_extract import image_extract
from scripts.unzip_twbx import unzip_twbx
from scripts.Tableau_Calculation_Dependencies import Tableau_Calculation_Dependencies
from scripts.workbook_colour_extractor import *
from scripts.tableau_workbook_translator import *
import os
import webbrowser

# Class to redirect stdout to the Text widget
class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, message):
        self.widget.config(state=tk.NORMAL)
        self.widget.insert(tk.END, message)
        self.widget.see(tk.END)  # Scroll to the end
        self.widget.config(state=tk.DISABLED)

    def flush(self):
        pass  # Flush is required for compatibility with stdout

# Wrapper to run each script and capture print output
def run_script_with_output(func):
    console_output.config(state=tk.NORMAL)
    console_output.delete(1.0, tk.END)  # Clear previous output
    console_output.config(state=tk.DISABLED)

    sys.stdout = TextRedirector(console_output)  # Redirect stdout
    try:
        func()
    finally:
        sys.stdout = sys.__stdout__  # Reset stdout back to default

# Function to process files and capture output
def process_file(func, *args):
    file = file_path.get()
    file = r'{}'.format(file)

    if not file:
        print("No file selected")
        return None

    try:
        return func(file, *args)
    except Exception as e:
        print(f"Error processing the file: {e}")
        return None
    
# Function to handle drag and drop
def drop(event):
    file_path.set(event.data.strip('{}'))
    
# Function to browse files
def browse_file():
    file = filedialog.askopenfilename(title="Select a file")
    if file:
        file_path.set(file)

### Function to run Tableau XML parsing
def run_read_tableau_to_xml():
    return process_file(read_tableau_to_xml)

# Script functions
def run_unzip_twbx():
    run_script_with_output(lambda: process_file(unzip_twbx))

def run_Shapes_Files_Extract():
    # Process XML first
    xml_root = run_read_tableau_to_xml()
    if xml_root:
        # Then proceed to extract shapes
        run_script_with_output(lambda: process_file(Shapes_Files_Extract, xml_root))

def run_image_extract():
    return process_file(image_extract)

def run_Tableau_Calculation_Dependencies():
    # Process XML first
    xml_root = run_read_tableau_to_xml()
    if xml_root:
        # Then proceed with calculation dependency analysis
        run_script_with_output(lambda: process_file(Tableau_Calculation_Dependencies, xml_root))

def run_workbook_colour_extractor():
    # Process XML first
    xml_root = run_read_tableau_to_xml()
    if xml_root:
        # Then proceed with calculation dependency analysis
        run_script_with_output(lambda: process_file(workbook_colour_extractor, xml_root))

def run_tableau_workbook_translator():
    # Process XML first
    xml_root = run_read_tableau_to_xml()
    if xml_root:
        # Then proceed with calculation dependency analysis
        run_script_with_output(lambda: process_file(tableau_workbook_translator, xml_root,'en', 'zh-TW'))

####### script_panel
def show_script_panel():

    if not os.path.exists(file_path.get()) or not file_path.get().endswith(('.twb', '.twbx')):
        # Show warning when file path is not valid
        messagebox.showwarning("Invalid File", "Please select a valid workbook (.twb/.twbx).")
        return  # Prevent further execution and do not move to the script panel

    # Hide the initial panel (label, entry, and buttons)
    initial_panel.pack_forget()

    # Create new panel for script execution buttons
    global script_panel
    script_panel = tk.Frame(root)
    script_panel.pack(pady=20, fill="both", expand=True)

    # Heading for the script execution panel
    tk.Label(script_panel, text="What actions you want to perform?", font=("Arial", 14)).pack(pady=10)

    #script
    tk.Button(script_panel, text="Unzip the Package Workbook (.twbx)", command=run_unzip_twbx).pack(pady=5)
    tk.Button(script_panel, text="Extract Shapes", command=run_Shapes_Files_Extract).pack(pady=5)
    tk.Button(script_panel, text="Extract Container Images", command=run_image_extract).pack(pady=5)
    tk.Button(script_panel, text="Calculation Dependency Analysis", command=run_Tableau_Calculation_Dependencies).pack(pady=5)
    tk.Button(script_panel, text="Extract Colour from Workbook", command=run_workbook_colour_extractor).pack(pady=5)
    tk.Button(script_panel, text="Translate Workbook", command=open_language_selection).pack(pady=5)

    # Show the console_output only in the script panel
    global console_output
    console_output = tk.Text(script_panel, height=10, width=70, state=tk.DISABLED)
    console_output.pack(pady=50)

    # Function to display the initial panel again
    def show_initial_panel():
        script_panel.pack_forget()  # Hide the script panel
        initial_panel.pack(pady=20)  # Show the initial panel

    # Add a "Return" button to go back to the initial panel
    return_button = tk.Button(script_panel, text="Return", command=show_initial_panel)
    return_button.pack(pady=10)


def open_language_selection():
    # Define available languages
    languages = {
        'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy',
        'assamese': 'as', 'aymara': 'ay', 'azerbaijani': 'az', 'bambara': 'bm', 'basque': 'eu', 
        'belarusian': 'be', 'bengali': 'bn', 'bhojpuri': 'bho', 'bosnian': 'bs', 'bulgarian': 'bg', 
        'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-CN', 
        'chinese (traditional)': 'zh-TW', 'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 
        'dhivehi': 'dv', 'dogri': 'doi', 'dutch': 'nl', 'english': 'en', 'esperanto': 'eo', 'estonian': 'et', 
        'ewe': 'ee', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy', 'galician': 'gl', 
        'georgian': 'ka', 'german': 'de', 'greek': 'el', 'guarani': 'gn', 'gujarati': 'gu', 'haitian creole': 'ht', 
        'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'iw', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu', 
        'icelandic': 'is', 'igbo': 'ig', 'ilocano': 'ilo', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 
        'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'kinyarwanda': 'rw', 
        'konkani': 'gom', 'korean': 'ko', 'krio': 'kri', 'kurdish (kurmanji)': 'ku', 'kurdish (sorani)': 'ckb', 
        'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lingala': 'ln', 'lithuanian': 'lt', 
        'luganda': 'lg', 'luxembourgish': 'lb', 'macedonian': 'mk', 'maithili': 'mai', 'malagasy': 'mg', 
        'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr', 'meiteilon (manipuri)': 'mni-Mtei', 
        'mizo': 'lus', 'mongolian': 'mn', 'myanmar': 'my', 'nepali': 'ne', 'norwegian': 'no', 'odia (oriya)': 'or', 
        'oromo': 'om', 'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 
        'quechua': 'qu', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 'sanskrit': 'sa', 'scots gaelic': 'gd', 
        'sepedi': 'nso', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 
        'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 
        'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'tatar': 'tt', 'telugu': 'te', 'thai': 'th', 'tigrinya': 'ti', 
        'tsonga': 'ts', 'turkish': 'tr', 'turkmen': 'tk', 'twi': 'ak', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 
        'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'
    }

    # Create a new window for language selection
    language_window = tk.Toplevel(root)
    language_window.title("Select Languages")

    tk.Label(language_window, text="Select Source Language:").pack(pady=5)
    source_language = tk.StringVar(language_window)
    source_language.set('english')  # Default value

    # Create a combobox for the source language
    source_menu = ttk.Combobox(language_window, textvariable=source_language, values=list(languages.keys()), state="readonly")
    source_menu.pack(pady=5)

    tk.Label(language_window, text="Select Target Language:").pack(pady=5)
    target_language = tk.StringVar(language_window)
    target_language.set('chinese (traditional)')  # Default value

    # Create a combobox for the target language
    target_menu = ttk.Combobox(language_window, textvariable=target_language, values=list(languages.keys()), state="readonly")
    target_menu.pack(pady=5)

    text_translation_warning = tk.Label(language_window, text="Noted that it only translates the text in the containers and titles on dashboards, not the data itself", font=("Arial", 9), anchor="w")  # Align text to the left
    text_translation_warning.pack(pady=20, fill='x')  # Use fill='x' to make the label take the full width

    def confirm_selection():
        # Get the language codes based on user selection
        src_lang = languages[source_language.get()]
        tgt_lang = languages[target_language.get()]
        
        # Run the translation process with selected languages
        xml_root = run_read_tableau_to_xml()
        if xml_root:
            run_script_with_output(lambda: process_file(tableau_workbook_translator, xml_root, src_lang, tgt_lang))

        # Close the language selection window after confirming
        language_window.destroy()

    # Add a confirmation button
    tk.Button(language_window, text="Confirm", command=confirm_selection).pack(pady=10)

def initial_panel_details(initial_panel):
    # Create and configure the label to display the file path
    text_header = tk.Label(initial_panel, text='      Tableau Utilities (Beta 1.2)',
                                fg='white', bg='#0876ee', font=('verdana',14,'bold'),
                                width=450, height=1, compound=tk.LEFT,
                                anchor='w')
    text_header.pack(pady=20)

    # Create and configure the label to display the file path
    label = tk.Label(initial_panel, text="Drag and drop a workbook (.twb/.twbx) here", width=60, height=4, bg="lightgray")
    label.pack(pady=10)
 


    # Bind DnD functionality to the label
    label.drop_target_register(DND_FILES)
    label.dnd_bind('<<Drop>>', drop)
    
    # Or text
    tk.Label(initial_panel, text="or", font=("Arial", 8)).pack(pady=5)
            
    # Button to browse files
    tk.Button(initial_panel, text="Browse Workbook", command=browse_file).pack(pady=10)

    # empty space
    tk.Frame(initial_panel, height=60).pack()  # Adjust height as needed

    text_yourWB = tk.Label(initial_panel, text="                     Your selected workbook:", font=("Arial", 8), anchor="w")  # Align text to the left
    text_yourWB.pack(pady=0, fill='x')  # Use fill='x' to make the label take the full width

    # Entry widget to display the file path
    tk.Entry(initial_panel, textvariable=file_path, width=60).pack(pady=10)

    # Confirm Button to proceed to the script panel
    tk.Button(initial_panel, text="Confirm", command=show_script_panel).pack(pady=10)


    ######### Footer Section
    # Copyright Text
    tk.Label(initial_panel, text="Copyright is owned by", font=("Arial", 8)).pack(pady=5)

    # Function to open the URL
    def open_link(event):
        webbrowser.open("https://www.linkedin.com/in/staneykinnok-chan/")

    # Create the hyperlink text label
    hyperlink_text = tk.Label(initial_panel, text="Stanley Chan", fg="blue", cursor="hand2", font=("Arial", 8, "underline"))
    hyperlink_text.pack(pady=5)

    # Bind the click event to the open_link function
    hyperlink_text.bind("<Button-1>", open_link)

    # Construct the image file path
    script_directory = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script


    # image_path = os.path.join(script_directory, '_image', 'Linkedin QR.png')

    # # Load and display the image
    # image = tk.PhotoImage(file=image_path)
    # image_label = tk.Label(initial_panel, image=image)
    # image_label.pack(pady=5)

if __name__ == '__main__':
    file_path = tk.StringVar()
    root = TkinterDnD.Tk()  # TkinterDnD enabled root
    root.title("Tableau Utilities")
    root.geometry("600x650")
    initial_panel = tk.Frame(root)  # Do not chain .pack() here
    initial_panel.pack(pady=10)  # Pack separately to retain reference