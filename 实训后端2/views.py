from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse

@csrf_exempt
def chat_api(request):
    print("\n===== 收到请求 =====")
    if request.method == 'POST':
        try:
            # 解析请求数据
            data = json.loads(request.body)
            user_question = data.get('question')

            # 打印调试信息
            print(f"[用户问题] {user_question}")

            # 这里添加业务逻辑（示例回复）
            ####################################
            # 示例1：简单回显测试
            bot_reply = f"已收到问题“{user_question}”正在思考中"

            # 示例2：调用AI模型生成回答（需自行实现）
            # from your_module import generate_answer
            # bot_reply = generate_answer(user_question)

            # 示例3：固定回复测试
            # bot_reply = "这是一个测试回复"
            ####################################

            print(f"[生成回复] {bot_reply}")

            # 返回标准格式响应
            return JsonResponse({
                'status': 'success',
                'reply': bot_reply  # 确保包含这个字段
            })

        except json.JSONDecodeError:
            error_msg = "无效的JSON格式"
            print(f"[错误] {error_msg}")
            return JsonResponse({
                'status': 'error',
                'reply': error_msg  # 错误信息也通过reply返回
            }, status=400)

        except Exception as e:
            error_msg = f"处理请求时发生错误：{str(e)}"
            print(f"[错误] {error_msg}")
            return JsonResponse({
                'status': 'error',
                'reply': error_msg
            }, status=500)

    # 处理非POST请求
    error_msg = f"不支持的请求方法：{request.method}"
    print(f"[警告] {error_msg}")
    return JsonResponse({
        'status': 'error',
        'reply': error_msg
    }, status=405)