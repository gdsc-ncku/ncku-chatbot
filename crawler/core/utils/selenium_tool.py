
__all__ = ["async_build_drivers", "build_drivers", "get_all_str", "auto_build_wrapper"]

from selenium import webdriver
from bs4 import BeautifulSoup

import functools
import asyncio
import os


async def async_build_drivers(options, num_worker):
    loop = asyncio.get_running_loop()
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=min(num_worker, os.cpu_count())) as executor:
        tasks = [
            loop.run_in_executor(executor, lambda: webdriver.Chrome(options=options))
            for _ in range(num_worker)
        ]
        drivers = await asyncio.gather(*tasks)
    return drivers


def build_drivers(options, num_worker=1):
    drivers = [webdriver.Chrome(options=options) for _ in range(max(num_worker, 1))]
    return drivers


def get_all_str(tab_pane, results):
    _results = results

    html_content = tab_pane.get_attribute("innerHTML")
    soup = BeautifulSoup(html_content, "html.parser")
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

            _results.append(f"\t{label}:\t{value}")
        row.decompose()

    for text in soup.stripped_strings:
        _results.append((f"\t{text}"))

    for img in soup.find_all("img"):
        img_url = img.get("src")
        _results.append((f"\t圖片連結:\t{img_url}"))

    _results.append(("\n"))
    return _results


def auto_build_wrapper(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if hasattr(self, "build_drivers") and callable(getattr(self, "build_drivers")):
            self.build_drivers()

        result = func(self, *args, **kwargs)
        return result
    return wrapper

