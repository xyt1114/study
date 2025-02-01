from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 获取用户输入
query = input("请输入职位查询关键字: ")

# 初始化 Edge 浏览器
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

try:
    with open(query + '数据.txt', 'w', encoding='utf-8') as f:  # 修改文件名为 '数据.txt'
        for page in range(1, 11):  # 从 1 循环到 10
            # 格式化 URL
            url = f"https://www.zhipin.com/web/geek/job?query={query}&city=101270100&page={page}"
            driver.get(url=url)

            # 等待职位名称元素加载
            job_elements = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.job-name'))
            )
            area_elements = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.job-area'))
            )
            # 等待薪资元素加载
            salary_elements = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.salary'))
            )

            # 遍历所有职位和薪资信息
            for job, area, salary in zip(job_elements, area_elements, salary_elements):
                job_name = job.text
                area_name = area.text
                salary_range = salary.text
                f.write(f"{job_name}: {salary_range} ({area_name})\n")  # 将职位名称和薪资写入文件

finally:
    driver.quit()
