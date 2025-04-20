import pymysql
import requests

from myutiks.MysqlUtil import get_connection
import json
import traceback
import logging
from django.http import JsonResponse
from django.db.utils import DatabaseError

logger = logging.getLogger(__name__)
def history_list(request):
    connection = get_connection()
    cursor = connection.cursor()
    query_param = request.GET.get('username')
    sql = 'select query_param from history where username=%s;'
    cursor.execute(sql, [query_param])
    result = cursor.fetchall()
    re_list = []
    for item in result:
        re_list.append({"queryParam": item[0]})
    print(re_list)
    cursor.close()
    connection.close()
    return JsonResponse({"myData": re_list})

def user_logon(request):
    if request.method == 'POST':
        try:
            # 获取请求参数
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if not username or not password or not confirm_password:
                if not request.body:
                    return JsonResponse({"message": "请求体为空"}, status=400)

                try:
                    data = json.loads(request.body)
                    username = data.get('username')
                    password = data.get('password')
                    confirm_password = data.get('confirm_password')
                except json.JSONDecodeError:
                    return JsonResponse({"message": "请求体格式错误"}, status=400)

            # 在控制台打印用户名和密码
            print(f"Received username: {username}")
            print(f"Received password: {password}")

            # 检查两次输入的密码是否一致
            if password != confirm_password:
                return JsonResponse({"message": "两次输入的密码不一致"}, status=400)

            # 获取数据库连接
            connection = get_connection()
            if not connection:
                return JsonResponse({"message": "无法连接到数据库"}, status=500)

            cursor = connection.cursor()

            # 检查用户名是否已存在
            cursor.execute("SELECT username FROM cdlg_app.login WHERE username = %s", [username])
            existing_user = cursor.fetchone()

            if existing_user:
                cursor.close()
                connection.close()
                return JsonResponse({"message": "用户名已存在"}, status=400)

            # 插入新用户
            cursor.execute(
                "INSERT INTO cdlg_app.login (username, password) VALUES (%s, %s)",
                [username, password]
            )

            # 提交事务
            connection.commit()

            # 关闭游标和连接
            cursor.close()
            connection.close()

            return JsonResponse({"message": "注册成功"}, status=201)

        except pymysql.Error as e:
            if 'connection' in locals() and connection:
                connection.rollback()
            print("Error details:", traceback.format_exc())
            return JsonResponse({"message": "数据库错误", "error": str(e)}, status=500)

        except Exception as e:
            if 'connection' in locals() and connection:
                connection.rollback()
            print("Error details:", traceback.format_exc())  # 打印错误的完整堆栈信息
            return JsonResponse({"message": "服务器错误", "error": str(e)}, status=500)
    else:
        return JsonResponse({"message": "请求方法不支持"}, status=405)
def user_login(request):
    if request.method == 'POST':
        try:
            # 获取请求参数
            username = request.POST.get('username')
            password = request.POST.get('password')

            # 如果参数为空，尝试从请求体中获取
            if not username or not password:
                if not request.body:
                    return JsonResponse({"message": "请求体为空"}, status=400)

                try:
                    data = json.loads(request.body)
                    username = data.get('username')
                    password = data.get('password')
                except json.JSONDecodeError:
                    return JsonResponse({"message": "请求体格式错误"}, status=400)

            # 检查用户名和密码是否为空
            if not username or not password:
                return JsonResponse({"message": "用户名或密码不能为空"}, status=400)

            # 在控制台打印用户名和密码（仅用于调试）
            print(f"Received username: {username}")
            print(f"Received password: {password}")

            # 获取数据库连接
            connection = get_connection()
            if not connection:
                return JsonResponse({"message": "无法连接到数据库"}, status=500)

            cursor = connection.cursor()

            # 查询用户是否存在且密码匹配
            cursor.execute(
                "SELECT * FROM cdlg_app.login WHERE username = %s AND password = %s",
                [username, password]
            )
            user = cursor.fetchone()

            # 关闭游标和连接
            cursor.close()
            connection.close()

            if user:
                # 登录成功，重定向到index页面
                return JsonResponse({
                    "message": "登录成功",
                    "redirect_url": "http://localhost:8000/index/"
                }, status=200)
            else:
                # 登录失败
                return JsonResponse({"message": "用户名或密码错误"}, status=401)

        except pymysql.Error as e:
            if 'connection' in locals() and connection:
                connection.rollback()
            print("Error details:", traceback.format_exc())
            return JsonResponse({"message": "数据库错误", "error": str(e)}, status=500)

        except Exception as e:
            if 'connection' in locals() and connection:
                connection.rollback()
            print("Error details:", traceback.format_exc())
            return JsonResponse({"message": "服务器错误", "error": str(e)}, status=500)
    else:
        return JsonResponse({"message": "请求方法不支持"}, status=405)

