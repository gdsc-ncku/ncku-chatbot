# 針對住宿規則爬蟲，因為用到 Jina api 為了避免 rate limit error ，所以每三秒才會爬一次，不過規則沒有很多

import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from rich.progress import track

def get_rule_urls(url: str) -> list[tuple[str, str]]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # 找出所有的 <td role="cell"> 並且底下的 a 標籤，用 (url, title) 格式輸出

    result = []
    for td in soup.find_all('td', {'role': 'cell'}):
        a = td.find('a')
        if a:
            result.append(('https://housing-osa.ncku.edu.tw' + a['href'], a.text.strip()))
    return result

def pdf2markdown(url: str, title: str) -> str:
    # 使用 jina reader api 下載
    # 用法 https://r.jina.ai/{url}
    response = requests.get(f"https://r.jina.ai/{url}")
    return response.text

def main():
    dorm_rules_url = "https://housing-osa.ncku.edu.tw/p/412-1052-2541.php?Lang=zh-tw"
    store_dir = Path('data/zh/dorm-rules')
    store_dir.mkdir(parents=True, exist_ok=True)
    rules = get_rule_urls(dorm_rules_url)
    for rule in track(rules, description="Processing rules"):
        markdown = pdf2markdown(rule[0], rule[1])
        # write to file
        file_path = store_dir / f'{rule[1]}.md'
        file_path.write_text(markdown, encoding='utf-8')
        time.sleep(3)


if __name__ == "__main__":
    main()