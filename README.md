# Crawler_basic

此为酒井暑培爬虫与数据库小作业的爬虫部分：

+ 用requests库实现一个**知乎热榜定时跟踪器**，定期爬取知乎热榜，并记录热榜中问题的一些基本信息，如问题摘要、描述、热度、访问人数、回答数量等。
+ 用Selenium库实现一个**GPA计算器**，模拟点击登录 WebVPN，然后登录 info，进而访问成绩单页面查询到成绩，计算每学期的绩点。

## 知乎热榜定时跟踪器

### 介绍

该程序位于 `zhihu_hot`文件夹下，可以定时爬取知乎50个热榜问题的 `"title", "url", "excerpt", "heat", "answer", "attention", "browse"`（标题，网址，详细描述，热度，回答数，关注数，浏览量）并将结果保存在 `zhihu.json` 文件内，每次爬取还会记录开始和结束时间。

此外，该程序除了可以使用requests模块获取网页信息外，还可以使用urllib模块，具体见代码注释。

### 使用方法

在 `headers.json`内写入您的 `"User-Agent"、"Cookie"`(通过在[知乎热榜](https://www.zhihu.com/hot)界面下按 `F12 `获取)。然后在 `zhihu_crawler.py `内修改每次爬取间隔的时间 `interval_crawler `（单位：秒）和最大爬取次数 `max_num `，~~此处摆烂没有用argparse或者input~~。最后在 `zhihu_hot `目录下 `python zhihu_crawler.py`即可运行。

### 问题

+ 对异常情况的处理较少，程序鲁棒性不够（基本上是爬取过程中遇到一个异常修复一个异常，比如没有详细描述的热榜问题，没有评论的广告等）；
+ 没有使用logging模块输出日志，可参考[Python Logging 模块完全解读 ](https://www.sohu.com/a/313356453_571478)，在下面的GPA计算器中使用了。

## GPA计算器

### 介绍

该程序位于 `GPA_caculator` 文件夹下，可以模拟用户通过 `webvpn `登录 `info` ，然后获取info上该用户所有成绩信息并打印和保存。（根据爬取的信息可以很方便计算出各种成绩信息，比如每学期的GPA，得到3.6的学分总数等，~~因为太懒就没有写~~）

### 使用方法

在 `user.json` 下写入您的用户名和密码（注意保管好个人隐私），然后在 `GPA_caculator `目录下 `python GPA_caculator.py `即可运行。

##  Reference

[lamda&#39;s example](https://github.com/Btlmd/sast2022-crawler-SQL-training)
