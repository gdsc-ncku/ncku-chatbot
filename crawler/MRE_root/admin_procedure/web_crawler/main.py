import os
from utils.file_ops import create_safe_filename, save_text
from utils.web_ops import fetch_url_content, fetch_suburls
from utils.content_gen import generate_content, question_classifaier
from openai import OpenAI
import time

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def get_link(main_url):
    links = fetch_suburls(main_url)
    with open("urls.txt", "w") as f:
        for link in links:
            f.write(f"{link}\n")


def jina():
    client = OpenAI()

    with open("urls.txt", "r") as f:
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
            save_text(generated_content, f"{filename}.txt")
            print(f"Text file saved as: ./txt/{filename}.txt")
        else:
            print(f"Skipping URL: {url}", "classified as False")

        time.sleep(3)

    # Clear the content of urls.txt after processing all URLs
    open("urls.txt", "w").close()


if __name__ == "__main__":
    main_urlrls = ["https://assistance-osa.ncku.edu.tw/p/412-1051-2563.php?Lang=zh-tw"]
    for main_url in main_urlrls:
        get_link(main_url)
        jina()
