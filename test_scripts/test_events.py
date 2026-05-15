"""
大事件测试用例
对应CSV测试用例：17-22
"""
import pytest
import allure
from pages.events_page import EventsPage
from config import config


@allure.feature("大事件模块")
class TestEventsPage:
    """大事件测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """初始化页面对象"""
        self.events_page = EventsPage(page)

    @allure.story("页面访问")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC017-大事件页面响应正常")
    def test_tc017_access_events(self):
        """
        用例编号: 17
        验证大事件页面可以正常访问
        """
        with allure.step("步骤1: 打开大事件页面"):
            self.events_page.navigate_to_events()

        with allure.step("验证: 页面加载成功"):
            assert self.events_page.verify_events_loaded()

    @allure.story("事件轮播")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC018-左右切换按钮切换事件内容")
    def test_tc018_event_slider(self):
        """
        用例编号: 18
        验证可以通过左右箭头按钮切换大事件内容
        """
        with allure.step("步骤1: 打开大事件页面"):
            self.events_page.navigate_to_events()

        with allure.step("步骤2: 滚动到Big Event区域"):
            self.events_page.scroll_to_big_event()

        with allure.step("验证: 第一个事件内容显示"):
            assert self.events_page.verify_first_event()

        with allure.step("步骤3: 点击向右箭头切换"):
            self.events_page.click_next_event()

        with allure.step("验证: 第二个事件内容显示"):
            assert self.events_page.verify_second_event()

    @allure.story("事件详情")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC019-点击大事件资讯跳转详情")
    def test_tc019_event_detail(self):
        """
        用例编号: 19
        验证点击大事件资讯可以跳转到详情页
        """
        with allure.step("步骤1: 打开大事件页面"):
            self.events_page.navigate_to_events()

        with allure.step("步骤2: 滚动到Big Event区域"):
            self.events_page.scroll_to_big_event()

        with allure.step("步骤3: 点击第一个事件资讯"):
            self.events_page.click_first_event_detail()

        with allure.step("验证: 事件详情页标题与预期一致"):
            assert self.events_page.verify_event_detail_title()=='研究发现：每天30分钟“微运动”可显著降低死亡风险'

        with allure.step("验证: 事件详情页日期显示"):
            assert self.events_page.verify_event_detail_date()



    @allure.story("健康资讯")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC021-健康资讯分类切换")
    def test_tc021_health_info_categories(self):
        """
        用例编号: 21
        验证健康资讯的分类切换功能正常
        """
        with allure.step("步骤1: 打开大事件页面"):
            self.events_page.navigate_to_events()

        with allure.step("步骤2: 滚动到健康资讯区域"):
            self.events_page.scroll_to_health_info()

        with allure.step("验证: 健康资讯分类显示"):
            assert self.events_page.verify_health_info_categories()

        with allure.step("步骤3: 点击'心血管'分类"):
            self.events_page.click_cardiovascular_category()
            assert self.events_page.verify_cardiovascular_articles()

        with allure.step("步骤4: 点击'丁香公开课'分类"):
            self.events_page.click_dingxiang_category()
            assert self.events_page.verify_dingxiang_articles()

    @allure.story("健康资讯")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC022-点击健康资讯跳转详情")
    def test_tc022_health_article_detail(self):
        """
        用例编号: 22
        验证点击健康资讯可以跳转到详情页
        """
        with allure.step("步骤1: 打开大事件页面"):
            self.events_page.navigate_to_events()

        with allure.step("步骤2: 滚动到健康资讯区域"):
            self.events_page.scroll_to_health_info()

        with allure.step("步骤3: 点击第一篇健康资讯"):
            self.events_page.click_first_health_article()

        with allure.step("验证: 资讯详情页标题显示"):
            assert self.events_page.verify_article_detail_title()

        with allure.step("验证: 资讯详情页日期显示"):
            assert self.events_page.verify_article_detail_date()
