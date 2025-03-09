# 這個檔案專門用來處理新聞、最新活動的爬蟲

import time
import requests
import json
import base64
import datetime
from pathlib import Path

from bs4 import BeautifulSoup
from rich import print
from rich.progress import track
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

load_dotenv()

url = 'https://housing-osa.ncku.edu.tw/p/406-1052-275273,r406.php?Lang=zh-tw'


def scroll_to_bottom(driver, end_date='2022-12-31'):
    """如果 scroll_times 為 0，則直接滾動到底部"""
    old_height = driver.execute_script("return document.body.scrollHeight")
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Wait for content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if old_height == new_height:
            break
        old_height = new_height

        # check date
        try:
            # Find all date elements and get the last one
            date_elements = driver.find_elements(By.CLASS_NAME, "mdate")
            if not date_elements:
                continue

            current_date = date_elements[-1].text.strip()
            current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d').date()
            if current_date < end_date:
                print(f"Reached date boundary: {current_date} is outside range {end_date}")
                break
        except ValueError as e:
            print(f"Date conversion error: {e}")
            continue
        except Exception as e:
            print(f"Error processing date: {e}")
            continue
    return


def encode_image(image_obj):
    # Convert PIL Image to bytes
    import io
    buffered = io.BytesIO()
    image_obj.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def extract_news_data(html):
    """Extract news data from the HTML content"""
    soup = BeautifulSoup(html, 'html.parser')
    news_items = []

    # Find all news items
    articles = soup.find_all('div', class_='mtitle')

    for article in articles:
        try:
            # Extract title and link
            link_elem = article.find('a')
            title = link_elem.text.strip() if link_elem else ''
            link = link_elem['href'] if link_elem else ''

            # Extract date
            date_elem = article.find('i', class_='mdate')
            date = date_elem.text.strip() if date_elem else ''

            news_items.append({
                'title': title,
                'link': link,
                'date': date
            })
        except Exception as e:
            print(f"Error extracting news item: {e}")

    return news_items


def extract_single_news_data(url, news_name):
    """
    將單一新聞下載下來，包含裡面的附件
    """
    # 先使用 requst 檢查 page 裡面有沒有 "module module-ptattach" 這個 class，這個 class 代表有附件，要額外下載
    base_url = '/'.join(url.split('/')[:3])  # 保留前三個
    markdown_text = ""
    appendix_text = ""

    if not url.startswith(base_url):
        url = base_url + url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title_and_content = soup.find('section', class_='mb')

    # get title
    title = title_and_content.find('div', class_='mpgtitle').text.strip()

    # get content
    content = title_and_content.find('div', class_='mcont').text.strip()
    markdown_text += f"# {title}\n\nurl: {url}\n\n{content}"

    if "module module-ptattach" in response.text:
        # 如果有附件，則下載
        print("有附件，append 到 markdown 中")
        # 找到底下的 mptattach 的 ul
        soup = BeautifulSoup(response.text, 'html.parser')
        mptattach = soup.find('ul', class_='mptattach')
        if mptattach:
            # 找到所有的 a 標籤
            links = mptattach.find_all('a')
            for index, link in enumerate(links):
                # 下載檔案
                file_url = link['href']
                file_name = link.text
                # 用 "附件 index: " + link.text : url 的方式來命名，加入到 appendix_text 中
                appendix_text += f"附件 {index + 1}: [{link.text}]({base_url + file_url})\n"

                # TODO: 之後可能可以用 OpenAI vision API 將 pdf 轉成 markdown，目前單純用連結 (因為效果差)
                # pdf_to_image_to_gpt_summary(file_name)

    # save response to file
    file_path = Path(f'{news_name}.md')
    file_path.touch(exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_text + '\n\n' + appendix_text)


# function: 將 news_item 中的每一個東西，使用 extract_single_news_data 函式下載下來，放到 data/zh/news 目錄下
def download_news(news_items, directory='data/zh/news'):
    """Download news items and save them as markdown files in the specified directory.

    Args:
        news_items (list): List of dictionaries containing news information
        directory (str): Target directory for saving the files
    """
    # Create directory if it doesn't exist
    save_dir = Path(directory)
    save_dir.mkdir(parents=True, exist_ok=True)

    for news_item in track(news_items):
        try:
            # Sanitize filename by replacing invalid characters
            safe_title = "".join(c for c in news_item['title'] if c.isalnum() or c in (' ', '-', '_'))
            safe_title = safe_title.strip()
            file_path = save_dir / f"{safe_title}_{news_item['date']}"
            extract_single_news_data(
                url=news_item['link'],
                news_name=str(file_path)
            )
            print(f"fetching: {news_item['title']}")
        except Exception as e:
            print(f"Error downloading {news_item['title']}: {e}")
            continue


def news_list_crawler(
        url='https://housing-osa.ncku.edu.tw/p/403-1052-406-1.php?Lang=zh-tw',
        headless=True,
        end_date='2023-01-01',
):
    """
    將公告頁面的標題和連結爬下來
    """
    print(f"開始爬取公告頁面的標題和連結: {url}")
    # 設定 Chrome Options
    options = Options()
    if headless:
        options.add_argument('--headless')  # 啟用 headless 模式
    options.add_argument('--disable-gpu')  # 某些系統需要此設定
    options.add_argument('--no-sandbox')  # 增加穩定性
    options.add_argument('--disable-dev-shm-usage')  # 避免記憶體問題

    # 先將所有公告爬下來
    driver = webdriver.Chrome(options=options)
    try:
        # Load page
        driver.get(url)

        # Wait for the main content to load
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mtitle"))
        )

        # Scroll to load all content
        scroll_to_bottom(driver, end_date=end_date)

        # Get the final HTML content
        html = driver.page_source

        # Extract news data
        news_items = extract_news_data(html)

        # filter news by date
        news_items = [item for item in news_items if item['date'] > end_date]

        print(f"Successfully extracted {len(news_items)} news items")

        # Save news data to a json file
        with open('news_data.json', 'w', encoding='utf-8') as f:
            json.dump(news_items, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    return news_items


if __name__ == "__main__":
    news_url = 'https://housing-osa.ncku.edu.tw/p/403-1052-406-1.php?Lang=zh-tw'
    news_path = Path('data/zh/news')
    news_activity_url = 'https://housing-osa.ncku.edu.tw/p/403-1052-407-1.php?Lang=zh-tw'
    news_activity_path = Path('data/zh/news-activity')

    # 住宿服務組公告
    news_items = news_list_crawler(
        url=news_url,
        headless=True,
        end_date='2023-12-31'
    )

    # 下載所有公告
    download_news(news_items, directory=news_path)

    # 住宿活動公告
    news_items = news_list_crawler(
        url=news_activity_url,
        headless=True,
        end_date='2023-12-31'
    )

    # 下載所有公告
    download_news(news_items, directory='data/zh/news-activity')