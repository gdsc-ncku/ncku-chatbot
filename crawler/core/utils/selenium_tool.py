
__all__ = ["async_build_drivers", "async_quit_drivers", "build_drivers", "auto_build_wrapper", "thread_core", "single_core"]

from selenium import webdriver
from tqdm import tqdm

from concurrent.futures import ThreadPoolExecutor, as_completed
import functools
import asyncio
import queue
import os


async def async_build_drivers(options, num_worker):
    """
    創建多個driver(async)
    """
    loop = asyncio.get_running_loop()
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=min(num_worker, os.cpu_count())) as executor:
        tasks = [
            loop.run_in_executor(executor, lambda: webdriver.Chrome(options=options))
            for _ in range(num_worker)
        ]
        drivers = await asyncio.gather(*tasks)
        executor.shutdown(wait=True)
    return drivers


async def async_quit_drivers(drivers):
    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor(max_workers=min(len(drivers), os.cpu_count())) as executor:
        tasks = [
            loop.run_in_executor(executor, lambda: driver.quit())
            for driver in drivers
        ]
        await asyncio.gather(*tasks)
        executor.shutdown(wait=True)


def build_drivers(options, num_worker=1):
    """
    創建多個driver(for loop)
    """
    drivers = [webdriver.Chrome(options=options) for _ in range(max(num_worker, 1))]
    return drivers


def auto_build_wrapper(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if hasattr(self, "build_drivers") and callable(getattr(self, "build_drivers")):
            self.build_drivers()

        result = func(self, *args, **kwargs)
        return result
    return wrapper


def thread_auto_derives(derives_queue, func, task, *args, **kwargs):
    device = derives_queue.get()
    try:
        return task, func(device, task, *args, **kwargs)

    finally:
        derives_queue.put(device)


def thread_core(derives, func, tasks, *args, **kwargs):
    """
    多線程任務
    derives: list of derives
    tasks: list of tasks
    *args: args
    **kwargs: kwargs

    return dict: {task: result}
    """

    derives_queue = queue.Queue()
    for d in derives:
        derives_queue.put(d)

    with ThreadPoolExecutor(max_workers=len(derives)) as executor:
        futures = [
            executor.submit(thread_auto_derives, derives_queue, func, task, *args, **kwargs)
            for task in tasks
        ]
        #executor.shutdown(False)

        output_dict = {}
        qbar = tqdm(futures, total=len(futures), desc=f"Processing tasks with {len(derives)} Threads")
        for future in qbar:
            task, result = future.result()
            if result is not None:
                output_dict[task] = result
        qbar.close()
        executor.shutdown(cancel_futures=True)
        return output_dict


def single_core(derives, func, tasks, *args, **kwargs):
    """
    單線程任務
    derives: list of derives
    tasks: list of tasks
    *args: args
    **kwargs: kwargs

    return dict: {task: result}
    """

    output_dict = {}
    qbar = tqdm(tasks, desc=f"Processing tasks with Main Thread")
    for task in qbar:
        result = func(derives[0], task, *args, **kwargs)
        if result is not None:
            output_dict[task] = result

    qbar.close()
    return output_dict