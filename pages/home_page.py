"""
首页页面对象
封装首页的所有元素定位和操作方法
对应测试用例：1-11
"""
import allure
from pages.base_page import BasePage
from playwright.sync_api import Page


class HomePage(BasePage):
    """首页类 - 继承自 BasePage"""

    # ==================== 元素定位器 ====================
    # Logo 区域
    LOGO = "h1.logo-name"

    # 顶部导航菜单
    MENU_HOME = "nav.nav a:has-text('首页')"
    MENU_SERVICES = "nav.nav a:has-text('专属服务')"
    MENU_EVENTS =  "nav.nav a:has-text('大事件')"
    MENU_DATA_PLATFORM = "nav.nav a:has-text('健康数据平台')"
    MENU_ABOUT ="nav.nav a:has-text('关于我们')"

    # 生命周期健康管理服务区域
    SECTION_HEALTH_SERVICE = "section.service-container p:has-text('全生命周期闭环健康管理服务')"
    TAB_HEALTH_MANAGEMENT = "div.service-list h4:has-text('健康管理')"
    TAB_LIGHT_MEDICAL = "text=轻医疗"
    TAB_SERIOUS_MEDICAL = "text=严肃医疗"

    # 健康管理内容
    CONTENT_HEALTH = "div.service-item p:has-text('筛查检测: ')"
    CONTENT_LIGHT_MEDICAL = "text=早癌筛查"
    CONTENT_SERIOUS_MEDICAL = "text=重大疾病住院"

    # AI 健康管理服务区域
    SECTION_AI_SERVICE = "text=AI健康管理服务"
    AI_SERVICE_CENTER = "div.card-container h5:has-text('AI智能健康管理服务中心')"

    # 底部导航区域
    FOOTER_NAVIGATION = "div.item-container h3:has-text('导航目录')"
    FOOTER_CONTACT = "div.item-container h3:has-text('联系方式')"
    FOOTER_SERVICES_LINK = "footer a:has-text('专属服务')"
    FOOTER_EVENTS_LINK = "footer a:has-text('大事件')"
    FOOTER_DATA_LINK = "footer a:has-text('健康数据平台')"
    FOOTER_ABOUT_LINK = "footer a:has-text('关于我们')"



    def __init__(self, page: Page):
        """初始化首页对象"""
        super().__init__(page)

    @allure.step("导航到首页")
    def navigate_to_home(self):
        """打开首页"""
        self.goto("/")
        return self

    @allure.step("验证首页加载成功")
    def verify_home_loaded(self):
        """验证首页是否正确加载"""
        # 检查 Logo 是否显示
        assert self.is_visible(self.LOGO), "Logo 未显示"
        # 检查首页菜单是否显示
        assert self.get_text(self.MENU_HOME).strip() == "首页"
        # 检查专属服务菜单是否显示
        assert self.get_text(self.MENU_SERVICES).strip() == "专属服务"
        print("✓ 首页加载成功验证通过")
        return True

    @allure.step("点击顶部'专属服务'菜单")
    def click_services_menu(self):
        """点击顶部导航的专属服务"""
        self.click_element(self.MENU_SERVICES)

    @allure.step("点击顶部'大事件'菜单")
    def click_events_menu(self):
        """点击顶部导航的大事件"""
        self.click_element(self.MENU_EVENTS)

    @allure.step("点击顶部'健康数据平台'菜单")
    def click_data_platform_menu(self):
        """点击顶部导航的健康数据平台"""
        self.click_element(self.MENU_DATA_PLATFORM)

    @allure.step("点击顶部'关于我们'菜单")
    def click_about_menu(self):
        """点击顶部导航的关于我们"""
        self.click_element(self.MENU_ABOUT)

    @allure.step("滚动到生命周期健康管理服务区域")
    def scroll_to_health_service(self):
        """滚动页面到健康管理服务区域"""
        self.scroll_to_element(self.SECTION_HEALTH_SERVICE)

    @allure.step("点击'健康管理'Tab")
    def click_health_management_tab(self):
        """点击健康管理标签"""
        self.click_element(self.TAB_HEALTH_MANAGEMENT)
        self.wait(1000)  # 等待内容切换动画完成

    @allure.step("点击'轻医疗'Tab")
    def click_light_medical_tab(self):
        """点击轻医疗标签"""
        self.click_element(self.TAB_LIGHT_MEDICAL)
        self.wait(1000)

    @allure.step("点击'严肃医疗'Tab")
    def click_serious_medical_tab(self):
        """点击严肃医疗标签"""
        self.click_element(self.TAB_SERIOUS_MEDICAL)
        self.wait(1000)

    @allure.step("验证健康管理内容显示")
    def verify_health_management_content(self):
        """验证健康管理Tab的内容是否正确显示"""
        assert self.is_visible(self.CONTENT_HEALTH), "健康管理内容未显示"
        return True

    @allure.step("验证轻医疗内容显示")
    def verify_light_medical_content(self):
        """验证轻医疗Tab的内容是否正确显示"""
        assert self.is_visible(self.CONTENT_LIGHT_MEDICAL), "轻医疗内容未显示"
        return True

    @allure.step("验证严肃医疗内容显示")
    def verify_serious_medical_content(self):
        """验证严肃医疗Tab的内容是否正确显示"""
        assert self.is_visible(self.CONTENT_SERIOUS_MEDICAL), "严肃医疗内容未显示"
        return True

    @allure.step("滚动到AI健康管理服务区域")
    def scroll_to_ai_service(self):
        """滚动到AI服务区域"""
        self.scroll_to_element(self.SECTION_AI_SERVICE)

    @allure.step("验证AI服务标题显示")
    def verify_ai_service_title(self):
        """验证AI健康管理服务标题是否显示"""
        assert self.is_visible(self.SECTION_AI_SERVICE), "AI服务标题未显示"
        return True

    @allure.step("验证AI服务中心文字显示")
    def verify_ai_service_center(self):
        """验证AI智能健康管理服务中心文字是否显示"""
        assert self.get_text(self.AI_SERVICE_CENTER) == "AI智能健康管理服务中心"
        return True


    @allure.step("滚动到页面底部")
    def scroll_to_bottom(self):
        """滚动到页面最底部"""
        # 使用 JavaScript 滚动到页面底部
        self.page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
        self.wait(2000)
        # 确保底部导航元素可见
        if self.is_visible(self.FOOTER_NAVIGATION):
            self.page.locator(self.FOOTER_NAVIGATION).scroll_into_view_if_needed()
            self.wait(500)

    @allure.step("验证底部导航目录显示")
    def verify_footer_navigation(self):
        """验证底部导航目录是否显示"""
        assert self.get_text(self.FOOTER_NAVIGATION) == "导航目录"
        assert self.get_text(self.FOOTER_CONTACT) == "联系方式"
        return True


    @allure.step("点击底部'专属服务'链接")
    def click_footer_services(self):
        """点击底部导航的专属服务链接"""
        self.click_element(self.FOOTER_SERVICES_LINK)

    @allure.step("点击底部'大事件'链接")
    def click_footer_events(self):
        """点击底部导航的大事件链接"""
        self.click_element(self.FOOTER_EVENTS_LINK)

    @allure.step("点击底部'健康数据平台'链接")
    def click_footer_data_platform(self):
        """点击底部导航的健康数据平台链接"""
        self.click_element(self.FOOTER_DATA_LINK)

    @allure.step("点击底部'关于我们'链接")
    def click_footer_about(self):
        """点击底部导航的关于我们链接"""
        self.click_element(self.FOOTER_ABOUT_LINK)
