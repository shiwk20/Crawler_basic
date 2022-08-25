from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as EC
import selenium
import json
import prettytable
import logging
import tqdm
from datetime import datetime


url = "https://webvpn.tsinghua.edu.cn"
info_url = "info.tsinghua.edu.cn/"

fmt = '%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
level = logging.INFO

formatter = logging.Formatter(fmt, datefmt)
logger = logging.getLogger()
logger.setLevel(level)

file = logging.FileHandler("./GPA.log", encoding='utf-8')
file.setLevel(level)
file.setFormatter(formatter)
logger.addHandler(file)

console = logging.StreamHandler()
console.setLevel(level)
console.setFormatter(formatter)
logger.addHandler(console)

def get_user():
    with open("user.json", "r") as f:
        dict = json.load(f)
    return dict

def change_handle(str: str) -> bool:
    flag = False
    for handle in browser.window_handles:
        # 先切换到该窗口
        browser.switch_to.window(handle)
        # 得到该窗口的标题栏字符串，判断是不是我们要操作的那个窗口
        if str in browser.title:
            # 如果是，那么这时候WebDriver对象就是对应的窗口，正好，跳出循环
            flag = True
            break
    return flag

def login_webvpn(dict: dict):
    global browser
    browser = selenium.webdriver.Chrome(service = ChromeService(ChromeDriverManager().install()))
    browser.get(url)
    browser.maximize_window()
    browser.find_element(By.ID, "user_name").send_keys(dict['username'])
    browser.find_element(By.NAME, "password").send_keys(dict['password'])

    login = browser.find_element(By.ID, "login")
    login.click()
    wdw(browser, 5).until(EC.visibility_of_element_located((By.ID, "quick-access-input")))
    return browser.find_elements(By.ID, "quick-access-input") != []


def go_info():
    access_input = browser.find_element(By.ID, "quick-access-input")
    access_input.send_keys(info_url)
    access_input.send_keys(Keys.ENTER)

    return change_handle("信息门户")

def login_info(dict):
    browser.find_element(By.ID, "userName").send_keys(dict["username"])
    browser.find_element(By.NAME, "password").send_keys(dict["password"])

    info_login = browser.find_element(By.CLASS_NAME, "but").find_element(By.TAG_NAME, "input")
    info_login.click()
    wdw(browser, 5).until(EC.visibility_of_element_located((By.LINK_TEXT, "进入门户")))
    return browser.find_elements(By.LINK_TEXT, "进入门户") != []

def go_grades():
    info_go = browser.find_element(By.LINK_TEXT, "进入门户")
    info_go.click()
    grades = browser.find_element(By.LINK_TEXT, "全部成绩")
    grades.click()
    return change_handle("成绩")

def read_table():
    tables = browser.find_elements(By.TAG_NAME, 'table')
    assert len(tables) >= 3
    table = tables[2]

    trs = table.find_elements(By.TAG_NAME, "tr")
    tr_head = trs[0]
    tr_sum = trs[-1]
    tr_courses = trs[1:-2]
    logger.info(f"read table successfully")
    # 读取表头
    ths = tr_head.find_elements(By.TAG_NAME, "th")
    res_head = []
    for th in ths:
        res_head.append(th.text)
    assert len(res_head) == 12
    logger.info(f"read head successfully")

    # 读取总数
    tds = tr_sum.find_elements(By.TAG_NAME, "td")
    res_sum = []
    for td in tds:
        res_sum.append(td.text)
    res_sum.pop()
    assert len(res_sum) == 3
    logger.info(f"read sum successfully")
    
    # 读取每一课
    res_courses = []
    for tr_course in tqdm.tqdm(tr_courses):
        tds = tr_course.find_elements(By.TAG_NAME, "td")
        res_course = []
        for td in tds:
            res_course.append(td.text)
        res_courses.append(res_course)
    logger.info(f"read {len(tr_courses)} courses successfully")

    return res_head, res_courses, res_sum

def print_save_table(res_head: list, res_courses: list, res_sum: list):
    def cur_time():
        now = datetime.now()
        return now.strftime("%Y/%m/%d %H:%M:%S")
        
    grades_table = prettytable.PrettyTable(res_head)
    for i in res_courses:
        grades_table.add_row(i) 
    grades_table.align["课程名"] = "l"
    
    with open("GPA.txt", "a", encoding='UTF-8') as f:
        f.write(cur_time() + "\n")
        f.write(str(grades_table) + "\n")
        f.close()
    print(grades_table)
    print(res_sum[0], res_sum[1], res_sum[2])

def main():
    logger.info("***************************************************************")
    logger.info("GPA_caculator started")
    dict = get_user()
    logger.info("user_info loaded")
    try:
        try:
            if login_webvpn(dict):
                logger.info("Webvpn logined successfully")
            else:
                logger.error("Webvpn logined failed")
                raise
        except Exception as e:
            logger.error(f"Exception when login Webvpn: {e}")
            raise
        
        try:
            if go_info():
                logger.info("go to info successfully")
            else:
                logger.error("go to info failed")
                raise
        except Exception as e:
            logger.error(f"Exception when go to info: {e}")
            raise
        
        try:
            if login_info(dict):
                logger.info("info logined successfully")
            else:
                logger.error("info logined failed")
                raise
        except Exception as e:
            logger.error(f"Exception when login info: {e}")
            raise
        
        try:
            if go_grades():
                logger.info("go to grades successfully")
            else:
                logger.error("go to grades failed")
                raise
        except Exception as e:
            logger.error(f"Exception when go to grades: {e}")
            raise

        try:
            res_head, res_courses, res_sum = read_table()
        except Exception as e:
            logger.error(f"Exception when read tables: {e}")
            raise

        browser.quit()
        logger.info("browser closed")

        print_save_table(res_head, res_courses, res_sum)
        logger.info("table printed and saved successfully")
    except:
        logger.error("program interuption")
    logger.info("***************************************************************")

if __name__ == "__main__":
    main()