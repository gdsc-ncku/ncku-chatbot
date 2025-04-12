import os
import time
import csv
import requests
from rich import print
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


# 基本設定
URL = "https://sys.activity-osa.ncku.edu.tw/index.php?c=club0408"
POST_URL = "https://sys.activity-osa.ncku.edu.tw/index.php?c=club0408&m=get_details"

HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}

KEYMAP = {
    "name_c": "社團名稱(中)",
    "name_e": "社團名稱(En)",
    "leader_name_c": "社長姓名(中)",
    "leader_name_e": "社長姓名(英)",
    "email": "社團 Email",
    "name": "輔導老師",
    "goal": "社團宗旨",
    "introduce": "社團簡介",
    "acttime": "例行活動時間",
    "actplace": "主要活動場地",
    "url": "社團網頁網址",
    "state": "社團狀態",
    "category": "社團性質",
}

FIELDNAMES = list(KEYMAP.values())

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "club_data")


def fetch_club_detail(club_id, club_state, cat_name):
    try:
        res = requests.post(POST_URL, headers=HEADERS, data=f"id={club_id}", timeout=10)
        result = res.json()
        renamed_result = {KEYMAP.get(k, k): v for k, v in result["data"].items()}
        renamed_result["社團狀態"] = club_state
        renamed_result["社團性質"] = cat_name
        return renamed_result
    except Exception as e:
        print(f"[Error] Fetch club_id={club_id} failed: {e}")
        return None


def crawl_category(driver, cat_id, cat_name, index):
    print(f"[INFO] 處理類別: {cat_name} ({cat_id})")
    Select(driver.find_element(By.CLASS_NAME, "form-select")).select_by_index(index)
    time.sleep(2)

    driver.find_element(By.XPATH, "//button[contains(text(), '查詢')]").click()
    time.sleep(2)

    rows = driver.find_elements(By.CSS_SELECTOR, ".grid_data tr")
    club_list, fail_list = [], []

    for row in rows:
        try:
            club_state = row.find_elements(By.TAG_NAME, "td")[3].text
            club_id = row.find_element(
                By.XPATH, ".//button[contains(text(), '檢視')]"
            ).get_attribute("value")
            print(f"[INFO] Fetching club_id={club_id}")
            data = fetch_club_detail(club_id, club_state, cat_name)
            if data:
                club_list.append(data)
            else:
                fail_list.append((club_state, club_id))
            time.sleep(0.5)
        except Exception as e:
            print(f"[Error] Get club_id failed: {e}")
            continue

    print(f"[INFO] Retry {len(fail_list)} failed clubs")
    for club_state, club_id in fail_list:
        data = fetch_club_detail(club_id, club_state, cat_name)
        if data:
            club_list.append(data)
        time.sleep(1)

    return club_list


def init_driver():
    options = Options()
    options.add_argument("--incognito")
    return webdriver.Chrome(options=options)


def main():
    os.makedirs(DATA_PATH, exist_ok=True)

    driver = init_driver()
    driver.get(URL)
    time.sleep(2)

    select_obj = Select(driver.find_element(By.CLASS_NAME, "form-select"))
    categories = [
        (opt.get_attribute("value"), opt.text.strip())
        for opt in select_obj.options
        if opt.get_attribute("value")
    ]

    print(f"[INFO] 類別清單: {categories}")

    for idx, (cat_id, cat_name) in enumerate(categories):
        club_list = crawl_category(driver, cat_id, cat_name, idx)

        if club_list:
            file_path = os.path.join(DATA_PATH, f"club_{cat_id}.csv")
            with open(file_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
                writer.writeheader()
                writer.writerows(club_list)
            print(f"[SUCCESS] Save to club_{cat_id}.csv ({len(club_list)} clubs)")
        else:
            print(f"[WARNING] No data found in {cat_name} ({cat_id})")

    driver.quit()


if __name__ == "__main__":
    main()
