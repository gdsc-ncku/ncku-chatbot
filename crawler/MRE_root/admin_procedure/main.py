import os
from utils.file_ops import create_safe_filename, save_xml
from utils.web_ops import fetch_url_content, fetch_suburls
from utils.content_gen import generate_content, question_classifaier
from openai import OpenAI
import time

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


# 將主要網頁的子網頁存入 urls.txt
def get_link(main_url):
    links = fetch_suburls(main_url)
    with open("./sub_urls/urls.txt", "w") as f:
        for link in links:
            f.write(f"{link}\n")


def jina():
    client = OpenAI()

    with open("./sub_urls/urls.txt", "r") as f:
        urls = f.readlines()

    for url in urls:
        url = url.strip()
        prefixed_url = f"https://r.jina.ai/{url}"
        web_data = fetch_url_content(prefixed_url)
        if web_data is None:
            continue
        classified = question_classifaier(client, web_data)
        if classified == "True":
            generated_content = generate_content(client, web_data)
            filename = create_safe_filename(url)
            save_xml(generated_content, f"{filename}.txt")
            print(f"Text file saved as: ./txt/{filename}.txt")
        else:
            print(f"Skipping URL: {url}", "classified as False")

        time.sleep(3)
    # Clear the content of urls.txt after processing all URLs
    open("./sub_urls/urls.txt", "w").close()


if __name__ == "__main__":
    # 讀取 txt 檔案並提取 URL 列表
    main_urls = []
    with open("web_crawler_urls.txt", "r") as file:
        for line in file:
            # 去除首尾空白，只保留純粹的 URL
            url = line.strip()
            # 檢查是否為有效的 URL（避免處理最後一行或其他無效行）
            if url.startswith("http"):
                main_urls.append(url)

    print(main_urls)

    for main_url in main_urls:
        get_link(main_url)
        jina()
