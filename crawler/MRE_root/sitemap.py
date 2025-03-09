import requests
from bs4 import BeautifulSoup
import json
import os

def generate_sitemap(url, output_path='data/sitemap.json'):
    """
    生成網站地圖並保存為JSON文件
    
    Args:
        url (str): 要爬取的網址
        output_path (str): 輸出JSON文件的路徑，默認為 'data/sitemap.json'
    
    Returns:
        dict: 生成的網站地圖字典，如果失敗則返回 None
    """
    try:
        # 發送請求
        response = requests.get(url)
        
        # 確認請求成功
        if response.status_code != 200:
            print(f"請求失敗，狀態碼：{response.status_code}")
            return None
            
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 提取主要內容
        content = soup.find("section", class_="mb")
        if not content:
            print("無法找到指定內容")
            return None
            
        # 找出所有超連結
        links = content.find_all("a")
        menu_dict = {}
        current_main = None
        
        for link in links:
            text = link.text.strip()
            link_url = link['href']
            
            # 檢查是否為主項目 (不含 '-')
            if '-' not in text:
                # 取得項目編號和名稱
                num = text.split('.')[0].strip()
                name = text.split('.')[1].strip()
                menu_dict[num] = {
                    'name': name,
                    'url': link_url,
                    'sub_items': {}
                }
                current_main = num
            else:
                # 處理子項目
                if current_main:
                    sub_num = text.split('.')[0].strip()
                    sub_name = text.split('.')[1].strip()
                    menu_dict[current_main]['sub_items'][sub_num] = {
                        'name': sub_name,
                        'url': link_url
                    }
        
        # 確保輸出目錄存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 將結果寫入 JSON 文件
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(menu_dict, f, ensure_ascii=False, indent=2)
        print(f"網站地圖已保存到 {output_path}")

        return menu_dict
        
    except Exception as e:
        print(f"發生錯誤：{str(e)}")
        return None

if __name__ == '__main__':
    # # 目標網址
    target_url_zh = "https://housing-osa.ncku.edu.tw/p/17-1052.php?Lang=zh-tw"
    target_url_en = "https://housing-osa.ncku.edu.tw/p/17-1052.php?Lang=en"
    generate_sitemap(target_url_zh, 'data/zh/sitemap.json')