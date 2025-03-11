from crawler import activity_crawler

if __name__ == "__main__":
    URL = "https://activity.ncku.edu.tw/"
    PATH = "index.php?c=apply&no="
    END_STR = '=END='

    activity_crawler(URL, PATH, END_STR, max_worker=0, headless=False)
