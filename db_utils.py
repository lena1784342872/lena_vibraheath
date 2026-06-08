# db_utils.py
from sshtunnel import SSHTunnelForwarder
import pymysql

# ========== 配置（直接写在文件里，不依赖环境变量）==========
SSH_HOST = '139.224.102.87'
SSH_PORT = 1622
SSH_USER = 'lena'
SSH_PASSWORD = 'w5yGK17490Zhp6r3'

RDS_HOST = 'rm-uf62gi7a28z3vcz8g.mysql.rds.aliyuncs.com'
RDS_PORT = 3306
DB_USER = 'dev_user'
DB_PASSWORD = 'AE4jKCoI3OlqaGnTgFQM'
DB_NAME = 'stg'
DB_CHARSET = 'utf8mb4'


# ========== 封装函数 ==========
def delete_test_data_by_phone(mobile: str) -> int:
    """
    通过 SSH 隧道连接 RDS，删除指定手机号的测试数据。

    :param phone: 要删除的手机号
    :return: 删除的记录数
    """
    # 1. 创建 SSH 隧道
    with SSHTunnelForwarder(
            (SSH_HOST, SSH_PORT),
            ssh_username=SSH_USER,
            ssh_password=SSH_PASSWORD,
            remote_bind_address=(RDS_HOST, RDS_PORT),
            local_bind_address=('127.0.0.1', 0) # 让系统自动分配空闲端口
    ) as tunnel:
        print(f"✅ SSH 隧道已建立，本地转发端口: {tunnel.local_bind_port}")

        # 2. 通过隧道连接数据库
        conn = pymysql.connect(
            host='127.0.0.1',
            port=tunnel.local_bind_port,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset=DB_CHARSET
        )

        try:
            with conn.cursor() as cursor:
                # 3. 执行删除（参数化查询，避免 SQL 注入）
                sql = "DELETE FROM `vh_applications` WHERE mobile = %s"
                affected_rows = cursor.execute(sql, (mobile,))
                conn.commit()
                print(f"✅ 清理完成，共删除 {affected_rows} 条手机号为 {mobile} 的测试数据")
                return affected_rows
        except Exception as e:
            conn.rollback()
            print(f"❌ 数据清理失败: {e}")
            raise
        finally:
            conn.close()
            print("🔒 数据库连接已关闭")

    # 隧道自动关闭
    print("🔒 SSH 隧道已自动关闭")


def list_databases():
    """通过 SSH 隧道连接 RDS，列出所有数据库"""
    with SSHTunnelForwarder(
        (SSH_HOST, SSH_PORT),
        ssh_username=SSH_USER,
        ssh_password=SSH_PASSWORD,
        remote_bind_address=(RDS_HOST, RDS_PORT),
        local_bind_address=('127.0.0.1', 0)
    ) as tunnel:
        print(f"✅ SSH 隧道已建立，本地端口: {tunnel.local_bind_port}")
        conn = pymysql.connect(
            host='127.0.0.1',
            port=tunnel.local_bind_port,
            user=DB_USER,
            password=DB_PASSWORD,
            charset=DB_CHARSET
        )
        with conn.cursor() as cursor:
            cursor.execute("SHOW DATABASES")
            print("\n📋 数据库列表：")
            for db in cursor.fetchall():
                print(f"  - {db[0]}")
        conn.close()