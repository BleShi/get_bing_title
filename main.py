import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException

def main(query, file_path):
    # 使用Safari，遥遥领先Chrome，不需要在路径里放个driver了，真的好方便
    driver = webdriver.Safari()  # 如果这一行报错，在终端里执行这句命令：sudo safaridriver --enable
    driver.get("https://www.bing.com")  # 访问必应
    time.sleep(5)  # 等必应首页加载

    # 拒绝Cookies
    try:
        reject_button = driver.find_element("xpath", '//*[@id="bnp_btn_reject"]')
        reject_button.click()
        time.sleep(5)  # 等待页面加载完成
    except NoSuchElementException:
        print("Cookies的XPaths没找到捏")

    # 执行搜索
    search_box = driver.find_element("name", "q")
    search_box.send_keys(query + Keys.RETURN)
    time.sleep(5)  # 等待搜索结果

    titles_text = []  # 初始化存储所有页面标题的列表

    for i in range(times):  # 翻页
        # 收集当前页的搜索结果标题
        titles = driver.find_elements("xpath", '//h2')
        for title in titles:
            title_text = title.text
            # 过滤掉不需要的标题
            if "相关搜索" in title_text or "进一步探索" in title_text or query in title_text:
                continue
            titles_text.append(title_text)
        
        # 尝试翻到下一页
        next_page_xpath = "//a[@title='下一页']"  # 使用title属性定位下一页按钮
        try:
            next_page_button = driver.find_element("xpath", next_page_xpath)
            next_page_button.click()
            time.sleep(5)  # 等待页面加载
        except NoSuchElementException:
            print("下一页的XPaths没找到捏")
            break

    driver.quit()
    
    # 将标题保存到CSV文件中
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title'])  # 写入表头
        for title in titles_text:
            writer.writerow([title])

# 下面这块根据需求改
times = 100  # 翻页次数，一般一页会有10个标题，每翻一页要5秒，如果网速比较好以及嫌慢可以把上面的time.sleep(5)的5改成想要的秒数
query_keywords = 'university'  # 输入研究的关键词或者句
query_site = 'www.shine.cn'  # 输入网站域名，啥都可以，学校官网也可以，微信公众号也可以，下面找了些报纸的例子

# english.news.cn 新华社英语版
# en.people.cn 人民日报英语版
# www.shine.cn 上海日报英语版
# www.thetimes.co.uk 泰晤士报
# www.telegraph.co.uk 每日电讯报
# www.theguardian.com 卫报
# www.nytimes.com 纽约时报
# www.washingtonpost.com 华盛顿邮报
# www.wsj.com 华尔街日报

# 输出结果
query_control = 'site:'
query = query_keywords + " " + query_control + query_site
file_path = 'output.csv'
main(query, file_path)

print(f"保存在 {file_path} 啦！")