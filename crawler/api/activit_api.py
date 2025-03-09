
"""
activity_api.py 的外部接口
"""


__all__ = ['activity_crawler']

from crawler.crawl.activity import *

def activity_crawler(url, path, end_str, max_worker=None, headless=True):
    crawler = ActivityCrawler(url, path, end_str, max_worker, headless)
    crawler.run()

if __name__ == "__main__":
    URL = "https://activity.ncku.edu.tw/"
    PATH = "index.php?c=apply&no="
    END_STR = '=END='

    activity_crawler(URL, PATH, END_STR, headless=False)