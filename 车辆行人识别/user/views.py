from django.shortcuts import render
from django.http import HttpResponse

from user.models import User
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json


# Create your views here.

from django.http import HttpResponse
from django.contrib.auth.models import User

def add(request):
    # 正确创建用户（自动哈希密码）
    user = User.objects.create_user(
        username='test1',
        password='123'  # 明文密码会被自动哈希
    )
    return HttpResponse('插入成功')

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User  # 如果你没有导入 User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

class LoginView(APIView):
    def post(self, request):
        # 获取并验证必填字段
        username = request.data.get('username')
        password = request.data.get('password')

        # 检查字段是否为空
        if not username or not password:
            return Response(
                {"success": False, "message": "用户名和密码不能为空"},
                status=status.HTTP_400_BAD_REQUEST  # 参数缺失用400
            )

        # 验证用户身份
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return Response(
                    {"success": True, "message": "登录成功"},
                    status=status.HTTP_200_OK
                )
            else:
                # 密码错误
                return Response(
                    {"success": False, "message": "用户名或密码错误"},
                    status=status.HTTP_401_UNAUTHORIZED  # 认证失败用401
                )
        except User.DoesNotExist:
            # 用户不存在
            return Response(
                {"success": False, "message": "用户名或密码错误"},
                status=status.HTTP_401_UNAUTHORIZED  # 认证失败用401
            )

    def get(self, request):
        return Response(
            {"detail": "Method \"GET\" not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )




@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            # 解析请求体中的 JSON 数据
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            print(f"Received data: {data}")  # 打印收到的数据

            # 检查用户名和密码是否为空
            if not username or not password:
                print(f"Missing username or password: {username}, {password}")  # 打印详细信息
                return JsonResponse({'error': '用户名和密码不能为空'}, status=400)

            # 检查用户名是否已存在
            if User.objects.filter(username=username).exists():
                print(f"用户名 {username} 已存在")  # 打印日志
                return JsonResponse({'error': '用户名已存在'}, status=400)

            # 创建新的用户
            user = User.objects.create_user(username=username, password=password)
            return JsonResponse({'message': '注册成功', 'status': 'success'}, status=201)

        except json.JSONDecodeError:
            print("Invalid JSON data")  # 打印无效JSON错误
            return JsonResponse({'error': '无效的 JSON 数据'}, status=400)
        except Exception as e:
            print(f"Error: {e}")  # 打印错误信息，便于排查
            return JsonResponse({'error': '注册失败', 'details': str(e)}, status=500)

    return JsonResponse({'error': '仅支持 POST 请求'}, status=405)



