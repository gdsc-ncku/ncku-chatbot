"""
     purpose: 爬取成功大學活動報名網站的活動資訊(最小實作)
 """

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from tqdm import tqdm
import re

URL = "https://activity.ncku.edu.tw/"
PATH = "index.php?c=apply&no="
TIMEOUT = 10

tab_dict = {"tabs-1": "活動資訊",
            "tabs-2": "活動簡介",
            "tabs-3": "活動海報", }

END_STR = '=END='

chrome_options = Options()
chrome_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, timeout=TIMEOUT)


def check_act_id(_driver, _wait):
    _driver.get(URL)

    _wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'img[src="images/table.png"]'))
    ).click()

    _elements = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//*[starts-with(@id, "act_") and descendant::span[starts-with(@onclick, "look_act(")]]')
        )
    )

    return _elements


def extract_act_id(_elements):
    extracted_numbers = [
        match.group(1)
        for elem in _elements
        if (match := re.search(r'act_(\d+)', elem.get_attribute("id")))
    ]

    return extracted_numbers


def core(num):
    driver.get(f"{URL}{PATH}{num}")
    results = [f"# 活動ID: {num}"]

    tab_content = driver.find_elements(By.CLASS_NAME, "tab-content")
    if not tab_content:
        return

    tab_panes = tab_content[0].find_elements(By.CSS_SELECTOR, "div.tab-pane")
    if len(tab_panes) < 1:
        return

    for tab_pane in tab_panes:
        tab_id = tab_pane.get_attribute("id")
        html_content = tab_pane.get_attribute("innerHTML")
        soup = BeautifulSoup(html_content, "html.parser")

        results.append((f"## {tab_dict[tab_id]}:"))

        for row in soup.find_all("tr"):
            th = row.find("th")
            td = row.find("td")

            if th and td:
                label = th.get_text(strip=True)
                value = td.get_text(strip=True)
                img_tag = td.find("img")

                if img_tag and img_tag.has_attr("src"):
                    value = img_tag["src"]
                else:
                    a_tag = td.find("a")
                    if a_tag and a_tag.has_attr("href"):
                        value = a_tag["href"]

                results.append(f"\t{label}:\t{value}")
            row.decompose()

        for text in soup.stripped_strings:
            results.append((f"\t{text}"))

        for img in soup.find_all("img"):
            img_url = img.get("src")
            results.append((f"\t圖片連結:\t{img_url}"))

        results.append(("\n"))

    results.append((f"\n{END_STR}\n"))
    results = '\n'.join(results)
    return results


def main(_driver=driver, _wait=wait):
    elements = check_act_id(_driver, _wait)
    extracted_numbers = extract_act_id(elements)

    results = []
    for num in tqdm(extracted_numbers):
        result = core(num)
        if result is not None:
            results.append(result)

    with open("act_results.txt", "w", encoding="UTF-8") as txt:
        txt.write('\n'.join(results))

    driver.quit()


if __name__ == "__main__":
    main()