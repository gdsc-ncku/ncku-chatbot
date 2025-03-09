

import asyncio
import inspect
import os

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


def inspect_path(obj_or_cls):
    """
    接收一個對象或類別，返回該類別定義所在的檔案名稱
    """
    # 如果傳入的不是類別，就取它的 class
    cls = obj_or_cls if isinstance(obj_or_cls, type) else obj_or_cls.__class__
    file_path = inspect.getfile(cls)
    folder_name = os.path.basename(os.path.dirname(file_path))
    file_name = os.path.basename(file_path).split('.')[0]
    return folder_name, file_name

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

