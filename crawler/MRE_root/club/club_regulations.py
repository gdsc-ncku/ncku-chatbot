import pdfplumber
import requests
import os
from bs4 import BeautifulSoup


def scrape_pdf_link(url):
    # 發送 HTTP GET 請求
    response = requests.get(url)
    response.raise_for_status()

    # 解析 HTML
    soup = BeautifulSoup(response.text, "html.parser")
    table_rows = soup.find_all("table")

    pdf_url_dict = {}
    for table in table_rows:
        for tr in table.find_all("tr"):
            for a_tag in tr.find_all("a", href=True):
                text = a_tag.get_text(strip=True)  # 提取 <a> 內的文字，去掉空格
                href = a_tag["href"]
                pdf_url_dict[text] = href
                print(f"Text: {text}, Href: {href}")

    return pdf_url_dict


def download_pdf(url, output_path):
    try:
        print(f"正在下載：{url}")
        response = requests.get(url, verify=False, timeout=10)
        response.raise_for_status()
        with open(output_path, "wb") as file:
            file.write(response.content)
        print(f"成功下載：{url}")
    except requests.exceptions.RequestException as e:
        print(f"下載失敗：{url}，錯誤：{e}")
        return False
    return True


def pdf_to_text(pdf_path, txt_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            with open(txt_path, "w", encoding="utf-8") as txt_file:
                for page in pdf.pages:
                    txt_file.write(page.extract_text())
                    txt_file.write("\n")
    except Exception as e:
        print(f"解析 PDF 失敗：{pdf_path}，錯誤：{e}")


os.makedirs("regulations_pdfread", exist_ok=True)
os.makedirs("regulations_src", exist_ok=True)
# 設定目標 URL
url = "https://activity-osa.ncku.edu.tw/p/412-1053-3715.php?Lang=zh-tw"
pdf_url_dict = scrape_pdf_link(url)


for pdf_name, pdf_url in pdf_url_dict.items():
    pdf_path = f"regulations_src/{pdf_name}.pdf"
    txt_path = f"regulations_pdfread/{pdf_name}.txt"

    # Download and convert
    download_pdf(pdf_url, pdf_path)
    pdf_to_text(pdf_path, txt_path)
