from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

def home(request):
    return HttpResponse('这是分目录首页')
# Create your views here.

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie


class VideoUploadView(APIView):
    def post(self, request):
        try:
            video_file = request.FILES.get('video_file')

            if not video_file:
                return Response(
                    {'detail': '未收到视频文件'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 保存文件到media目录
            with open(f'media/{video_file.name}', 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

            return Response({
                'status': 'success',
                'file_path': f'/media/{video_file.name}',
                'file_size': video_file.size
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})