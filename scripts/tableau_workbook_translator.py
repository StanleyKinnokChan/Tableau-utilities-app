import xml.etree.ElementTree as ET
from deep_translator import GoogleTranslator
import re
import os

# Function to translate text while keeping placeholders (e.g., <name>) intact
def translate_with_placeholders(text, translator):
    if text is None:
        return ""
    
    # Regular expression to match placeholders (e.g., <name>)
    placeholder_pattern = r"(<[^>]+>)"
    
    # Split the text into translatable parts and placeholders
    parts = re.split(placeholder_pattern, text)
    
    # Translate only the parts that are not placeholders and are not None
    translated_parts = [
        part if re.match(placeholder_pattern, part) or part is None else translator.translate(part)
        for part in parts
    ]
    
    # Recombine the translated parts and placeholders, ignoring None values
    return ''.join(part for part in translated_parts if part is not None)

# Function to replace text inside <run> tags nested under <zone>, <title>, or <format attr='title'>
def tableau_workbook_translator(file_path, root,source_lang='en', target_lang='zh-TW'):

    # Initialize the Google Translator
    translator = GoogleTranslator(source=source_lang, target=target_lang)

    # Search for <run> elements within <zone>, <title>, or <format attr='title'> elements
    # Finding <zone> and <title> tags
    for zone_or_title in root.findall('.//zone') + root.findall('.//title'):
        # Loop through all <formatted-text> elements within <zone> or <title>
        for formatted_text in zone_or_title.findall('.//formatted-text'):
            # Find the <run> element inside the <formatted-text> element
            run_element = formatted_text.find('run')
            if run_element is not None and run_element.text:
                # Translate the text in <run>, keeping placeholders intact
                translated_text = translate_with_placeholders(run_element.text, translator)
                # Replace the original text with the translated text
                run_element.text = translated_text

    # Finding <format> tags with attr='title'　(filter title)
    for format_elem in root.findall(".//format[@attr='title']"):
        # Loop through all <formatted-text> elements within <format attr='title'>
        for formatted_text in format_elem.findall('.//formatted-text'):
            # Find the <run> element inside the <formatted-text> element
            run_element = formatted_text.find('run')
            if run_element is not None and run_element.text:
                # Translate the text in <run>, keeping placeholders intact
                translated_text = translate_with_placeholders(run_element.text, translator)
                # Replace the original text with the translated text
                run_element.text = translated_text

    # Construct a valid output file path
    base_name = os.path.basename(file_path)
    file_name, file_extension = os.path.splitext(base_name)
    updated_file = os.path.join(os.path.dirname(file_path), f"{file_name}_{target_lang}{file_extension}")

    tree = ET.ElementTree(root)

    # Write the updated XML back to the file
    tree.write(updated_file, encoding='utf-8', xml_declaration=True)
    print(f"Translation complete. Translated workbookS saved as {updated_file}")

# available lang:
# {'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'assamese': 'as', 'aymara': 'ay', 'azerbaijani': 'az', 'bambara': 'bm', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bhojpuri': 'bho', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-CN', 'chinese (traditional)': 'zh-TW', 'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dhivehi': 'dv', 'dogri': 'doi', 'dutch': 'nl', 'english': 'en', 'esperanto': 'eo', 'estonian': 'et', 'ewe': 'ee', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el', 'guarani': 'gn', 'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'iw', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'ilocano': 'ilo', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'kinyarwanda': 'rw', 'konkani': 'gom', 'korean': 'ko', 'krio': 'kri', 'kurdish (kurmanji)': 'ku', 'kurdish (sorani)': 'ckb', 'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lingala': 'ln', 'lithuanian': 'lt', 'luganda': 'lg', 'luxembourgish': 'lb', 'macedonian': 'mk', 'maithili': 'mai', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr', 'meiteilon (manipuri)': 'mni-Mtei', 'mizo': 'lus', 'mongolian': 'mn', 'myanmar': 'my', 'nepali': 'ne', 'norwegian': 'no', 'odia (oriya)': 'or', 'oromo': 'om', 'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'quechua': 'qu', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 'sanskrit': 'sa', 'scots gaelic': 'gd', 'sepedi': 'nso', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'tatar': 'tt', 'telugu': 'te', 'thai': 'th', 'tigrinya': 'ti', 'tsonga': 'ts', 'turkish': 'tr', 'turkmen': 'tk', 'twi': 'ak', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'}

if __name__ == '__main__':
    file_path = r"C:\Users\StanleyChan\SynologyDrive\Tech\Tableau\personal project\Hostpital ER\Hospital ER.twb"
    tree = ET.parse(file_path)
    root = tree.getroot()
    tableau_workbook_translator(file_path, root,'en', 'zh-TW')
