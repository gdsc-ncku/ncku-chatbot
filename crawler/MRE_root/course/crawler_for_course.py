"""
爬 https://course.ncku.edu.tw/index.php?c=qry_all (成大選課系統) by seleniumy
"""

import time
import json
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from rich import print


def setup_driver():
    # 設定 Chrome 選項
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 無頭模式，不會開啟瀏覽器視窗
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # 初始化 webdriver
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def main():
    url = "https://course.ncku.edu.tw/index.php?c=qry_all"
    driver = setup_driver()
    driver.get(url)
    last_height = driver.execute_script("return document.body.scrollHeight")
    print(last_height)

    # 找到所有導航按鈕
    nav_elements = driver.find_elements(By.CLASS_NAME, "btn_dept")
    course_list = [element.text for element in nav_elements if element.text != ""]
    # for i in course_list: print(i)
    # 點擊每個按鈕並收集資料
    data = []

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, "lxml")
    div_elements = soup.find_all("li", class_="btn_dept")
    counter = len(div_elements)

    for course in course_list:
        counter -= 1
        if counter < 0:
            # print(soup)
            break
        try:
            # 使用 XPath 查找按鈕
            button_xpath = f"//li[@class='btn_dept'][contains(text(), '{course}')]"
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, button_xpath))
            )

            # 點擊按鈕
            driver.execute_script("arguments[0].click();", button)
            time.sleep(1)  # 等待頁面載入

            # 解析課程資料
            soup = BeautifulSoup(driver.page_source, "lxml")
            table = soup.find("table", {"id": "A9-table"})

            if table:
                rows = table.find_all("tr")
                for row in rows[1:]:  # 跳過表頭
                    columns = row.find_all("td")
                    course_data = {
                        "系所名稱": columns[0].text.strip(),
                        "系號-序號": columns[1].text.strip(),
                        "年級": columns[2].text.strip(),
                        "類別": columns[3].text.strip(),
                        "科目名稱": columns[4].text.strip().split(" ")[0],
                        "學分": columns[5].text.strip(),
                        "教師姓名": columns[6].text.strip(),
                        "已選課人數/餘額": columns[7].text.strip(),
                        "時間/教室": columns[8].text.strip(),
                        "是否有餘額": "額" not in columns[7].text.strip(),
                    }
                    data.append(course_data)

            print(f"已掃描: {course}")
            driver.back()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//li[@class="btn_dept"]'))
            )

        except Exception as e:
            print(f"處理 {course} 時發生錯誤: {str(e)}")
            continue

    # 關閉瀏覽器
    driver.quit()

    # 儲存資料
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"ncku_courses_11302.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"課程資料已保存至: {filename}")
    print(f"總共收集到 {len(data)} 門課程")


if __name__ == "__main__":
    main()
