"""
基础页面对象类
封装所有页面通用的操作方法（点击、输入、等待、截图等）
所有具体页面都继承这个类
"""
import os
import time
import allure
from playwright.sync_api import Page, expect
from config import config


class BasePage:
    """
    基础页面类 - 所有页面的父类

    包含的通用功能：
    1. 打开网页
    2. 点击元素
    3. 输入文本
    4. 获取文本内容
    5. 等待元素出现
    6. 滚动到元素位置
    7. 失败时自动截图
    """

    def __init__(self, page: Page):
        """
        初始化方法

        参数:
            page: Playwright 的页面对象，用于操作浏览器
        """
        self.page = page
        self.timeout = config.TIMEOUTS["element_wait"]

    @allure.step("打开页面: {url_path}")
    def goto(self, url_path: str):
        """
        打开指定URL的页面

        参数:
            url_path: URL路径（不包含域名），如 "/" 或 "/services"
        """
        full_url = config.BASE_URL + url_path
        print(f"正在打开: {full_url}")

        # 优化点 1：wait_until="domcontentloaded"
        # 只要 HTML 下载并解析完就继续，不需要等图片/样式表加载，速度极快
        # 优化点 2：timeout=60000
        # 将超时时间延长到 60 秒，适应不稳定的测试环境
        response = self.page.goto(
            full_url,
            timeout=60000,
            wait_until="domcontentloaded"
        )

        # 校验响应状态码是否为 200
        if response:
            assert response.status == 200, f"页面加载失败，状态码: {response.status}"
            print(f"✓ 页面加载成功，状态码: {response.status}")
        else:
            print("✓ 页面已跳转（无响应对象）")

    @allure.step("点击元素: {locator_str}")
    def click_element(self, locator_str: str):
        """
        点击页面上的元素

        参数:
            locator_str: 元素定位器字符串，如 "button:has-text('提交')"

        为什么使用显式等待：
        页面元素可能还没加载完成就点击会报错，所以先等待元素可见再点击
        """
        try:
            # 创建定位器对象
            locator = self.page.locator(locator_str)

            # 等待元素可见（最多等待配置的超时时间）
            locator.wait_for(state="visible", timeout=self.timeout)

            # 执行点击
            locator.click()
            print(f"✓ 已点击元素: {locator_str}")

        except Exception as e:
            # 如果点击失败，截图并抛出异常
            self.take_screenshot(f"click_error_{int(time.time())}")
            raise Exception(f"点击元素失败: {locator_str}\n错误信息: {str(e)}")

    @allure.step("在元素中输入文本: {text}")
    def fill_input(self, locator_str: str, text: str):
        """
        在输入框中输入文本

        参数:
            locator_str: 输入框的定位器
            text: 要输入的文本内容

        使用示例:
            self.fill_input("input[name='username']", "张三")
        """
        try:
            locator = self.page.locator(locator_str)
            locator.wait_for(state="visible", timeout=self.timeout)

            # 先清空输入框，再填入新内容
            locator.clear()
            locator.fill(text)
            print(f"✓ 已输入文本: {text}")

        except Exception as e:
            self.take_screenshot(f"fill_error_{int(time.time())}")
            raise Exception(f"输入文本失败: {str(e)}")

    @allure.step("获取元素文本内容: {locator_str}")
    def get_text(self, locator_str: str) -> str:
        """
        获取页面上元素的文本内容

        参数:
            locator_str: 元素定位器

        返回:
            元素的文本内容字符串
        """
        try:
            locator = self.page.locator(locator_str)
            locator.wait_for(state="visible", timeout=self.timeout)
            text = locator.text_content()
            print(f"✓ 获取到文本: {text[:50]}...")  # 只打印前50个字符
            return text

        except Exception as e:
            raise Exception(f"获取文本失败: {str(e)}")

    @allure.step("验证元素是否可见: {locator_str}")
    def is_visible(self, locator_str: str) -> bool:
        """
        检查元素是否在页面上可见

        参数:
            locator_str: 元素定位器

        返回:
            True=元素可见，False=元素不可见
        """
        try:
            locator = self.page.locator(locator_str)
            # 等待元素可见，如果超时则返回 False
            locator.wait_for(state="visible", timeout=self.timeout)
            return True
        except:
            return False

    @allure.step("断言元素包含文本: {expected_text}")
    def assert_text_contains(self, locator_str: str, expected_text: str):
        """
        断言元素的文本内容包含指定的文字

        参数:
            locator_str: 元素定位器
            expected_text: 期望包含的文本

        为什么用断言：
        断言失败会自动抛出异常，pytest 会捕获并标记为测试失败
        """
        actual_text = self.get_text(locator_str)
        assert expected_text in actual_text, \
            f"文本不匹配！\n期望包含: {expected_text}\n实际内容: {actual_text}"
        print(f"✓ 断言通过: 元素包含文本 '{expected_text}'")

    @allure.step("滚动到元素位置: {locator_str}")
    def scroll_to_element(self, locator_str: str):
        """
        滚动页面，使指定元素出现在可视区域

        参数:
            locator_str: 目标元素的定位器

        使用场景：
        当元素在页面下方，需要滚动才能看到时使用
        """
        try:
            locator = self.page.locator(locator_str)
            locator.wait_for(state="visible", timeout=self.timeout)

            # 滚动到元素位置
            locator.scroll_into_view_if_needed()
            print(f"✓ 已滚动到元素位置")

            # 稍微等待一下，确保滚动完成
            self.page.wait_for_timeout(500)

        except Exception as e:
            raise Exception(f"滚动失败: {str(e)}")

    @allure.step("等待指定时间: {milliseconds}毫秒")
    def wait(self, milliseconds: int = 1000):
        """
        强制等待指定的毫秒数

        参数:
            milliseconds: 等待的毫秒数（1000毫秒=1秒）

        使用建议：
        尽量少用强制等待，优先使用显式等待（wait_for）
        但在某些动态加载场景下，强制等待更稳定
        """
        self.page.wait_for_timeout(milliseconds)

    @allure.step("截取屏幕快照: {filename}")
    def take_screenshot(self, filename: str):
        """
        截取当前页面并保存为图片

        参数:
            filename: 截图文件名（不含扩展名）

        使用场景：
        1. 测试失败时自动截图
        2. 关键步骤手动截图留证
        """
        # 确保截图目录存在
        os.makedirs(config.SCREENSHOTS_DIR, exist_ok=True)

        # 生成完整的文件路径
        filepath = os.path.join(config.SCREENSHOTS_DIR, f"{filename}.png")

        # 执行截图
        self.page.screenshot(path=filepath, full_page=True)
        print(f"✓ 截图已保存: {filepath}")

        # 将截图附加到 Allure 报告
        allure.attach.file(
            filepath,
            name=f"截图: {filename}",
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("校验页面响应状态为200")
    def check_page_status(self):
        """
        校验当前页面的 HTTP 响应状态码是否为 200

        实现原理：
        通过 Playwright 的响应拦截功能，检查最后一次页面加载的状态码
        """
        # 获取当前页面的 URL
        current_url = self.page.url

        # 重新加载页面并捕获响应
        with self.page.expect_response(current_url) as response_info:
            self.page.reload()
            response = response_info.value

        # 断言状态码为 200
        assert response.status == 200, f"页面状态码异常: {response.status}"
        print(f"✓ 页面响应状态正常: {response.status}")

    @allure.step("选择下拉框选项: {option_text}")
    def select_option(self, locator_str: str, option_text: str):
        """
        从下拉框中选择指定选项

        参数:
            locator_str: 下拉框的定位器，如 "#age"
            option_text: 要选择的选项文本，如 "20-30 岁"

        使用示例:
            self.select_option("#age", "20-30 岁")
        """
        try:
            locator = self.page.locator(locator_str)

            # 等待元素可见，增加更详细的日志
            print(f"正在等待下拉框元素可见: {locator_str}")
            locator.wait_for(state="visible", timeout=self.timeout)
            print(f"✓ 下拉框元素已可见")

            # 使用 Playwright 的 select_option 方法，根据选项文本进行选择
            print(f"正在选择选项: {option_text}")
            locator.select_option(label=option_text)
            print(f"✓ 已选择下拉框选项: {option_text}")

        except Exception as e:
            self.take_screenshot(f"select_error_{int(time.time())}")
            print(f" 选择下拉框失败，已截图")
            print(f"定位器: {locator_str}")
            print(f"选项文本: {option_text}")
            print(f"错误信息: {str(e)}")
            raise Exception(f"选择下拉框选项失败: {str(e)}")

    @allure.step("点击选择下拉框选项: {option_text}")
    def click_select_option(self, dropdown_locator: str, option_text: str):
        """
        处理自定义下拉框（非标准select元素）
        先点击下拉框展开选项，再点击指定选项

        参数:
            dropdown_locator: 下拉框触发器的定位器
            option_text: 要选择的选项文本

        使用示例:
            self.click_select_option(".age-dropdown", "20-30 岁")
        """
        try:
            # 第一步：点击下拉框，展开选项列表
            dropdown = self.page.locator(dropdown_locator)
            print(f"正在点击下拉框: {dropdown_locator}")
            dropdown.wait_for(state="visible", timeout=self.timeout)
            dropdown.click()
            self.wait(500)  # 等待选项列表展开

            # 第二步：点击目标选项
            # 使用文本定位器查找选项
            option_locator = f"text={option_text}"
            print(f"正在点击选项: {option_text}")

            option = self.page.locator(option_locator)
            option.wait_for(state="visible", timeout=self.timeout)
            option.click()

            print(f"✓ 已选择下拉框选项: {option_text}")

        except Exception as e:
            self.take_screenshot(f"click_select_error_{int(time.time())}")
            print(f"✗ 点击选择下拉框失败，已截图")
            print(f"错误信息: {str(e)}")
            raise Exception(f"点击选择下拉框选项失败: {str(e)}")
