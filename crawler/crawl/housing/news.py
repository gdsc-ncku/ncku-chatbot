from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from tqdm import tqdm
import re

from crawler.core import SeleniumCrawler, get_all_str


table_condition = 'img[src="images/table.png"]'
act_conditions = '//*[starts-with(@id, "act_") and descendant::span[starts-with(@onclick, "look_act(")]]'
act_re_patten = r'act_(\d+)'

class NewsCrawler(SeleniumCrawler):
    def __init__(self, url, url_path, end_str, max_worker=None, headless=True):
        super().__init__(url, url_path, end_str, max_worker, headless)