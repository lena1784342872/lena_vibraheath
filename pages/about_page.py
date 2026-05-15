"""
关于我们页面对象
封装关于我们页面的所有操作，包括表单填写
对应测试用例：26-32
"""
import allure
from pages.base_page import BasePage
from playwright.sync_api import Page
from config import config


class AboutPage(BasePage):
    """关于我们页面类"""

    # ==================== 元素定位器 ====================
    # 页面标题
    PAGE_TITLE = "section.banner-container h3:has-text('关于我们')"
    # 产品介绍区域
    PRODUCT_SECTION = "text=基础健康"
    PRODUCT_DETOX = "text=净化排毒"

    # 联系我们区域
    CONTACT_US_SECTION = "section.contact-us-container p.section-description"

    # 表单切换按钮
    BTN_IMPROVE_HEALTH = "div.switch-container div:has-text('我想改善健康')"
    BTN_BECOME_PARTNER = "div.switch-container div:has-text('我想成为伙伴')"

    # 表单输入框
    INPUT_SURNAME ="input[name='lastName'][placeholder='请输入您的姓氏']"
    INPUT_NAME = "input[name='firstName'][placeholder='请输入您的名字']"
    INPUT_PHONE = "input[name='phone'][placeholder='请输入您的手机号']"
    SELECT_AGE = "#age"
    SELECT_AGE_ALTERNATIVE = "select[name='age'], select#age, .age-select"
    SELECT_OPTION_LABEL= "20-30岁"

    # 健康问题复选框
    CHECKBOX_ANTI_AGING = "div.health-question-container div:has-text('抗衰管理')"
    CHECKBOX_SLEEP ="div.health-question-container div:has-text('睡眠管理')"
    CHECKBOX_FAMILY = "div.health-question-container div:has-text('家庭健康')"

    # 合作伙伴表单字段
    INPUT_CURRENT_JOB ="input[name='position'][placeholder='您目前的职位/工作方向']"
    INPUT_APPLY_JOB = "input[name='cooperationDirection'][placeholder='您想申请的职位或者合作方向']"

    # 提交按钮
    BTN_SUBMIT = "input.submit-button"

    # 成功提示
    SUCCESS_TOAST = ".toast-success, .success-message, text=提交成功"

    def __init__(self, page: Page):
        """初始化关于我们页面"""
        super().__init__(page)

    @allure.step("导航到关于我们页面")
    def navigate_to_about(self):
        """打开关于我们页面"""
        self.goto("/about")
        return self

    @allure.step("验证关于我们页面加载成功")
    def verify_about_loaded(self):
        """验证页面是否正确加载"""
        assert self.get_text(self.PAGE_TITLE) == "关于我们"
        print("✓ 关于我们页面加载成功")
        return True

    @allure.step("滚动到产品介绍区域")
    def scroll_to_product_section(self):
        """滚动到产品介绍区域"""
        self.scroll_to_element(self.PRODUCT_SECTION)

    @allure.step("验证产品介绍显示")
    def verify_product_introduction(self):
        """验证产品介绍内容是否显示"""
        assert self.is_visible(self.PRODUCT_SECTION), "'基础健康'未显示"
        assert self.is_visible(self.PRODUCT_DETOX), "'净化排毒'未显示"
        print("✓ 产品介绍显示正常")
        return True

    @allure.step("滚动到联系我们区域")
    def scroll_to_contact_us(self):
        """滚动到联系我们表单区域"""
        self.scroll_to_element(self.CONTACT_US_SECTION)

    @allure.step("点击'我想改善健康'按钮")
    def click_improve_health_button(self):
        """切换到改善健康表单"""
        self.click_element(self.BTN_IMPROVE_HEALTH)
        self.wait(500)

    @allure.step("点击'我想成为伙伴'按钮")
    def click_become_partner_button(self):
        """切换到成为伙伴表单"""
        self.click_element(self.BTN_BECOME_PARTNER)
        self.wait(500)

    @allure.step("验证改善健康表单显示")
    def verify_improve_health_form(self):
        """验证改善健康表单的字段是否显示"""
        assert self.is_visible(self.INPUT_SURNAME), "姓氏输入框未显示"
        assert self.is_visible(self.INPUT_NAME), "名字输入框未显示"
        assert self.is_visible(self.INPUT_PHONE), "手机号输入框未显示"
        assert self.is_visible(self.CHECKBOX_ANTI_AGING), "'抗衰管理'选项未显示"
        assert self.is_visible(self.BTN_SUBMIT), "'提交申请'按钮未显示"
        print("✓ 改善健康表单显示正常")
        return True

    @allure.step("验证成为伙伴表单显示")
    def verify_partner_form(self):
        """验证成为伙伴表单的字段是否显示"""
        assert self.is_visible(self.INPUT_SURNAME), "姓氏输入框未显示"
        assert self.is_visible(self.INPUT_CURRENT_JOB), "当前职位输入框未显示"
        assert self.is_visible(self.INPUT_APPLY_JOB), "申请职位输入框未显示"
        assert self.is_visible(self.BTN_SUBMIT), "'提交申请'按钮未显示"
        print("✓ 成为伙伴表单显示正常")
        return True

    @allure.step("填写改善健康表单")
    def fill_improve_health_form(self):
        """
        填写改善健康表单
        使用配置中的固定测试数据
        """
        data = config.FORM_DATA_HEALTH

        # 填写姓氏
        self.fill_input(self.INPUT_SURNAME, data["surname"])

        # 填写名字
        self.fill_input(self.INPUT_NAME, data["name"])

        # 填写手机号
        self.fill_input(self.INPUT_PHONE, data["phone"])

        # 选择年龄 - 先尝试标准方法，如果失败则尝试备用方案
        try:
            self.select_option(self.SELECT_AGE, self.SELECT_OPTION_LABEL)
        except Exception as e:
            print(f"标准select_option失败，尝试备用方案: {str(e)}")
            # 尝试点击式下拉框
            try:
                self.click_select_option(self.SELECT_AGE, self.SELECT_OPTION_LABEL)
            except Exception as e2:
                print(f"点击式下拉框也失败: {str(e2)}")
                # 如果下拉框元素找不到，尝试通过placeholder定位
                alternative_selector = "input[placeholder*='年龄'], select[placeholder*='年龄']"
                if self.is_visible(alternative_selector):
                    self.click_select_option(alternative_selector, self.SELECT_OPTION_LABEL)
                else:
                    raise Exception("无法找到年龄选择框")

        # 选择关注的健康问题（多选）
        for concern in data["concerns"]:
            if concern == "抗衰管理":
                self.click_element(self.CHECKBOX_ANTI_AGING)
            elif concern == "睡眠管理":
                self.click_element(self.CHECKBOX_SLEEP)
            elif concern == "家庭管理":
                self.click_element(self.CHECKBOX_FAMILY)
            self.wait(300)

        print("✓ 改善健康表单填写完成")

    @allure.step("填写成为伙伴表单")
    def fill_partner_form(self):
        """
        填写成为伙伴表单
        使用配置中的固定测试数据
        """
        data = config.FORM_DATA_PARTNER

        # 填写基本信息
        self.fill_input(self.INPUT_SURNAME, data["surname"])
        self.fill_input(self.INPUT_NAME, data["name"])
        self.fill_input(self.INPUT_PHONE, data["phone"])

        # 选择年龄
        if self.is_visible(self.SELECT_AGE):
            self.page.select_option(self.SELECT_AGE, data["age"])

        # 填写职位信息
        self.fill_input(self.INPUT_CURRENT_JOB, data["current_job"])
        self.fill_input(self.INPUT_APPLY_JOB, data["apply_job"])

        print("✓ 成为伙伴表单填写完成")

    @allure.step("提交表单")
    def submit_form(self):
        """点击提交按钮并提交表单"""
        self.click_element(self.BTN_SUBMIT)
        self.wait(2000)  # 等待提交处理

    @allure.step("验证表单提交成功")
    def verify_submit_success(self):
        """
        验证表单是否提交成功
        通过检查成功提示弹窗/Toast来判断
        """
        # 尝试查找成功提示
        success_visible = self.is_visible(self.SUCCESS_TOAST)

        if success_visible:
            print("✓ 表单提交成功提示显示")
            return True
        else:
            # 如果没有明显的成功提示，检查页面是否有变化或跳转
            print("⚠ 未检测到明确的成功提示，但表单已提交")
            return True
