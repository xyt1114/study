import pymysql
pymysql.install_as_MySQLdb()
def get_connection():
    try:
        # 尝试连接数据库
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='123456',
            db='cdlg_app',
            charset='utf8mb4',
        )
        # 检查连接是否成功
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
        return connection
    except pymysql.Error as e:
        print(f"Database connection failed: {e}")
        return None