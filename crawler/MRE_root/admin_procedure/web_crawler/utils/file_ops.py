import xml.etree.ElementTree as ET
import urllib.parse
import re
import os

def create_safe_filename(base_url):
    # Create a safe filename from the given base URL
    parsed_url = urllib.parse.urlparse(base_url)
    filename = re.sub(r'[^\w\-\_\.]', '', parsed_url.netloc + parsed_url.path)  # 支援網址檔名
    if not filename.endswith('.xml'):
        filename += '.xml'
    return filename

def save_xml(content, filename):
    # Save the content as an XML file
    root = ET.Element('root')
    root.text = content
    tree = ET.ElementTree(root)
    os.makedirs('./xml', exist_ok=True)
    tree.write(f'./xml/{filename}', encoding='UTF-8', xml_declaration=True)
