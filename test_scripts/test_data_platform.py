"""
健康数据平台测试用例
对应CSV测试用例：23-25
"""
import pytest
import allure
from pages.data_platform_page import DataPlatformPage


@allure.feature("健康数据平台模块")
class TestDataPlatformPage:
    """健康数据平台测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """初始化页面对象"""
        self.data_platform_page = DataPlatformPage(page)

    @allure.story("页面访问")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC023-健康数据平台页面响应正常")
    def test_tc023_access_data_platform(self):
        """
        用例编号: 23
        验证健康数据平台页面可以正常访问
        """
        with allure.step("步骤1: 打开健康数据平台页面"):
            self.data_platform_page.navigate_to_data_platform()

        with allure.step("验证: 页面加载成功"):
            assert self.data_platform_page.verify_data_platform_loaded()

    @allure.story("数字健康管理")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC024-全天候数字健康管理展示")
    def test_tc024_digital_health(self):
        """
        用例编号: 24
        验证全天候数字健康管理区域展示正常
        """
        with allure.step("步骤1: 打开健康数据平台页面"):
            self.data_platform_page.navigate_to_data_platform()

        with allure.step("步骤2: 滚动到全天候数字健康管理区域"):
            self.data_platform_page.scroll_to_digital_health()

        with allure.step("验证: 全天候数字健康管理标题显示"):
            assert self.data_platform_page.verify_digital_health_title()

        with allure.step("验证: 全天候数字健康管理描述显示"):
            assert self.data_platform_page.verify_digital_health_description()

    @allure.story("可视化大屏")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC025-可视化大屏展示")
    def test_tc025_visual_dashboard(self):
        """
        用例编号: 25
        验证可视化大屏分析身体指标区域展示正常
                """
        with allure.step("步骤1: 打开健康数据平台页面"):
            self.data_platform_page.navigate_to_data_platform()

        with allure.step("步骤2: 滚动到可视化大屏区域"):
            self.data_platform_page.scroll_to_visual_dashboard()

        with allure.step("验证: 可视化大屏标题显示"):
            assert self.data_platform_page.verify_visual_dashboard_title()

        with allure.step("验证: 可视化大屏图片显示"):
            self.data_platform_page.verify_visual_dashboard_image()