def question(request):
    query_param = request.GET.get('queryParam')
    username = request.GET.get('username')
    result = history_id(username, query_param)
    print(result)
    if len(result) == 0:
        print("未找到匹配的 history_id，调用 insert_history")  # 调试信息
        insert_result = insert_history(username, query_param)
        if insert_result['status'] == 500:
            return JsonResponse({
                "status": 500,
                "msg": "新建对话失败",
            })
        # 获取新插入的 history_id
        history_id_val = insert_result['history_id']
    else:
        # 如果存在，获取现有的 history_id
        history_id_val = result[0][0]  # 假设 result 是一个列表，每个元素是一个元组

    my_dict = {
        "model": "deepseek-r1:1.5b",
        "prompt": query_param,
        "stream": False
    }
    url = "http://localhost:11434/api/generate/"
    rs = requests.post(url, json=my_dict)
    if rs.status_code == 200:
        data = rs.json()
    result_text = data['response']
    result_text = result_text.replace('<think>', '').replace('</think>', '')
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO qa VALUES (null, %s, %s, %s)"
    try:
        cursor.execute(sql, [query_param, result_text, history_id_val])
        conn.commit()
    except Exception as e:
        print(traceback.format_exc())
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    re_data = {
        "status": 200,
        "msg": "查询成功",
        "data": {
            "answer": result_text,
            "question": query_param,
            "history_id": history_id_val
        }
    }
    return JsonResponse(re_data)

def insert_history(username, query_param):
    conn = get_connection()
    cur = conn.cursor()
    sql = "INSERT INTO history (query_param, username) VALUES (%s, %s)"
    try:
        cur.execute(sql, [query_param, username])
        conn.commit()
        cur.execute("SELECT LAST_INSERT_ID()")  # 获取最后插入的ID
        result = cur.fetchone()
        print(f"新插入的 history_id: {result[0]}")  # 打印新插入的主键
        return {
            "status": 200,
            "history_id": result[0]
        }
    except Exception as e:
        print(traceback.format_exc())
        conn.rollback()
        return {
            "status": 500,
            "error": str(e)
        }
    finally:
        cur.close()
        conn.close()
def qa_list(request):
    try:
        username = request.GET.get('username')
        query_Param = request.GET.get('queryParam')
        print(f"Received username: {username}")
        print(f"Received queryParam: {query_Param}")

        # 检查参数是否为空
        if not username or not query_Param:
            return JsonResponse({
                "status": 400,
                "error": "Missing username or queryParam"
            })

        id = history_id(username, query_Param)[0][0]
        result = qa(id)
        return JsonResponse({
            "status": 200,
            "data": result
        })
    except Exception as e:
        logger.error(f"An error occurred in qa_list: {str(e)}")
        return JsonResponse({
            "status": 500,
            "error": "Internal server error"
        })
def history_id(username, query_param):
    conn = get_connection()
    cur = conn.cursor()
    sql = "select history_id from history where username=%s and query_param=%s;"
    cur.execute(sql, [username, query_param])
    result = cur.fetchall()

    return result


def qa(id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = "select question, answer from qa where qa_fk_history=%s;"
        cur.execute(sql, [id])
        result = cur.fetchall()
        data_list = []
        for i in result:
            data_list.append({
                "question": i[0],
                "answer": i[1],
            })
        return data_list
    except DatabaseError as e:
        logger.error(f"Database error in qa: {str(e)}")
        raise Exception("Database error occurred") from e
    except Exception as e:
        logger.error(f"An error occurred in qa: {str(e)}")
        raise Exception("Error occurred") from e
