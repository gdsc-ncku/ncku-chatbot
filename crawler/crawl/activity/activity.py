
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import re

from crawler.core import SeleniumCrawler
from crawler.utils import read_local_config


config = read_local_config(format="json")

table_condition = config["table_condition"]
act_conditions = config["act_conditions"]
act_re_patten = config["act_re_patten"]
tab_dict = config["tab_dict"]


class ActivityCrawler(SeleniumCrawler):
    def __init__(self, url, url_path, end_str, max_worker=None, headless=True):
        super().__init__(url, url_path, end_str, max_worker, headless)

    def check_all_activity_id(self):
        """
        Check all activity id in the website
        """

        driver = self.drivers[0]

        driver.get(self.url)
        wait = WebDriverWait(driver, self.time_out)

        table_elements = self.wait_until(wait,
                                         EC.element_to_be_clickable((By.CSS_SELECTOR, table_condition))
                                         )

        table_elements.click()

        act_elements = self.wait_until(wait,
                                       EC.presence_of_all_elements_located(
                                           (By.XPATH, act_conditions))
                                       )

        act_ids = [match.group(1)
                  for elem in act_elements
                  if (match := re.search(act_re_patten, elem.get_attribute("id")))
                  ]

        return act_ids


    def extract_act_id(self, driver, act_id, url):
        """
        Extract activity id information
        """
        driver.get(f"{url}{act_id}")

        txt_list = [f"# 活動ID: {act_id}"]

        tab_content = driver.find_elements(By.CLASS_NAME, "tab-content")
        if not tab_content:
            return

        tab_panes = tab_content[0].find_elements(By.CSS_SELECTOR, "div.tab-pane")
        if len(tab_panes) < 1:
            return

        for tab_pane in tab_panes:
            tab_id = tab_pane.get_attribute("id")
            txt_list.append((f"## {tab_dict[tab_id]}:"))
            txt_list = self.get_attribute_str(tab_pane, txt_list)

        return txt_list

    def run(self):
        """
        Run the activity crawler
        return dict: 以Json格式自動儲存到 /save資料夾, 而且會自動整理格式再儲存到 /output資料夾
        return str: 以字串格式回傳自動儲存到 /output資料夾
        """
        act_ids = self.check_all_activity_id() # get all activity id

        # extract all activity id information
        act_url = f"{self.url}{self.url_path}"
        # 原生for loop
        #act_dict = {}
        #for act_id in tqdm(act_ids[:]):
        #    act_txt = self.extract_act_id(self.drivers[0], act_id, self._url)
        #    if act_txt is not None and act_id not in act_dict:
        #        act_dict[act_id] = act_txt

        # 使用自動多線程
        act_dict = self.task_loop(self.extract_act_id, act_ids, act_url)
        return act_dict
