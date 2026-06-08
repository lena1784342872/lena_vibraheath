"""
专属服务测试用例
对应CSV测试用例：12-16
"""
import pytest
import allure
from pages.services_page import ServicesPage


@allure.feature("专属服务模块")
class TestServicesPage:
    """专属服务测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """初始化页面对象"""
        self.services_page = ServicesPage(page)

    @allure.story("页面访问")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC012-专属服务页面响应正常")
    def test_tc012_access_services(self):
        """
        用例编号: 12
        验证专属服务页面可以正常访问
        """
        with allure.step("步骤1: 打开专属服务页面"):
            self.services_page.navigate_to_services()

        with allure.step("验证: 页面加载成功"):
            assert self.services_page.verify_services_loaded()

    @allure.story("团队介绍")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC013-团队介绍展示")
    def test_tc013_team_introduction(self):
        """
        用例编号: 13
        验证团队介绍区域的标题和图片内容展示正常
        """
        with allure.step("步骤1: 打开专属服务页面"):
            self.services_page.navigate_to_services()

        with allure.step("步骤2: 滚动到团队介绍区域"):
            self.services_page.scroll_to_team_intro()

        with allure.step("验证: 团队介绍标题显示"):
            assert self.services_page.verify_team_intro_title()

        with allure.step("验证: 团队介绍描述显示"):
            assert self.services_page.verify_team_intro_description()


    @allure.story("医生团队")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC014-专属医生团队展示")
    def test_tc014_medical_team(self):
        """
        用例编号: 14
        验证专属医生团队区域展示正常
        """
        with allure.step("步骤1: 打开专属服务页面"):
            self.services_page.navigate_to_services()

        with allure.step("步骤2: 滚动到医生团队区域"):
            self.services_page.scroll_to_medical_team()

        with allure.step("验证: 医生团队标题显示"):
            assert self.services_page.verify_medical_team_title()

        with allure.step("验证: 医生团队成员介绍显示"):
            assert self.services_page.verify_medical_team_members()

    @allure.story("服务流程")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC015-服务流程展示7个流程")
    def test_tc015_service_process(self):
        """
        用例编号: 15
        验证服务流程区域展示7个完整的流程步骤
        """
        with allure.step("步骤1: 打开专属服务页面"):
            self.services_page.navigate_to_services()

        with allure.step("步骤2: 滚动到服务流程区域"):
            self.services_page.scroll_to_service_process()

        with allure.step("验证: 7个流程步骤全部显示"):
            assert self.services_page.verify_all_process_steps()

    @allure.story("健康管理计划")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC016-健康管理计划展示")
    def test_tc016_health_plan(self):
        """
        用例编号: 16
        验证健康管理计划区域展示6个图框和介绍
        """
        with allure.step("步骤1: 打开专属服务页面"):
            self.services_page.navigate_to_services()

        with allure.step("步骤2: 滚动到健康管理计划区域"):
            self.services_page.scroll_to_health_plan()

        with allure.step("验证: 健康管理计划特性显示"):
            assert self.services_page.verify_health_plan_features()
