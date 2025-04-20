__all__ = ["SeleniumCrawler"]

from selenium.webdriver.chrome.options import Options

from crawler.utils import async_run
from crawler.core.base_crawler import BaseCrawler
from crawler.core.utils import (
    async_build_drivers,
    async_quit_drivers,
    build_drivers,
    auto_build_wrapper,
    thread_core,
    single_core,
)

from crawler.utils import read_local_config

config = read_local_config(format="yaml")
page_load_strategy = config["page_load_strategy"]


class SeleniumCrawler(BaseCrawler):
    def __init__(self, url, url_path, end_str, num_worker=None, headless=True):
        super().__init__(url, url_path, end_str, num_worker)
        self.headless = headless
        self.options = Options()
        self.options.page_load_strategy = page_load_strategy

        self.options.add_argument("--log-level=1")
        self.options.add_argument("--no-sandbox")  # 增加穩定性
        self.options.add_argument("--disable-dev-shm-usage")  # 避免記憶體問題
        if headless:
            self.options.add_argument("--headless")
            self.options.add_argument("--log-level=3")

        self.drivers = None

    def __init_subclass__(self, **kwargs):
        super().__init_subclass__(**kwargs)
        if "run" in self.__dict__:
            self.run = auto_build_wrapper(self.__dict__["run"])

    def build_drivers(self):
        if self.use_mp:
            self.drivers = async_run(async_build_drivers, self.options, self.num_worker)
        else:
            self.drivers = build_drivers(self.options, self.num_worker)

    @staticmethod
    def wait_until(wait, condition):
        return wait.until(condition)

    def get_tbody_str(self, tbody, results):
        attribute = tbody.get_attribute("innerHTML")
        return super().get_attribute_str(attribute, results)

    def quit(self):
        if self.drivers is None:
            return
        if self.use_mp:
            self.drivers = async_run(async_quit_drivers, self.drivers)
        else:
            for driver in self.drivers:
                driver.quit()

        self.drivers = None

    @auto_build_wrapper
    def run(self):
        raise NotImplementedError

    def load(self):
        """
        檢查在save目錄中是否有已經爬取的數據
        """
        raise NotImplementedError

    def task_loop(self, func, tasks, *args, **kwargs):
        """
        多線程任務
        """
        if self.use_mp:
            # thread_core(self.drivers, func, tasks, *args, **kwargs)
            return thread_core(self.drivers, func, tasks, *args, **kwargs)
        else:
            return single_core(self.drivers, func, tasks, *args, **kwargs)
