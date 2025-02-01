import re

lines = []  # 重命名变量，避免与内置类型冲突


with open('测试.txt', 'r', encoding='utf-8') as file:  # 打开 text.txt 文件进行读取
    for line in file:
        # 如果行非空，去掉前后空白并添加到列表
        if line.strip():
            lines.append(line.strip())  # 只去除每行的前后空白
        else:
            lines.append("")  # 处理空行，保持空行在列表中的存在


formatted_text = '/'.join(lines)  # 将所有行合并成一个字符串，中间用 `/` 连接

# # 输出格式化后的文本
# print(formatted_text)

result = re.sub(r'//','\n',formatted_text)

with open('测试.txt', 'w', encoding='utf-8') as file:    # 写入那个文件
    file.write(result)