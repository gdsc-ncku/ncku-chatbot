import requests
from bs4 import BeautifulSoup

def fetch_url_content(url):
    # Fetch content from the given URL
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'UTF-8'
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

def fetch_suburls(url):
    # Fetch sub-URLs from the given URL
    response = requests.get(url)

    # 檢查請求狀態
    if response.status_code == 200:
        print(f"Successfully fetched.")

    # 解析網頁內容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取所有連結
    links = []
    for a in soup.find_all('a', href=True):
        link = a['href']
        if link.startswith('http'):
            links.append(link)
        elif link.startswith('/'):
            links.append(f"{url.rstrip('/')}{link}")
        else:
            links.append(f"{url.rstrip('/')}/{link}")
    return links

if __name__ == "__main__":
    main_url = "https://www.google.com/"
    print(fetch_suburls(main_url))