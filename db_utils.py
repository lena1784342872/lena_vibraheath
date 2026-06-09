import os
from dotenv import load_dotenv
import pymysql

# 只在本地有 .env 文件时加载（CI 中没有 .env 也不会报错）
load_dotenv()

# ========== 配置（保留你的硬编码，但允许环境变量覆盖）==========
SSH_HOST = os.getenv('SSH_HOST', '139.224.102.87')
SSH_PORT = int(os.getenv('SSH_PORT', '1622'))
SSH_USER = os.getenv('SSH_USER', 'lena')
SSH_PASSWORD = os.environ.get('SSH_PASSWORD')
if not SSH_PASSWORD:
    raise ValueError("SSH_PASSWORD environment variable is required")

RDS_HOST = os.getenv('RDS_HOST', 'rm-uf62gi7a28z3vcz8g.mysql.rds.aliyuncs.com')
RDS_PORT = int(os.getenv('RDS_PORT', '3306'))
DB_USER = os.getenv('DB_USER', 'dev_user')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD environment variable is required")
DB_NAME = os.getenv('DB_NAME', 'stg')
DB_CHARSET = 'utf8mb4'

# ========== 封装函数 ==========
def delete_test_data_by_phone(mobile: str) -> int:
    from sshtunnel import SSHTunnelForwarder

    with SSHTunnelForwarder(
            (SSH_HOST, SSH_PORT),
            ssh_username=SSH_USER,
            ssh_password=SSH_PASSWORD,
            remote_bind_address=(RDS_HOST, RDS_PORT),
            local_bind_address=('127.0.0.1', 0)
    ) as tunnel:
        print(f"✅ SSH tunnel established, local port: {tunnel.local_bind_port}")
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
                sql = "DELETE FROM `vh_applications` WHERE mobile = %s"
                affected_rows = cursor.execute(sql, (mobile,))
                conn.commit()
                print(f"✅ Deleted {affected_rows} records for phone {mobile}")
                return affected_rows
        except Exception as e:
            conn.rollback()
            print(f"❌ Failed: {e}")
            raise
        finally:
            conn.close()

def list_databases():
    from sshtunnel import SSHTunnelForwarder
    with SSHTunnelForwarder(
        (SSH_HOST, SSH_PORT),
        ssh_username=SSH_USER,
        ssh_password=SSH_PASSWORD,
        remote_bind_address=(RDS_HOST, RDS_PORT),
        local_bind_address=('127.0.0.1', 0)
    ) as tunnel:
        conn = pymysql.connect(
            host='127.0.0.1',
            port=tunnel.local_bind_port,
            user=DB_USER,
            password=DB_PASSWORD,
            charset=DB_CHARSET
        )
        with conn.cursor() as cursor:
            cursor.execute("SHOW DATABASES")
            print("\n📋 Databases:")
            for db in cursor.fetchall():
                print(f"  - {db[0]}")
        conn.close()