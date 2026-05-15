"""
健康数据平台页面对象
封装健康数据平台页面的所有操作
对应测试用例：23-25
"""
import allure
from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class DataPlatformPage(BasePage):
    """健康数据平台页面类"""

    # ==================== 元素定位器 ====================
    # 页面标题
    PAGE_TITLE = "section.banner-container h3:has-text('健康数据平台')"

    # 全天候数字健康管理区域
    DIGITAL_HEALTH_SECTION = "section.data-manage-container h2.section-title"
    DIGITAL_HEALTH_TITLE = "text=全天候数字健康管理"
    DIGITAL_HEALTH_DESC = "text=由专业人士整理您的历年健康报告"

    # 可视化大屏区域
    VISUAL_DASHBOARD_SECTION = "section.body-indicators-container h2.section-title"
    VISUAL_DASHBOARD_TITLE = "text=可视化大屏分析身体指标"
    VISUAL_DASHBOARD_DESC = "text=健康数据可视化大屏"
    VISUAL_DASHBOARD_IMAGE = "video#indicatorVideo"

    def __init__(self, page: Page):
        """初始化健康数据平台页面"""
        super().__init__(page)

    @allure.step("导航到健康数据平台页面")
    def navigate_to_data_platform(self):
        """打开健康数据平台页面"""
        self.goto("/data-platform")
        return self

    @allure.step("验证健康数据平台页面加载成功")
    def verify_data_platform_loaded(self):
        """验证页面是否正确加载"""
        assert self.get_text(self.PAGE_TITLE) == "健康数据平台"
        print("✓ 健康数据平台页面加载成功")
        return True

    @allure.step("滚动到全天候数字健康管理区域")
    def scroll_to_digital_health(self):
        """滚动到全天候数字健康管理区域"""
        self.scroll_to_element(self.DIGITAL_HEALTH_SECTION)

    @allure.step("验证全天候数字健康管理标题显示")
    def verify_digital_health_title(self):
        """验证全天候数字健康管理标题是否显示"""
        assert self.is_visible(self.DIGITAL_HEALTH_TITLE), "全天候数字健康管理标题未显示"
        return True

    @allure.step("验证全天候数字健康管理描述显示")
    def verify_digital_health_description(self):
        """验证全天候数字健康管理的描述文字是否显示"""
        assert self.is_visible(self.DIGITAL_HEALTH_DESC), "描述文字未显示"
        return True

    @allure.step("滚动到可视化大屏区域")
    def scroll_to_visual_dashboard(self):
        """滚动到可视化大屏区域"""
        self.scroll_to_element(self.VISUAL_DASHBOARD_SECTION)

    @allure.step("验证可视化大屏标题显示")
    def verify_visual_dashboard_title(self):
        """验证可视化大屏标题是否显示"""
        assert self.is_visible(self.VISUAL_DASHBOARD_TITLE), "可视化大屏标题未显示"
        return True



    @allure.step("验证可视化大屏图片显示")
    def verify_visual_dashboard_image(self):
        """验证可视化大屏的图片/动图是否显示"""
        #assert self.is_visible(self.VISUAL_DASHBOARD_IMAGE), "可视化大屏图片未显示"
        #return True
        expect(self.page.locator(self.VISUAL_DASHBOARD_IMAGE)).to_be_visible()


