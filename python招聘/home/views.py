from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.models import User
from job.models import Job
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q




def home(request):
    return render(request,'base.html')



@api_view(['POST'])
def register(request):
    # 获取请求数据
    name = request.data.get('name')
    account = request.data.get('account')
    password = request.data.get('password')
    if not name or not account or not password:
        return Response({"error": "所有字段都必须填写"}, status=400)
    try:
        user = User.objects.create(
            name=name,
            account=account,
            password=password
        )
        user.save()  # 保存到数据库
        return Response({"message": "注册成功"}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


# views.py
@api_view(['POST'])
def login(request):
    try:
        # 获取请求体中的 JSON 数据
        data = json.loads(request.body)
        name = data.get('name')
        account = data.get('account')
        password = data.get('password')

        # 打印数据检查
        print(f"Received username: {name}, account: {account}, password: {password}")

        # 确保所有字段都存在
        if not name or not account or not password:
            return JsonResponse({'success': False, 'message': '用户名、账号或密码不能为空！'})

        # 查找数据库中的用户
        user = User.objects.filter(name=name, account=account).first()
        print(user)

        if user:
            # 如果找到用户，验证密码
            if (password == user.password):
                return JsonResponse({'success': True, 'message': '登录成功！'})
            else:
                return JsonResponse({'success': False, 'message': '密码错误！'})
        else:
            return JsonResponse({'success': False, 'message': '用户名或账号不存在！'})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': '无效的请求格式！'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


# 创建一个简单的搜索视图
@csrf_exempt  # 忽略 CSRF 校验（对于 API 请求可以这样处理，生产环境中请使用 Token 或其他方式保护 API）
def search(request):
    if request.method == 'POST':
        import json
        # 获取前端发送的搜索内容
        data = json.loads(request.body)
        query = data.get('query', '')
        print(query)
        jobs = Job.objects.filter(
            Q(title__icontains=query) | Q(address__icontains=query)
        )
        print(jobs)
        return render(request,'base.html')