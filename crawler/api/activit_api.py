"""
activity_api.py 的外部接口
"""

__all__ = ["activity_crawler"]

from crawler.crawl.activity import *


def activity_crawler(url, path, end_str, max_worker=None, headless=True):
    crawler = ActivityCrawler(url, path, end_str, max_worker, headless)
    crawler.run()
