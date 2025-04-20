import json
import yaml


import asyncio
import inspect
import os

from crawler.config import PROJECT_ROOT, DEFAULT_CONFIG_FORMAT


def async_run(async_func, *args, **kwargs):
    coroutine = async_func(*args, **kwargs)
    try:
        # 檢查是否已有正在運行的 event loop
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # 非同步環境：回傳 coroutine，由呼叫端來 await
        return coroutine
    else:
        # 同步環境：直接執行 coroutine，並回傳結果
        return asyncio.run(coroutine)


def inspect_path(obj_or_cls=None, stack_level=1, return_folder_root=False):
    """
    接收一個對象或類別，返回該類別定義所在的檔案名稱
    """
    if obj_or_cls is None:
        caller_frame = inspect.stack()[stack_level]
        file_path = caller_frame.filename

    else:
        cls = obj_or_cls if isinstance(obj_or_cls, type) else obj_or_cls.__class__
        file_path = inspect.getfile(cls)

    folder = os.path.dirname(file_path)
    folder = os.path.basename(folder) if not return_folder_root else folder
    file_name = os.path.basename(file_path).split(".")[0]

    return PROJECT_ROOT, folder, file_name


def get_path(root, *args):
    """
    返回路徑
    """
    return os.path.join(root, *args)


def check_path(root, *args):
    """
    檢查路徑是否存在
    """
    path = get_path(root, *args) if args else root
    return os.path.exists(path)


def makedirs(root, *args):
    """
    檢查路徑是否存在，不存在就創建
    """
    path = get_path(root, *args)
    if not check_path(path):
        os.makedirs(path)
    return path


def read_local_config(format=DEFAULT_CONFIG_FORMAT, dir_name="cfg"):
    """
    讀取本地設定檔
    """
    format = format.lower()
    assert format in ["yaml", "json"], "format should be yaml or json"
    if format == "yaml":
        loader = yaml.safe_load
    else:
        loader = json.load

    _, folder_root, file_name = inspect_path(stack_level=2, return_folder_root=True)
    path = get_path(folder_root, dir_name, f"{file_name}.{format}")

    if check_path(path):
        with open(path, "r", encoding="utf-8") as f:
            return loader(f)
    else:
        print(f"Local config not found at {path}")
        return {}
