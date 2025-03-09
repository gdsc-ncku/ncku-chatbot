

__all__ = ["SeleniumCrawler", "get_all_str", ]

from selenium.webdriver.chrome.options import Options

from crawler.utils import async_run
from crawler.core.base_crawler import BaseCrawler
from crawler.core.utils import async_build_drivers, build_drivers, get_all_str, auto_build_wrapper

page_load_strategy = 'eager'


class SeleniumCrawler(BaseCrawler):
    def __init__(self, url, url_path, end_str, num_worker=None, headless=True):
        super().__init__(url, url_path, end_str, num_worker)
        self.headless = headless
        self.options = Options()
        self.options.page_load_strategy = page_load_strategy

        self.options.add_argument('--log-level=1')
        if headless:
            self.options.add_argument("--headless")
            self.options.add_argument('--log-level=3')

        self.drivers = None

    def __init_subclass__(self, **kwargs):
        super().__init_subclass__(**kwargs)
        # 如果子類直接在定義中提供 run() 方法，
        if 'run' in self.__dict__:
            self.run = auto_build_wrapper(self.__dict__['run'])

    def build_drivers(self):
        if self.use_mp:
            self.drivers = async_run(async_build_drivers, self.options, self.num_worker)
        else:
            self.drivers = build_drivers(self.options, self.num_worker)

    @staticmethod
    def wait_until(wait, condition):
        return wait.until(condition)

    def quit(self):
        for driver in self.drivers:
            driver.quit()
        self.drivers = None

    def run(self):
        raise NotImplementedError

    def load(self):
        """
        檢查在save目錄中是否有已經爬取的數據
        """
        raise NotImplementedError

