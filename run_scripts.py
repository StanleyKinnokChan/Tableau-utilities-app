from scripts.read_tableau_to_xml import read_tableau_to_xml
from scripts.Shapes_Files_Extract import Shapes_Files_Extract
from scripts.image_extract import image_extract
from scripts.unzip_twbx import unzip_twbx
from scripts.Tableau_Calculation_Dependencies import Tableau_Calculation_Dependencies
from scripts.workbook_colour_extractor import *
from scripts.tableau_workbook_translator import *


######### run script
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
