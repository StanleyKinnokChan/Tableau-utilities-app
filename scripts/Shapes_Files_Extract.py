import xml.etree.ElementTree as ET
import base64
import os

def Shapes_Files_Extract(xml_file_path,root):
    # Get the directory where the XML file is located
    xml_dir = os.path.dirname(xml_file_path)

    # Create a new directory called 'shapes' in the same directory as xml_file_path
    output_dir = os.path.join(xml_dir, 'shapes')

    # Find all <shape> elements
    shapes = root.findall('.//shape')

    # Create an output directory for the images
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each <shape> element

    for shape in shapes:
        # Get the name attribute and base64 data
        name = shape.attrib.get('name')

        if name is not None and shape.text is not None:
            base64_data = shape.text.strip()
        
            # Decode the base64 data
            image_data = base64.b64decode(base64_data)
        
            # Determine the output file path
            output_file_path = os.path.join(output_dir, name.replace('/', '_').replace(':',''))

            # Save the image to a file
            with open(output_file_path, 'wb') as image_file:
                image_file.write(image_data)
        
            print(f'Saved image to {output_file_path}')
        else:
            pass
    
    print('Image extraction complete.')

if __name__ == '__main__':
    # Usage example
    xml_file_path = r"C:\Users\StanleyChan\SynologyDrive\Tech\python\Tableau related\Tableau utilities app\demo workbook\demo_HR_dashboard_Stanley.twb"
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(xml_file_path, parser=parser)
    root = tree.getroot()
    
    # Extract shapes from workbook
    Shapes_Files_Extract(xml_file_path,root)