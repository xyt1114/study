import re
from django.http import HttpResponse
from django.shortcuts import render
from .models import Job
from .models import Occupation

from django.http import HttpResponse
import re
from .models import Occupation

def insert_from_file(request):
    try:
        with open('测试.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()

            job_pattern = re.compile(
                r'^(?P<title>[^,]+),'  # 职位名称
                r'(?P<salary>[^,]+),'  # 薪资
                r'(?P<address>[^,]+),'  # 工作地点
                r'(?P<experience>[^,]+),'  # 工作经验
                r'(?P<educational_background>[^,]+),'  # 学历要求
                r'(?P<job_description>[^/]+)(?=,|/)'  # 确保职位描述只匹配到第一个斜杠或逗号
                r'(?P<tech_stacks>[^,]+(?:[\s/][^/]*)*)'  # 技术栈
            )

            for line in lines:
                line = line.strip()  # 去除前后空白字符

                match = job_pattern.match(line)
                if match:
                    title = match.group('title')
                    salary = match.group('salary')
                    address = match.group('address')
                    experience = match.group('experience')
                    educational_background = match.group('educational_background')
                    job_description = match.group('job_description')
                    tech_stacks = match.group('tech_stacks')
                    tech_stack_list = tech_stacks.split('\n') if tech_stacks else []
                    tech_stack = ', '.join(tech_stack_list)

                    # 调试：检查插入的数据
                    print(f"Inserting: {title}, {salary}, {address}, {experience}, {educational_background}, {job_description}, {tech_stack}")

                    # 插入数据到数据库
                    Occupation.objects.create(
                        title=title,
                        salary=salary,
                        address=address,
                        experience=experience,
                        educational_background=educational_background,
                        job_description=job_description,
                        tech_stack=tech_stack
                    )

        return HttpResponse("Jobs imported successfully!", status=200)

    except Exception as e:
        return HttpResponse(f"Error importing jobs: {str(e)}", status=500)

def add_job(request):
    # 假设文件存储在本地，路径为 job_data.txt
    try:
        with open('前端数据(1).txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()

            # 正则表达式，用来提取职位名称、薪资、地址等信息
            job_pattern = re.compile(r'^(?P<title>[\w·]+): (?P<salary>[\d-]+K(?:·\d{1,2}薪)?) \((?P<address>.+)\)$')

            for line in lines:
                # 去除每行前后的空白字符
                line = line.strip()

                # 解析每行数据
                match = job_pattern.match(line)
                if match:
                    title = match.group('title')
                    salary = match.group('salary')
                    address = match.group('address')

                    # 创建并保存 Job 实例
                    Job.objects.create(
                        title=title,
                        salary=salary,
                        address=address,
                    )

        return HttpResponse("Jobs imported successfully!", status=200)
    except Exception as e:
        return HttpResponse(f"Error importing jobs: {str(e)}", status=500)


