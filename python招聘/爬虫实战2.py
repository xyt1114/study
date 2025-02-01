import time
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.edge.service import Service

# 创建 Edge 浏览器的 WebDriver 实例
service = Service()  # 请替换为你的EdgeDriver路径
wd = webdriver.Edge(service=service)

url_list = []

# 打开目标网页
wd.get("https://www.zhipin.com/web/geek/job?query=%E5%89%8D%E7%AB%AF&city=101270100")

# 等待网页加载
time.sleep(5)  # 等待几秒钟，让网页加载

try:
    elements = WebDriverWait(wd, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "job-card-body")]/a'))
    )

    for element in elements:
        time.sleep(1)
        href = element.get_attribute("href")

        if href:
            url_list.append(href)  # 直接使用 href
            print("*************************")
            print(href)
        else:
            print("未找到匹配的链接")

except Exception as e:
    print(f"发生错误: {e}")

finally:
    wd.quit()  # 确保退出浏览器
