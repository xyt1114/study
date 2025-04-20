from django.http import HttpResponse


def index(request):
    return HttpResponse('这是项目首页')
def ai(request):
    return  HttpResponse('ai')
def school(request):
    return HttpResponse('school')
def information(request):
    return HttpResponse('information')


def server(request):
    print(request)
    print("前端发送的请求方式是：", request.method)

    if request.method == "GET":
        print("前端发送的请求方式是：", request.GET)
        return HttpResponse('GET')

    elif request.method == "POST":
        print("前端发送的请求方式是：", request.POST)
        # 使用get()方法来获取POST数据中的'username'字段
        username = request.POST.get('username')
        # 通过字符串格式化返回响应内容
        return HttpResponse(f'POST, 欢迎用户 {username}')

    else:
        return HttpResponse("其它")

