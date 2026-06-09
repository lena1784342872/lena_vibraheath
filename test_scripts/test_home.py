"""
首页测试用例
对应CSV测试用例：1-11
"""
import pytest
import allure
from pages.home_page import HomePage
from pages.services_page import ServicesPage
from pages.events_page import EventsPage
from pages.data_platform_page import DataPlatformPage
from pages.about_page import AboutPage
import time


@allure.feature("首页模块")
class TestHomePage:
    """首页测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """
        每个测试用例执行前的准备工作
        autouse=True 表示自动执行，无需手动调用
        """
        self.home_page = HomePage(page)
        self.services_page = ServicesPage(page)
        self.events_page = EventsPage(page)
        self.data_platform_page = DataPlatformPage(page)
        self.about_page = AboutPage(page)

    @allure.story("页面访问")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC001-进入官方网站")
    def test_tc001_access_homepage(self):
        """
        用例编号: 1
        验证能够正常访问官方网站首页
        """
        with allure.step("步骤1: 打开浏览器，输入网址"):
            self.home_page.navigate_to_home()



        with allure.step("验证: 左上角展示'vibrahealth'"):
            assert self.home_page.is_visible(self.home_page.LOGO), "Logo未显示"

        with allure.step("验证: 展示'首页'字段"):
            assert self.home_page.get_text(self.home_page.MENU_HOME).strip() == "首页"

        with allure.step("验证: 展示'专属服务'字段"):
            assert self.home_page.get_text(self.home_page.MENU_SERVICES).strip() == "专属服务"

    @allure.story("页面访问")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC002-不同分辨率展示正常")
    def test_tc002_responsive_display(self, context):
        """
        用例编号: 2
        验证在不同分辨率下页面展示正常
        """
        with allure.step("步骤1: 设置分辨率为1440x900"):
            self.home_page.page.set_viewport_size({"width": 1440, "height": 900})

        with allure.step("步骤2: 打开网站首页"):
            self.home_page.navigate_to_home()

        with allure.step("验证: 页面元素显示正常"):
            assert self.home_page.verify_home_loaded()

    @allure.story("导航功能")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC003-顶部导航栏切换页面")
    def test_tc003_top_navigation(self):
        """
        用例编号: 3
        验证点击顶部导航栏可以正常切换页面
        """
        with allure.step("步骤1: 打开首页"):
            self.home_page.navigate_to_home()

        with allure.step("步骤2: 点击'专属服务'进入专属服务页面"):
            self.home_page.click_services_menu()
            #验证‘团队介绍’字段
            assert self.services_page.verify_services_loaded()

        with allure.step("步骤3: 点击'大事件'进入大事件页面"):
            self.events_page.navigate_to_events()
            assert self.events_page.verify_events_loaded()

        with allure.step("步骤4: 点击'健康数据平台'进入健康数据平台页面"):
            self.data_platform_page.navigate_to_data_platform()
            assert self.data_platform_page.verify_data_platform_loaded()

        with allure.step("步骤5: 点击'关于我们'进入关于我们页面"):
            self.about_page.navigate_to_about()
            assert self.about_page.verify_about_loaded()

    @allure.story("健康管理服务")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC004-生命周期健康管理服务切换")
    def test_tc004_health_service_tabs(self):
        """
        用例编号: 4
        验证生命周期健康管理服务的tab切换功能
        """
        with allure.step("步骤1: 打开首页并滚动到健康管理服务区域"):
            self.home_page.navigate_to_home()
            self.home_page.scroll_to_health_service()

        with allure.step("步骤2: 点击'健康管理'"):
            self.home_page.click_health_management_tab()
            time.sleep(2)
            assert self.home_page.verify_health_management_content()

        with allure.step("步骤3: 点击'轻医疗'"):
            self.home_page.click_light_medical_tab()
            assert self.home_page.verify_light_medical_content()

        with allure.step("步骤4: 点击'严肃医疗'"):
            self.home_page.click_serious_medical_tab()
            assert self.home_page.verify_serious_medical_content()

    @allure.story("AI服务")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC005-AI健康管理服务展示")
    def test_tc005_ai_service(self):
        """
        用例编号: 5
        验证AI健康管理服务区域展示正常
        """
        with allure.step("步骤1: 打开首页并滚动到AI服务区域"):
            self.home_page.navigate_to_home()
            self.home_page.scroll_to_ai_service()

        with allure.step("验证: 展示'AI健康管理服务'字段"):
            assert self.home_page.verify_ai_service_title()

        with allure.step("验证: 展示'AI智能健康管理服务中心'字段"):
            assert self.home_page.verify_ai_service_center()

    @allure.story("底部导航")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC006-导航目录展示")
    def test_tc006_footer_navigation(self):
        """
        用例编号: 6
        验证页面底部导航目录展示正常
        """
        with allure.step("步骤1: 打开首页并滚动到底部"):
            self.home_page.navigate_to_home()
            self.home_page.scroll_to_bottom()

        with allure.step("验证: 展示'导航目录'和'联系方式'"):
            assert self.home_page.verify_footer_navigation()

    @allure.story("底部导航")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC007-底部导航栏切换专属服务")
    def test_tc007_footer_services_link(self):
        """
        用例编号: 7
        验证点击底部导航栏的'专属服务'可以切换页面
        """
        with allure.step("步骤1: 打开首页并滚动到底部"):
            self.home_page.navigate_to_home()
            self.home_page.scroll_to_bottom()

        with allure.step("步骤2: 点击底部'专属服务'链接"):
            self.home_page.click_footer_services()

        with allure.step("验证: 专属服务页面加载成功"):
            assert self.services_page.verify_services_loaded()

    @allure.story("底部导航")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC008-底部导航栏切换大事件")
    def test_tc008_footer_events_link(self):
        """
        用例编号: 8
        验证点击底部导航栏的'大事件'可以切换页面
        """
        with allure.step("步骤1: 打开首页并滚动到底部"):
            self.home_page.navigate_to_home()
            self.home_page.scroll_to_bottom()

        with allure.step("步骤2: 点击底部'大事件'链接"):
            self.home_page.click_footer_events()

        with allure.step("验证: 大事件页面加载成功"):
            assert self.events_page.verify_events_loaded()

    @allure.story("底部导航")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC009-底部导航栏切换健康数据平台")
    def test_tc009_footer_data_platform_link(self):
        """
        用例编号: 9
        验证点击底部导航栏的'健康数据平台'可以切换页面
        """
        with allure.step("步骤1: 打开首页并滚动到底部"):
            self.home_page.navigate_to_home()
            self.home_page.scroll_to_bottom()

        with allure.step("步骤2: 点击底部'健康数据平台'链接"):
            self.home_page.click_footer_data_platform()

        with allure.step("验证: 健康数据平台页面加载成功"):
            assert self.data_platform_page.verify_data_platform_loaded()

    @allure.story("底部导航")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC010-底部导航栏切换关于我们")
    def test_tc010_footer_about_link(self):
        """
        用例编号: 10
        验证点击底部导航栏的'关于我们'可以切换页面
        """
        with allure.step("步骤1: 打开首页并滚动到底部"):
            self.home_page.navigate_to_home()
            self.home_page.scroll_to_bottom()

        with allure.step("步骤2: 点击底部'关于我们'链接"):
            self.home_page.click_footer_about()

        with allure.step("验证: 关于我们页面加载成功"):
            assert self.about_page.verify_about_loaded()


