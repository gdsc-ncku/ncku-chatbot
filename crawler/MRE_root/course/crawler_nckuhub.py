'''
    爬 https://nckuhub.com/course，並用 chatgpt 文本摘要評論
    *需要openai api_key
'''

import time
import json
import os
import requests
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from rich import print
import openai

openai.api_key = ""

# 定義摘要函式
def summarize_text(content_list):
    content_str = "\n".join(content_list)

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "你是一個擅長文本摘要的 AI，請把課程評價做**30字內**簡潔且具體的摘要。"},
            {"role": "user", "content": content_str}
        ],
        temperature=0.5
)
    summary = response["choices"][0]["message"]["content"]
    print(summary)
    return summary

def main():
    url = "https://nckuhub.com/course"
    response = requests.get(url)
    if response.status_code == 200:
        # 將回應資料解析為 JSON 格式
        data = response.json()
        course=data['courses']

        id=[]
        for i in course:
            id.append(i.get('id'))
            #print(i)

        course_list=[]

        print(len(id))
        index=1

        for i in id:
            course_url=url+'/'+str(i)
            #print(course_url)
            response=requests.get(course_url)
            if response.status_code != 200: continue

            data = response.json()
            courseInfo=data['courseInfo']

            course_name=courseInfo["課程名稱"]
            print(course_name,index)
            index+=1

            if_exixt={}
            for item in course_list:
                if item['科目名稱'] == course_name and item["教師姓名"] == courseInfo["老師"]:
                    if_exixt=item   

            ###如果課程已存在，更新時間
            if if_exixt !={}:
                # 將新的「時間」append（type:list）
                if isinstance(if_exixt['時間'], list):
                    if_exixt['時間'].append(courseInfo["時間"])
                    if_exixt['課程編碼'].append(courseInfo["選課序號"])
                else:
                    # 將原本單個時間轉為列表，並追加新時間
                    if_exixt['時間'] = [if_exixt['時間'], courseInfo["時間"]]
                    if_exixt['課程編碼'] = [if_exixt['課程編碼'], courseInfo["選課序號"]]

            ###如果是新課程，把甜涼收穫轉成float or None
            else:
                got=data['got']
                if isinstance(got, str):
                    got = float(got)
                got=int(got)
                if got==0:
                    got='None'

                sweet=data['sweet']
                if isinstance(sweet, str):
                    sweet = float(sweet)
                sweet=int(sweet)
                if sweet==0:
                    sweet='None'

                cold=data['cold']
                if isinstance(cold, str):
                    cold = float(cold)
                cold=int(cold)
                if cold==0:
                    cold='None'

                comment_list=[]
                comment=data['comment']

                for i in comment:
                    comment_list.append(i['comment'])
                
                summary=[]

                #如果評論存在，則文本摘要
                if comment:
                    time.sleep(1)
                    summary=summarize_text(comment_list)
                else:
                    time.sleep(0.5)
                    continue

                course_data={
                        '科目名稱':courseInfo["課程名稱"],
                        '課程編碼':courseInfo["選課序號"],
                        '系所名稱':courseInfo["系所名稱"],
                        '教師姓名':courseInfo["老師"],
                        '時間':courseInfo["時間"],
                        '收穫':got,
                        '甜度':sweet,
                        '涼度':cold,
                        '評價':summary,
                }
                course_list.append(course_data)



            if index%300==0: #每300筆存一次
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f'nckuhub_ts_{timestamp}.json'
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(course_list, f, ensure_ascii=False, indent=2)
                
                print(f"課程資料已保存至: {filename}")
                print(f"總共收集到 {len(course_list)} 門課程")

        # 儲存資料
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f'nckuhub_ts_{timestamp}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(course_list, f, ensure_ascii=False, indent=2)
        
        print(f"課程資料已保存至: {filename}")
        print(f"總共收集到 {len(course_list)} 門課程")


if __name__ == "__main__":
    main()