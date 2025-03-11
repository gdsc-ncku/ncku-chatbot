# 用法：使用 F12 工具將住宿服務組的「業務分類」選起來，將 html section 複製到 business_classification.py 這個檔案中
import os
import time

from pathlib import Path
import json

import requests
from bs4 import BeautifulSoup
from rich import print
from rich.progress import track
from dotenv import load_dotenv

load_dotenv()

html_section = """
 <section class="mb">
 		<ul class="cgmenu list-group dropmenu-right" id="ab2fba95161b0e343a47b098f22170dd3_MenuTop">


 			<li class="list-group-item dropdown" id="Menu_490">
 				<a title="宿舍申請" class="" href="/p/412-1052-8196.php?Lang=zh-tw">宿舍申請

 				</a>

 			</li>


 			<li class="list-group-item dropdown" id="Menu_1932">
 				<a title="110-113續住試辦計劃" class="" href="/p/412-1052-26375.php?Lang=zh-tw">110-113續住試辦計劃

 				</a>

 			</li>


 			<li class="list-group-item dropdown" id="Menu_491">
 				<a title="住宿費減免" class="" href="/p/412-1052-2587.php?Lang=zh-tw">住宿費減免

 				</a>

 			</li>


 			<li class="list-group-item dropdown" id="Menu_539">
 				<a title="宿舍餐廳" class="" href="/p/412-1052-4084.php?Lang=zh-tw">宿舍餐廳

 				</a>

 			</li>


 			<li class="list-group-item dropdown" id="Menu_1500">
 				<a title="工程類進度(另開新視窗)" class="" href="/p/403-1052-2796.php?Lang=zh-tw" target="_blank">工程類進度

 				</a>

 			</li>


 			<li class="list-group-item dropdown" id="Menu_2624">
 				<a title="東寧宿舍興建" class="" href="/p/403-1052-3474.php?Lang=zh-tw">東寧宿舍興建

 				</a>

 			</li>


 			<li class="list-group-item dropdown" id="Menu_836">
 				<a title="宿舍自修室" class="" href="/p/412-1052-18841.php?Lang=zh-tw">宿舍自修室

 				</a>

 			</li>


 			<li class="list-group-item dropdown" id="Menu_3004">
 				<a title="宿舍簡易廚房" class="" href="/p/412-1052-30526.php?Lang=zh-tw">宿舍簡易廚房

 				</a>

 			</li>


 			<li class="list-group-item dropdown" id="Menu_837">
 				<a title="服務學習三" class="" href="/p/412-1052-3317.php?Lang=zh-tw">服務學習三

 				</a>

 			</li>


 			<li class="list-group-item dropdown" id="Menu_838">
 				<a title="宿舍會議記錄" class="" href="/p/412-1052-2436.php?Lang=zh-tw">宿舍會議記錄

 				</a>

 			</li>


 			<li class="list-group-item dropdown" id="Menu_888" onmouseover="fixMenuPosition2(this,'Menul_888',0,0,'menu')">
 				<a role="button" aria-expanded="false" onfocus="fixMenuPosition2(this,'Menul_888',0,0,'menu',1)" title="活動花絮" class="dropdown-toggle" href="javascript:void(0)">活動花絮
 					<b class="caret"></b>
 				</a>

 					<ul id="Menul_888" class="dropdown-menu dropmenu-right">



 								<li id="Menu_2840"><a title="2022年" href="/p/412-1052-29453.php?Lang=zh-tw">2022年</a></li>




 								<li id="Menu_2839"><a title="2021年" href="/p/412-1052-29452.php?Lang=zh-tw">2021年</a></li>




 								<li id="Menu_1461"><a title="國際美食烹飪比賽" href="/p/412-1052-23428.php?Lang=zh-tw">國際美食烹飪比賽</a></li>




 								<li id="Menu_892"><a title="宿舍國際嘉年華" href="/p/412-1052-5930.php?Lang=zh-tw">宿舍國際嘉年華</a></li>




 								<li id="Menu_893"><a title="愛與地球相遇在成大" href="/p/412-1052-6080.php?Lang=zh-tw">愛與地球相遇在成大</a></li>




 								<li id="Menu_890"><a title="品德教育" href="/p/412-1052-2637.php?Lang=zh-tw">品德教育</a></li>


 					</ul>

 			</li>


 			<li class="list-group-item dropdown" id="Menu_1952">
 				<a title="宿舍財務資訊" class="" href="/p/412-1052-26390.php?Lang=zh-tw">宿舍財務資訊

 				</a>

 			</li>

 		</ul>
 	</section>
 """


def get_business_classification_dict(html: str) -> dict[str, str]:
    """用 beautiful soup 去取得名稱和連結的 dictionary"""
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.find('ul', id="ab2fba95161b0e343a47b098f22170dd3_MenuTop")
    li_list = ul.find_all('li')
    result = {}
    for li in li_list:
        a = li.find('a')
        result[a['title']] = a['href']
    return result


def store_in_json(data: dict[str, str], path: Path) -> None:
    """將 dictionary 存入 JSON 文件"""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_markdown_from_url(url: str, api_key: str) -> str:
    """從網址取得 markdown，使用 jina reader api，用法為 https://r.jina.ai/{target_url} """
    jina_url = f"https://r.jina.ai/https://housing-osa.ncku.edu.tw{url}"
    print(f"url: {url}")
    try:
        response = requests.get(jina_url)
        if response.status_code != 200:
            response = requests.get(jina_url)
        return response.text
    except Exception as e:
        print(f"Error fetching markdown: {e}")
        return ""


# 寫一個把 json 檔案中所有連結的用 jina reader api 轉換成 markdown，然後再用這個 json 的 key 當作檔案名稱，存到 data/zh/business_classification/ 底下
def store_md_into_file(json_path: Path, md_path: Path) -> None:
    with json_path.open('r', encoding='utf-8') as f:
        data = json.load(f)
    md_path.mkdir(parents=True, exist_ok=True)

    # 因為 20 RPM 限制，所以每 20 個連結 sleep 一下
    # 如果有提供可以用的 API Key，那就會是 200 RPM
    for key, value in track(data.items(), description="Fetching markdown..."):
        print("fetching: ", key)
        md = get_markdown_from_url(value, os.getenv("JINA_API_KEY"))
        # touch file
        file_path = md_path / f'{key}.md'
        file_path.touch(exist_ok=True)
        file_path.write_text(md, encoding='utf-8')
        time.sleep(2)


if __name__ == "__main__":
    md_path = Path('data/zh/business_classification')
    json_path = Path('data/zh/business_classification.json')

    # 先把業務分類存成 json
    store_in_json(get_business_classification_dict(html_section), json_path)

    # 再把網站轉換成 md 存成多個檔案
    store_md_into_file(json_path, md_path)