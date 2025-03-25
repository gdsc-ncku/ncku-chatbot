import os
import xml.etree.ElementTree as ET

def convert_xml_to_txt(xml_folder):
    for filename in os.listdir(xml_folder):
        if filename.endswith('.xml'):
            xml_file_path = os.path.join(xml_folder, filename)
            txt_file_path = os.path.join(xml_folder, filename.replace('.xml', '.txt'))
            
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            
            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                for elem in root.iter():
                    txt_file.write(f'{elem.tag}: {elem.text}\n')

# Example usage
convert_xml_to_txt('./xml')
