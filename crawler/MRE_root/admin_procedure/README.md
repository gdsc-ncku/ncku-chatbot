### 行政手續爬蟲
- 藉由 jina 工具來做網頁爬蟲

#### 使用說明
1. 將想要爬取的網頁放置在 web_crawler_urls.txt 裡面，例如:
> https://www.google.com/
> https://www.dcard.tw/f
2. 執行 main.py ，就會藉由 jina 來整理資料，然後用 gpt 來判斷是否為行政手續的網址，最後再用 gpt 整理內文，並存在 txt 資料夾內。

### 行政手續 QA 形式
#### 使用說明
1. 執行 gen_title_gpt.py ，就會藉由 jina 來整理資料，然後用 gpt 來整理成 QA 形式，並儲存成 .json 檔。