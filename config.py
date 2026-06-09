"""
全局配置文件
统一管理所有配置项，方便修改和维护
"""
import os
from dotenv import load_dotenv


class Config:
    # 加载 .env 文件（如果存在）
    load_dotenv()

    """配置类 - 存储所有测试相关的配置信息"""

    # ==================== URL 配置 ====================
    # 统一基础域名（解决CSV中stg和正式环境混用的问题）
    BASE_URL = "https://stg.vibrahealth.cn"

    # 各页面路径（只写路径部分，不包含域名）
    PAGES = {
        "home": "/",  # 首页
        "services": "/services",  # 专属服务
        "events": "/events",  # 大事件
        "data_platform": "/data-platform",  # 健康数据平台
        "about": "/about",  # 关于我们
    }

    # ---------- 浏览器配置 ----------
    BROWSER_CONFIG = {
        # 是否无头模式：True=后台运行（CI），False=显示窗口（本地）
        "headless": os.getenv("HEADLESS", "false").lower() == "true",
        # 操作延迟（毫秒），本地调试建议 300，CI 可设为 0
        "slow_mo": int(os.getenv("SLOW_MO", "0")),
        # 视口宽度
        "viewport_width": int(os.getenv("VIEWPORT_WIDTH", "1920")),
        # 视口高度
        "viewport_height": int(os.getenv("VIEWPORT_HEIGHT", "1080")),
    }

    # ==================== 超时配置 ====================
    TIMEOUTS = {
        "page_load": 30000,  # 页面加载超时：30秒
        "element_wait": 10000,  # 元素等待超时：10秒
        "default": 5000,  # 默认超时：5秒
    }

    # ==================== 测试数据 ====================
    # 表单提交测试数据（固定值，方便验证）
    FORM_DATA_HEALTH = {
        "surname": "chen",  # 姓氏
        "name": "lena",  # 名字
        "phone": "16566666666",  # 手机号
        "age": "20-30岁",  # 年龄段
        "concerns": ["抗衰管理", "睡眠管理", "家庭管理"]  # 关注的健康问题
    }

    FORM_DATA_PARTNER = {
        "surname": "chen",
        "name": "lena",
        "phone": "16566666666",
        "age": "20-30岁",
        "current_job": "护士",  # 当前职位
        "apply_job": "护士"  # 申请职位
    }

    # ==================== 文件路径 ====================
    # 获取项目根目录的绝对路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # CSV测试用例文件路径
    CSV_FILE = os.path.join(BASE_DIR, "test_data", "官方网站回归测试用例 - Sheet1.csv")

    # 报告目录
    ALLURE_RESULTS = os.path.join(BASE_DIR, "reports")
    ALLURE_HTML = os.path.join(BASE_DIR, "allure_html_report")

    # 截图保存目录
    SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")



# 创建配置实例，其他文件可以直接导入使用
config = Config()
