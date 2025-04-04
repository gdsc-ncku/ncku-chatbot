import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import urllib.parse
import re

# Add error handling for the request
try:
    url = "https://r.jina.ai/https://web.ncku.edu.tw/p/412-1000-166.php?Lang=zh-tw"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
except requests.RequestException as e:
    print(f"Error fetching the URL: {e}")
    exit(1)

response.encoding = "UTF-8"

soup = BeautifulSoup(response.text, "html.parser")


# Create a safe filename from the URL
def create_safe_filename(url):
    # Parse the URL and get the path
    parsed_url = urllib.parse.urlparse(url)

    # Remove protocol and replace non-alphanumeric characters with underscores
    filename = re.sub(r"[^\w\-_\.]", "_", parsed_url.netloc + parsed_url.path)

    # Ensure the filename ends with .xml
    if not filename.endswith(".xml"):
        filename += ".xml"

    return filename


# Convert BeautifulSoup object to XML using xml.etree.ElementTree
root = ET.Element("root")
root.text = soup.prettify()

# Create an ElementTree and write to file with the URL-derived filename
filename = create_safe_filename(url)
tree = ET.ElementTree(root)
tree.write(filename, encoding="UTF-8", xml_declaration=True)

print(f"XML file saved as: {filename}")
