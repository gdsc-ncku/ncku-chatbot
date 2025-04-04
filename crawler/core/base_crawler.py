import os
import json

from crawler.utils import inspect_path, makedirs, get_path, read_local_config
from crawler.core.utils import auto_backend_wrapper, get_all_attribute_words

config = read_local_config(format="yaml")
TIMEOUT = config["timeout"]
JSON_DIR = config["json_dir"]
TXT_DIR = config["txt_dir"]


class BaseCrawler:
    def __init__(self, url, url_path, end_str, num_worker=None):
        self.time_out = TIMEOUT
        self.url = url
        self.url_path = url_path
        self.end_str = end_str
        self.num_worker = (
            os.cpu_count()
            if num_worker == "auto"
            else (num_worker if num_worker else 0)
        )

        self.use_mp = self.num_worker > 1

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "run" in cls.__dict__:
            cls.run = auto_backend_wrapper(cls.__dict__["run"])

    def save(self, result):
        project_root, folder, file_name = self.inspect_path()
        if isinstance(result, dict):
            self.save_json(result, project_root, folder, file_name)
            self.output(result)

        elif isinstance(result, str):
            self.save_txt(result, project_root, folder, file_name)

        else:
            raise ValueError("result should be dict or str")

    @staticmethod
    def save_json(result, project_root, folder, file_name):
        save_path = makedirs(project_root, JSON_DIR, folder)
        with open(
            get_path(save_path, f"{file_name}_result.json"), "w", encoding="utf-8"
        ) as js:
            json.dump(result, js, ensure_ascii=False, indent=4)

    @staticmethod
    def save_txt(result, project_root, folder, file_name):
        save_path = makedirs(project_root, TXT_DIR, folder)
        with open(
            get_path(save_path, f"{file_name}_result.txt"), "w", encoding="UTF-8"
        ) as txt:
            txt.write("\n".join(result))

    def output(self, result=None):
        project_root, folder, file_name = self.inspect_path()
        if result is None:
            ## TODO: 這裡要改
            # result = load json
            pass

        elif isinstance(result, dict):
            result = [
                "\n".join(v) + f"\n{self.end_str}\n"
                for v in result.values()
                if v is not None
            ]
            self.save_txt(result, project_root, folder, file_name)

        else:
            raise ValueError("result should be dict")

    def inspect_path(self):
        return inspect_path(self)

    @auto_backend_wrapper
    def run(self):
        raise NotImplementedError

    def quit(self):
        raise NotImplementedError

    def get_attribute_str(self, attribute, results):
        return get_all_attribute_words(attribute, results)
