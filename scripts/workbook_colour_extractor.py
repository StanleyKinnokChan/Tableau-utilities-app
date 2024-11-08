import re
import xml.etree.ElementTree as ET
import os
import colorsys
import math
import matplotlib.pyplot as plt

# Function to convert hex to RGB
def hex_to_rgb(hex_codes):
    # Function to convert hex color codes to RGB values normalized to the range [0, 1]
    from matplotlib.colors import hex2color
    
    # Convert hex codes to RGB values and create a nested list
    rgb_values = [list(hex2color(hex_code)) for hex_code in hex_codes]
    return rgb_values

# Step sorting at https://www.alanzucconi.com/2015/09/30/colour-sorting/
def step (r,g,b, repetitions=1):
    lum = math.sqrt( .241 * r + .691 * g + .068 * b )

    h, s, v = colorsys.rgb_to_hsv(r,g,b)

    h2 = int(h * repetitions)
    lum2 = int(lum * repetitions)
    v2 = int(v * repetitions)

    return (h2, lum, v2)

# Function to convert RGB to hex
def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))


def workbook_colour_extractor(file_path,root):

    xml_dir = os.path.dirname(file_path)
    output_dir = os.path.join(xml_dir, 'colours')
    os.makedirs(output_dir, exist_ok=True)
    output_html_path = os.path.join(output_dir ,'colour palette generated from wb.html')

    """Extracts unique hex codes from an XML file."""
    hex_pattern = r'#(?:[0-9a-fA-F]{3}){1,2}\b'  # Pattern to match hex codes

    hex_codes = set()  # Set to avoid duplicates
    
    # Find all text that matches the hex pattern in the XML
    for elem in root.iter():
        if elem.text:
            hex_codes.update(re.findall(hex_pattern, elem.text))
        if elem.tail:
            hex_codes.update(re.findall(hex_pattern, elem.tail))
            
    hex_codes = list(hex_codes)
    rbg_codes = hex_to_rgb(hex_codes)
    rbg_codes.sort(key=lambda rgb: step(rgb[0], rgb[1], rgb[2], 8))
    # Convert sorted colours to hex format
    hex_codes = [rgb_to_hex(colour) for colour in rbg_codes]

    """Generates an HTML file displaying hex codes as colored squares."""
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hex Color Display</title>
        <style>
            body { font-family: Arial, sans-serif; display: flex; flex-wrap: wrap; gap: 15px; padding: 20px; background-color: #f9f9f9; }
            .color-square {
                width: 60px; height: 60px; cursor: pointer; border: 1px solid #ccc; display: flex; align-items: center; justify-content: center; 
                border-radius: 5px; position: relative;
            }
            .tooltip {
                visibility: hidden; position: absolute; bottom: 100%; left: 50%; transform: translateX(-50%);
                background-color: #333; color: #fff; padding: 5px; border-radius: 3px; font-size: 12px; white-space: nowrap;
            }
            .color-square:hover .tooltip { visibility: visible; }
            .notification { display: none;
                position: fixed;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                background-color: #333;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                z-index: 1000; }
        </style>
        <script>
            function copyToClipboard(hexCode) {
                navigator.clipboard.writeText(hexCode).then(() => {
                    const notification = document.getElementById('notification');
                    notification.innerText = `${hexCode} copied to clipboard!`;
                    notification.style.display = 'block';
                    setTimeout(() => { notification.style.display = 'none'; }, 2000);
                }).catch(err => console.error('Error copying text: ', err));
            }
        </script>
    </head>
    <body>
        <div id="notification" class="notification"></div>
    """

    # Add a div for each hex color
    for hex_code in hex_codes:
        html_template += f"""
        <div class="color-square" onclick="copyToClipboard('{hex_code}')" style="background-color: {hex_code}">
            <span class="tooltip">{hex_code}</span>
        </div>
        """

    # Closing tags
    html_template += """
    </body>
    </html>
    """

    # Write the HTML content to the specified output file
    with open(output_html_path, 'w') as file:
        file.write(html_template)
    print(f"HTML file created at {output_html_path}")


if __name__ == '__main__':
    # Usage example
    xml_file_path = r"C:\Users\StanleyChan\SynologyDrive\Tech\python\Tableau related\Tableau utilities app\demo_packed.twb"  # Replace with your XML file path
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(xml_file_path, parser=parser)
    root = tree.getroot()
    
    # Extract hex codes and generate HTML
    workbook_colour_extractor(xml_file_path,root)

