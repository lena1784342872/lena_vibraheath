"""
专属服务页面对象
封装专属服务页面的所有操作
对应测试用例：12-16
"""
import allure
from pages.base_page import BasePage
from playwright.sync_api import Page


class ServicesPage(BasePage):
    """专属服务页面类"""

    # ==================== 元素定位器 ====================
    # 页面标题
    PAGE_TITLE =  "nav.nav a:has-text('专属服务')"

    # 团队介绍区域
    TEAM_INTRO_SECTION = "section.team-container p:has-text('团队介绍')"
    TEAM_INTRO_TITLE = "section.team-container h2:has-text('Team Introduction')"
    TEAM_INTRO_DESC = "div.content-container div:has-text('我们为您组建多领域专家协同专业服务团队。以预防为起点，从风险评估到个性化干预，从科学膳食规划到功能运动指导，全程贴心陪伴。灵活匹配您不同阶段的需求，让疾病止步于萌芽，守护您人生每一程的健康品质。')"


    # 专属医生团队区域
    MEDICAL_TEAM_SECTION = "text=Individually Assigned Medical Team"
    MEDICAL_TEAM_TITLE = "section.doctor-team-container h2:has-text('Individually Assigned Medical Team')"
    MEDICAL_TEAM_MEMBERS = "div.doctor-list-container h4:has-text('专属管家')"

    # 服务流程区域
    SERVICE_PROCESS_SECTION = "section.service-process-container p:has-text('服务流程')"
    PROCESS_STEP_01 = "div.item-process p:has-text('预约申请')"
    PROCESS_STEP_02 ="div.item-process p:has-text('全析健康评估')"

    # 健康管理计划区域
    HEALTH_PLAN_SECTION = "section.health-plan-container p:has-text('健康管理计划')"
    PLAN_FEATURE_PERSONAL = "div.plan-container p:has-text('个性：量身定制专属方案，精准匹配个体健康需求')"
    PLAN_FEATURE_GOAL = "div.plan-container p:has-text('价值：长期健康效益可量化，提升生命质量，提高生活品质')"


    def __init__(self, page: Page):
        """初始化专属服务页面"""
        super().__init__(page)

    @allure.step("导航到专属服务页面")
    def navigate_to_services(self):
        """打开专属服务页面"""
        self.goto("/services")
        return self

    @allure.step("验证专属服务页面加载成功")
    def verify_services_loaded(self):
        """验证页面是否正确加载"""
        assert self.get_text(self.PAGE_TITLE).strip() == "专属服务"
        assert self.is_visible(self.TEAM_INTRO_TITLE), "'团队介绍'未显示"
        print("✓ 专属服务页面加载成功")
        return True

    @allure.step("滚动到团队介绍区域")
    def scroll_to_team_intro(self):
        """滚动到团队介绍区域"""
        self.scroll_to_element(self.TEAM_INTRO_SECTION)

    @allure.step("验证团队介绍标题显示")
    def verify_team_intro_title(self):
        """验证团队介绍标题是否显示"""
        assert self.get_text(self.TEAM_INTRO_TITLE) == "Team Introduction"
        return True

    @allure.step("验证团队介绍描述显示")
    def verify_team_intro_description(self):
        """验证团队介绍的描述文字是否显示"""
        assert self.is_visible(self.TEAM_INTRO_DESC), "团队介绍描述未显示"
        return True


    @allure.step("滚动到专属医生团队区域")
    def scroll_to_medical_team(self):
        """滚动到医生团队区域"""
        self.scroll_to_element(self.MEDICAL_TEAM_SECTION)

    @allure.step("验证医生团队标题显示")
    def verify_medical_team_title(self):
        """验证医生团队标题是否显示"""
        assert self.get_text(self.MEDICAL_TEAM_TITLE) == "Individually Assigned Medical Team"
        return True

    @allure.step("验证医生团队成员介绍显示")
    def verify_medical_team_members(self):
        """验证医生团队成员介绍是否显示"""
        assert self.is_visible(self.MEDICAL_TEAM_MEMBERS), "医生团队成员介绍未显示"
        return True

    @allure.step("滚动到服务流程区域")
    def scroll_to_service_process(self):
        """滚动到服务流程区域"""
        self.scroll_to_element(self.SERVICE_PROCESS_SECTION)

    @allure.step("验证服务流程7个步骤全部显示")
    def verify_all_process_steps(self):
        """验证2个服务流程步骤是否都显示"""
        steps = [
            self.PROCESS_STEP_01,
            self.PROCESS_STEP_02
        ]

        for i, step_locator in enumerate(steps, 1):
            assert self.is_visible(step_locator), f"第{i}步流程未显示"

        print("✓ 2个服务流程步骤全部显示")
        return True

    @allure.step("滚动到健康管理计划区域")
    def scroll_to_health_plan(self):
        """滚动到健康管理计划区域"""
        self.scroll_to_element(self.HEALTH_PLAN_SECTION)

    @allure.step("验证健康管理计划特性显示")
    def verify_health_plan_features(self):
        """验证健康管理计划的3个特性是否显示"""
        assert self.get_text(self.PLAN_FEATURE_PERSONAL) == "个性：量身定制专属方案，精准匹配个体健康需求"
        assert self.is_visible(self.PLAN_FEATURE_GOAL), "'价值'特性未显示"
        print("✓ 健康管理计划特性显示正常")
        return True
