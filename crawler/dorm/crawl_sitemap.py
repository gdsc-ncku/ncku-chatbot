# 將 sitemap 上的東西，除了公告以外的 url 都使用 jina ai reader 下載下來
import requests
import json
from pathlib import Path
from bs4 import BeautifulSoup
from sitemap import generate_sitemap
from dotenv import load_dotenv
from markdownify import markdownify as md

load_dotenv()

SITE_MAP = Path('data/zh/sitemap.json')
OUTPUT_DIR = Path('data/zh/dorm-data')

url = 'https://housing-osa.ncku.edu.tw/p/17-1052.php?Lang=zh-tw'
generate_sitemap(url, 'data/zh/sitemap.json')

if __name__ == '__main__':
    if not OUTPUT_DIR.exists():
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with SITE_MAP.open('r') as f:
        sitemap = json.load(f)

    # 先取出 div classname = 'mcol' 也就是主要的內容，再去解析
    for item in sitemap.values():
        data_text = ''
        if item['name'] == '最新消息':
            continue

        # 例外網站
        if "常見Q&A" in item['name']:
            print(f'正在爬取 {item["name"]}')
            response = requests.get(item['url'].strip())
            soup = BeautifulSoup(response.text, 'html.parser')
            wrap_content = soup.find('article', id='wrap')
            data_text = str(wrap_content.prettify())
            md_text = md(data_text)
            # write to file
            output_file = OUTPUT_DIR / f'{item["name"].replace(" ", "_").strip()}.md'
            output_file.write_text(md_text)
            continue

        # 一般的網站
        if len(item['sub_items']) == 0: 
            print(f'正在爬取 {item["name"]}')
            url = item['url'].strip()
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.find('div', class_='col col_02')
            main_content = content.find('div', id='Dyn_2_2')
            md_text = md(str(main_content))

            # write to file
            output_file = OUTPUT_DIR / f'{item["name"].replace(" ", "_").strip()}.md'
            output_file.write_text(md_text + '\n\n' + data_text)
            continue
        
        # 有子項目的網站
        for sub_item in item['sub_items'].values():
            print(f'正在爬取 {sub_item["name"]}')
            url = sub_item['url'].strip()
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.find('div', class_='col col_02')
            main_content = content.find('div', id='Dyn_2_2')

            data_text = str(main_content.prettify())
            md_text = md(data_text)
            # write to file
            output_file = OUTPUT_DIR / f'{sub_item["name"].replace(" ", "_").strip()}.md'
            output_file.write_text(md_text)