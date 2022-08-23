import requests
import json
from bs4 import BeautifulSoup as BS
import re
import time

url = "https://www.zhihu.com/hot"

interval_questions = 2
interval_crawler = 60
max_num = 2

hearders = {}

def get_section():
    global headers
    with open("headers.json", "r") as f:
        dict = json.load(f)
    headers = {"User-Agent": dict["User-Agent"], "Cookie": dict["Cookie"]}
    response = requests.get("https://www.zhihu.com/hot", headers = headers)
    soup = BS(response.text, 'lxml')
    return soup.find_all("section", class_="HotItem")

def crawler(num: int):
    section = get_section()
    assert len(section) == 50
    
    result_list = []
    for i in range(50):
        tmp_dict = {}
        # keys = ["title", "url", "excerpt", "heat", "answer", "attention", "browse"]

        # 获得标题
        a_class = section[i].find("a")
        tmp_dict["title"] = a_class["title"]

        # 获得该问题的内容网址
        tmp_url = a_class["href"]
        tmp_dict["url"] = tmp_url

        # 获得详细描述（有些问题没有）
        try:
            regex = '<p class="HotItem-excerpt">(.+)</p>'
            pattern = re.compile(regex)
            tmp_dict["excerpt"] = re.findall(pattern, str(a_class.find("p")))[0]
        except Exception as e:
            print("get excerpt error", e)
            tmp_dict["excerpt"] = ""

        # 获得热度
        regex = '</svg>(.+)热度'
        pattern = re.compile(regex)
        tmp_dict["heat"] = re.findall(pattern, str(section[i]))[0]
        
        # 进入该问题的内容网址
        time.sleep(interval_questions)
        tmp_response = requests.get(tmp_url, headers = headers)
        tmp_soup = BS(tmp_response.text, 'lxml')

        # 获得热度
        regex = '<span>(.+)<!-- --> 个回答</span>'
        pattern = re.compile(regex)
        tmp_dict["answer"] = re.findall(pattern, str(tmp_soup))[0]

        # 获得关注和浏览数
        strong_value = tmp_soup.find_all("strong", class_ = "NumberBoard-itemValue")
        tmp_dict["attention"] = strong_value[0]["title"]
        tmp_dict["browse"] = strong_value[1]["title"]
        
        result_list.append(tmp_dict)
        print("Num: ", num, "Index: ", i + 1, " ", tmp_dict)
        print()

    return result_list

def cur_time():
    t = time.localtime()
    return str(t.tm_year) + "/" + str(t.tm_mon) + "/" + str(t.tm_mday) + " " + str(t.tm_hour) + ":" + str(t.tm_min) + ":" + str(t.tm_sec)

def main():
    all_result = []
    for i in range(max_num):
        start_time = cur_time()
        result_list = crawler(i + 1)
        end_time = cur_time()
        run_time = {"start_time": start_time, "end_time": end_time}
        print("Num: ", i + 1, run_time)
        print()
        result_list.insert(0, run_time)
        all_result.append(result_list)
        time.sleep(interval_crawler) if i != max_num - 1 else None

    with open("zhihu.json", "w") as f:
        json.dump(all_result, f)
        f.close()
    print("Save successfully")

if __name__ == "__main__":
    main()