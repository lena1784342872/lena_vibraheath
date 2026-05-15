"""
关于我们测试用例
对应CSV测试用例：26-32
"""
import pytest
import allure
from pages.about_page import AboutPage


@allure.feature("关于我们模块")
class TestAboutPage:
    """关于我们测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """
        每个测试用例执行前的准备工作
        autouse=True 表示自动执行，无需手动调用
        """
        self.about_page = AboutPage(page)

    @allure.story("页面访问")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC026-关于我们页面响应正常")
    def test_tc026_access_about(self):
        """
        用例编号: 26
        验证关于我们页面可以正常访问
        """
        with allure.step("步骤1: 打开关于我们页面"):
            self.about_page.navigate_to_about()

        with allure.step("验证: 页面加载成功"):
            assert self.about_page.verify_about_loaded()

    @allure.story("产品介绍")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC027-产品介绍展示")
    def test_tc027_product_introduction(self):
        """
        用例编号: 27
        验证产品介绍区域展示正常
        """
        with allure.step("步骤1: 打开关于我们页面"):
            self.about_page.navigate_to_about()

        with allure.step("步骤2: 滚动到产品介绍区域"):
            self.about_page.scroll_to_product_section()

        with allure.step("验证: 产品介绍内容显示"):
            assert self.about_page.verify_product_introduction()

    @allure.story("联系我们表单")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC028-联系我们表单展示")
    def test_tc028_contact_form_display(self):
        """
        用例编号: 28
        验证联系我们表单展示正常
        """
        with allure.step("步骤1: 打开关于我们页面"):
            self.about_page.navigate_to_about()

        with allure.step("步骤2: 滚动到联系我们区域"):
            self.about_page.scroll_to_contact_us()

        with allure.step("步骤3: 点击'我想改善健康'"):
            self.about_page.click_improve_health_button()

        with allure.step("验证: 改善健康表单显示"):
            assert self.about_page.verify_improve_health_form()

    @allure.story("联系我们表单")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC029-表单类型切换")
    def test_tc029_form_type_switch(self):
        """
        用例编号: 29
        验证可以在'我想改善健康'和'我想成为伙伴'之间切换
        """
        with allure.step("步骤1: 打开关于我们页面"):
            self.about_page.navigate_to_about()

        with allure.step("步骤2: 滚动到联系我们区域"):
            self.about_page.scroll_to_contact_us()

        with allure.step("步骤3: 点击'我想成为伙伴'"):
            self.about_page.click_become_partner_button()

        with allure.step("验证: 成为伙伴表单显示"):
            assert self.about_page.verify_partner_form()

    @allure.story("表单提交")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC030-改善健康表单提交")
    def test_tc030_submit_improve_health_form(self):
        """
        用例编号: 30
        验证改善健康表单可以正常提交
        """
        with allure.step("步骤1: 打开关于我们页面"):
            self.about_page.navigate_to_about()

        with allure.step("步骤2: 滚动到联系我们区域"):
            self.about_page.scroll_to_contact_us()

        with allure.step("步骤3: 填写改善健康表单"):
            self.about_page.fill_improve_health_form()

        with allure.step("步骤4: 提交表单"):
            self.about_page.submit_form()

        with allure.step("验证: 表单提交成功"):
            assert self.about_page.verify_submit_success()

    @allure.story("表单提交")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC031-成为伙伴表单提交")
    def test_tc031_submit_partner_form(self):
        """
        用例编号: 31
        验证成为伙伴表单可以正常提交
        """
        with allure.step("步骤1: 打开关于我们页面"):
            self.about_page.navigate_to_about()

        with allure.step("步骤2: 滚动到联系我们区域"):
            self.about_page.scroll_to_contact_us()

        with allure.step("步骤3: 切换到成为伙伴表单并填写"):
            self.about_page.click_become_partner_button()
            self.about_page.fill_partner_form()

        with allure.step("步骤4: 提交表单"):
            self.about_page.submit_form()

        with allure.step("验证: 表单提交成功"):
            assert self.about_page.verify_submit_success()

    @allure.story("数据清理")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC032-验证后删除测试数据")
    def test_tc032_cleanup_test_data(self):
        """
        用例编号: 32
        说明：纯UI自动化无法直连数据库，此用例仅做提示
        实际项目中需要配合后端接口或手动清理数据
        """
        with allure.step("说明: 此用例需要数据库访问权限"):
            print("⚠ 提示：请在数据库中手动删除测试数据")
            print("  姓氏: chen, 名字: lena, 手机: 16566666666")
            assert True, "数据清理提示（需手动处理或调用API）"
