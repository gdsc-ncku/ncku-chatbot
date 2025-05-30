from crawler import activity_crawler
import time


def timer():
    import atexit, time

    start_time = time.perf_counter()
    atexit.register(diff_time, start_time, "Total")
    return start_time


def diff_time(start, name=""):
    print(
        f"{name.strip()+' ' if len(name) > 0 else name}Time: {time.perf_counter() - start:.2f} sec"
    )


if __name__ == "__main__":
    URL = "https://activity.ncku.edu.tw/"
    PATH = "index.php?c=apply&no="
    END_STR = "=END="

    start_time = timer()
    activity_crawler(URL, PATH, END_STR, max_worker=0, headless=True)
    diff_time(start_time, "Code")
