"""
Pytest 全局配置文件
管理浏览器生命周期、截图、重试等通用功能
所有测试文件都会自动使用这里的配置
"""
import os
import time
import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
import allure
from config import config
import pytest
from db_utils import delete_test_data_by_phone


@pytest.fixture(scope="session")
def browser():
    """
    创建浏览器实例（整个测试会话只启动一次）

    scope="session" 的含义：
    - 在所有测试开始前启动浏览器
    - 所有测试共享同一个浏览器实例
    - 所有测试结束后关闭浏览器
    - 优点：速度快，不需要每次都启动浏览器
    """
    print("\n" + "=" * 60)
    print("正在启动浏览器...")
    print("=" * 60)

    with sync_playwright() as p:
        # 启动 Chromium 浏览器
        browser_instance = p.chromium.launch(
            headless=config.BROWSER_CONFIG["headless"],  # 是否显示浏览器窗口
            slow_mo=config.BROWSER_CONFIG["slow_mo"]  # 操作延迟（毫秒）
        )

        yield browser_instance  # 将浏览器实例传递给测试

        print("\n" + "=" * 60)
        print("正在关闭浏览器...")
        print("=" * 60)
        browser_instance.close()  # 所有测试结束后关闭


@pytest.fixture(scope="function")
def context(browser: Browser):
    """
    创建浏览器上下文（每个测试用例独立）

    比喻说明：
    就像浏览器的"无痕模式"，每个测试用例都有独立的Cookie和缓存
    测试之间互不影响，保证测试的独立性

    scope="function" 的含义：
    - 每个测试函数执行前创建新的上下文
    - 测试结束后自动清理
    """
    context = browser.new_context(
        viewport={
            'width': config.BROWSER_CONFIG["viewport_width"],
            'height': config.BROWSER_CONFIG["viewport_height"]
        },
        ignore_https_errors=True  # 忽略HTTPS证书错误（测试环境常用）
    )

    yield context
    context.close()  # 测试结束后关闭上下文


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """
    创建页面对象（测试中最常用的对象）

    这是 Playwright 的核心对象，用于：
    - 打开网页
    - 点击元素
    - 输入文本
    - 获取页面内容
    """
    page = context.new_page()

    # 启用追踪功能（失败时可以查看完整执行过程）
    page.context.tracing.start(
        screenshots=True,  # 保存截图
        snapshots=True  # 保存页面快照
    )

    yield page

    # 测试结束后停止追踪并关闭页面
    page.context.tracing.stop()
    page.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest 钩子函数：测试失败时自动截图

    工作原理：
    1. 监听每个测试用例的执行结果
    2. 如果测试失败（failed），自动截取当前页面
    3. 将截图附加到 Allure 报告中
    """
    outcome = yield  # 执行测试用例
    report = outcome.get_result()  # 获取测试结果

    # 只在测试执行阶段（call）且失败时截图
    if report.when == "call" and report.failed:
        # 获取当前测试的 page 对象
        if "page" in item.funcargs:
            page = item.funcargs["page"]

            try:
                # 生成截图文件名（使用时间戳避免重复）
                timestamp = int(time.time())
                screenshot_name = f"failure_{timestamp}.png"
                screenshot_path = os.path.join(config.SCREENSHOTS_DIR, screenshot_name)

                # 确保截图目录存在
                os.makedirs(config.SCREENSHOTS_DIR, exist_ok=True)

                # 截取全屏
                page.screenshot(path=screenshot_path, full_page=True)
                print(f"\n⚠ 测试失败，截图已保存: {screenshot_path}")

                # 将截图附加到 Allure 报告
                allure.attach.file(
                    screenshot_path,
                    name="失败截图",
                    attachment_type=allure.attachment_type.PNG
                )

            except Exception as e:
                print(f"截图失败: {e}")


# 可选：添加重试机制（网络不稳定时有用）
def pytest_collection_modifyitems(items):
    """
    修改测试用例收集逻辑
    可以给特定用例添加重试标记
    """
    for item in items:
        # 如果需要给P0优先级用例添加重试，可以这样写：
        # if "p0" in item.keywords:
        #     item.add_marker(pytest.mark.flaky(reruns=2))
        pass



TEST_PHONE = "16566666666"

@pytest.fixture( scope="function")
def auto_cleanup():
    # 前置清理：删除可能残留的同号数据
    delete_test_data_by_phone(TEST_PHONE)
    yield
    # 后置清理：删除本次创建的数据
    delete_test_data_by_phone(TEST_PHONE)