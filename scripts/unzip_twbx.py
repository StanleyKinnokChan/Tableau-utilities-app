import zipfile
import os
import xml.etree.ElementTree as ET
import shutil

def unzip_twbx(file_path):
    file_path = r'{}'.format(file_path)
    twb_file_path = None
    extracted_folder = None

    if file_path.endswith('.twbx'):
        # Create a folder for extraction in the same directory as the file
        extracted_folder = os.path.join(os.path.dirname(file_path), 'unzipped_twbx')
        os.makedirs(extracted_folder, exist_ok=True)
        
        # Unzip the twbx file
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_folder)
        print('The workbook is unzipped.')

    elif file_path.endswith('.twb'):
        # If it's a .twb file, just set the path
        print('This workbook is not packaged. No unzip action can be done.')
    else:
        raise ValueError("The provided file is neither a .twbx nor a .twb file")
