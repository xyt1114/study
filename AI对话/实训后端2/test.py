import requests
query_param = input("请输入内容:\n")
my_dict = {
    "model" : "deepseek-r1:1.5b",
    "prompt" : query_param,
    "stream" : False
}
url = "http://localhost:11434/api/generate/"
rs = requests.post(url, json=my_dict)
if rs.status_code == 200:
    data = rs.json()
    print(data)
result = data['response']