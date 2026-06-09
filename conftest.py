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

# ---------- 数据库清理功能（可选，依赖安装失败时降级）----------
try:
    from db_utils import delete_test_data_by_phone
    DB_UTILS_AVAILABLE = True
except (ImportError, ModuleNotFoundError) as e:
    print(f"⚠️ 警告: 无法导入 db_utils，数据库清理功能将被禁用。原因: {e}")
    DB_UTILS_AVAILABLE = False
    # 定义一个 dummy 函数，避免后续 NameError
    def delete_test_data_by_phone(*args, **kwargs):
        print("⚠️ 数据库清理不可用，跳过操作")
        return 0

# ---------- 浏览器 fixtures ----------
@pytest.fixture(scope="session")
def browser():
    """
    创建浏览器实例（整个测试会话只启动一次）
    """
    print("\n" + "=" * 60)
    print("正在启动浏览器...")
    print("=" * 60)

    with sync_playwright() as p:
        browser_instance = p.chromium.launch(
            headless=config.BROWSER_CONFIG["headless"],
            slow_mo=config.BROWSER_CONFIG["slow_mo"]
        )
        yield browser_instance
        print("\n" + "=" * 60)
        print("正在关闭浏览器...")
        print("=" * 60)
        browser_instance.close()


@pytest.fixture(scope="function")
def context(browser: Browser):
    """
    创建浏览器上下文（每个测试用例独立）
    """
    context = browser.new_context(
        viewport={
            'width': config.BROWSER_CONFIG["viewport_width"],
            'height': config.BROWSER_CONFIG["viewport_height"]
        },
        ignore_https_errors=True
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """
    创建页面对象（测试中最常用的对象）
    """
    page = context.new_page()
    page.context.tracing.start(screenshots=True, snapshots=True)
    yield page
    page.context.tracing.stop()
    page.close()


# ---------- 失败自动截图 ----------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            try:
                timestamp = int(time.time())
                screenshot_name = f"failure_{timestamp}.png"
                screenshot_path = os.path.join(config.SCREENSHOTS_DIR, screenshot_name)
                os.makedirs(config.SCREENSHOTS_DIR, exist_ok=True)
                page.screenshot(path=screenshot_path, full_page=True)
                print(f"\n⚠ 测试失败，截图已保存: {screenshot_path}")
                allure.attach.file(
                    screenshot_path,
                    name="失败截图",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"截图失败: {e}")


# ---------- 测试数据清理 fixture ----------
TEST_PHONE = "16566666666"

@pytest.fixture(scope="function")
def auto_cleanup():
    """
    自动清理测试数据的 fixture
    如果数据库工具不可用，则跳过清理（打印警告）
    """
    # 前置清理
    if DB_UTILS_AVAILABLE:
        delete_test_data_by_phone(TEST_PHONE)
    else:
        print("⚠️ auto_cleanup: 数据库不可用，跳过前置清理")

    yield

    # 后置清理
    if DB_UTILS_AVAILABLE:
        delete_test_data_by_phone(TEST_PHONE)
    else:
        print("⚠️ auto_cleanup: 数据库不可用，跳过后置清理")