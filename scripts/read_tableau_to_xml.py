import zipfile
import os
import xml.etree.ElementTree as ET
import shutil

def read_tableau_to_xml(file_path) -> None:
    file_path = r'{}'.format(file_path)
    twb_file_path = None
    extracted_folder = None

    try:
        if file_path.endswith('.twbx'):
            extracted_folder = 'extracted_twbx'
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extracted_folder)
            for root, dirs, files in os.walk(extracted_folder):
                for file in files:
                    if file.endswith('.twb'):
                        twb_file_path = os.path.join(root, file)
                        break
            if twb_file_path is None:
                raise FileNotFoundError("No .twb file found in the .twbx package")
        elif file_path.endswith('.twb'):
            twb_file_path = file_path
        else:
            raise ValueError("The provided file is neither a .twbx nor a .twb file")

        tree = ET.parse(twb_file_path)
        root = tree.getroot()

        return root
    
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if extracted_folder and os.path.exists(extracted_folder):
            shutil.rmtree(extracted_folder)
