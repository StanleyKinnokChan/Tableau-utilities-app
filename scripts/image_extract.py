import zipfile
import os
import xml.etree.ElementTree as ET
import shutil

def image_extract(file_path) -> None:
    file_path = r'{}'.format(file_path)
    file_dir = os.path.dirname(file_path)
    target_image_folder = os.path.join(file_dir, 'Image')
    extracted_folder = os.path.join(file_dir,'extracted_twbx')
    image_num = 0
    image_file_paths = set()  # Set to store unique param values

    if not os.path.exists(target_image_folder):
        os.makedirs(target_image_folder)

    try:
        if file_path.endswith('.twbx'):

            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extracted_folder)

            image_folder_path = os.path.join(extracted_folder, 'Image')

            if os.path.exists(image_folder_path):

                # Loop through all the files in the directory
                for file_name in os.listdir(image_folder_path):
                    # Create the full path to the file
                    full_file_path = os.path.join(image_folder_path, file_name)

                    # Check if it's a file (not a directory)
                    if os.path.isfile(full_file_path):
                        image_file_paths.add(full_file_path)  # Add the full file path to the set

            else:
                print("Image in the workbook were not found.")

        elif file_path.endswith('.twb'):

            # Get XML
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Iterate through all <zone> tags
            for zone in root.findall('.//zone'):
                param = zone.get('param')

                # Check if the param attribute is a valid file path and if type-v2 is 'bitmap'
                if param and zone.get('type-v2') == 'bitmap':
                    image_file_path = os.path.normpath(param)
                    image_file_paths.add(image_file_path)  # Add to the set (will automatically ignore duplicates)

        else:
            raise ValueError("The provided file is neither a .twbx nor a .twb file")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
                # Loop through the unique params set
        for image_file_path in image_file_paths:
            if os.path.exists(image_file_path):  # Check if the file exists
                file_name = os.path.basename(image_file_path)  # Extract the file name from the path
                destination_path = os.path.join(target_image_folder, file_name)

                # Copy the file to the destination folder if it doesn't already exist there
                if not os.path.exists(destination_path):
                    shutil.copy(image_file_path, destination_path)  # Copy the file
                    image_num += 1
                else:
                    print(f'{file_name} already existed in Image folder.')
            else:
                print(f"Non-existing path: {image_file_path}")

        print(f"{image_num} new images were exported to {target_image_folder}")
        if os.path.exists(extracted_folder):
            shutil.rmtree(extracted_folder)

if __name__ == '__main__':
    xml_file_path = r"C:\Users\StanleyChan\SynologyDrive\Tech\Tableau\personal project\Hostpital ER\Hospital ER.twbx"
    image_extract(xml_file_path)