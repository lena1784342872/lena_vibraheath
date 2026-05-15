"""
大事件页面对象
封装大事件页面的所有操作
对应测试用例：17-22
"""
import allure
from pages.base_page import BasePage
from playwright.sync_api import Page


class EventsPage(BasePage):
    """大事件页面类"""

    # ==================== 元素定位器 ====================
    # 页面标题
    PAGE_TITLE = "section.banner-container h3:has-text('大事件')"
    BIG_EVENT_TITLE = "section.events-container h3:has-text('Big Event')"

    # Big Event 轮播区域
    BIG_EVENT_SECTION = "text=Big Event"
    EVENT_SLIDER_ITEM = ".event-slider .item, .big-event-item"
    EVENT_ARROW_RIGHT = "div.custom-swiper-next.custom-swiper-button"

    # 第一个事件内容
    FIRST_EVENT = "div.swiper-wrapper p:has-text('研究发现：每天30分钟“微运动”可显著降低死亡风险')"
    SECOND_EVENT = "div.swiper-wrapper p:has-text('科学饮水的智慧')"

    # 事件详情页
    EVENT_DETAIL_TITLE = "main.news-container h3.title"
    EVENT_DETAIL_DATE = "main.news-container p.date"
    EVENT_DETAIL_CONTENT = "main.news-container p.content"

    # 健康资讯区域
    HEALTH_INFO_SECTION = "section.info-container p.description"
    CATEGORY_ALL = "section.info-container li:has-text('全部')"
    CATEGORY_CARDIOVASCULAR = "section.info-container li:has-text('心血管')"
    CATEGORY_DINGXIANG = "section.info-container li:has-text('丁香公开课')"

    # 资讯文章
    ARTICLE_CARDIOVASCULAR_1 = "section.info-container  li:has-text('心血管')"

    ARTICLE_DINGXIANG = "div.info-list a.info-item[href='/news/39']"

    ARTICLE_DINGXIANG1=""



    def __init__(self, page: Page):
        """初始化大事件页面"""
        super().__init__(page)

    @allure.step("导航到大事件页面")
    def navigate_to_events(self):
        """打开大事件页面"""
        self.goto("/events")
        return self

    @allure.step("验证大事件页面加载成功")
    def verify_events_loaded(self):
        """验证页面是否正确加载"""
        #assert self.is_visible(self.PAGE_TITLE), "大事件页面标题未显示"
        assert self.get_text(self.PAGE_TITLE) == "大事件"
        #assert self.is_visible(self.BIG_EVENT_TITLE), "'Big Event'未显示"
        assert self.get_text(self.BIG_EVENT_TITLE) == "Big Event"
        print("✓ 大事件页面加载成功")
        return True

    @allure.step("滚动到Big Event区域")
    def scroll_to_big_event(self):
        """滚动到Big Event轮播区域"""
        self.scroll_to_element(self.BIG_EVENT_SECTION)

    @allure.step("验证第一个事件内容显示")
    def verify_first_event(self):
        """验证第一个事件是否显示"""
        assert self.is_visible(self.FIRST_EVENT), "第一个事件内容未显示"
        return True

    @allure.step("点击向右箭头切换事件")
    def click_next_event(self):
        """点击向右箭头切换到下一个事件"""
        self.click_element(self.EVENT_ARROW_RIGHT)
        self.wait(1500)  # 等待切换动画完成

    @allure.step("验证第二个事件内容显示")
    def verify_second_event(self):
        """验证第二个事件是否显示"""
        assert self.get_text(self.SECOND_EVENT) == "科学饮水的智慧"
        return True

    @allure.step("点击第一个事件查看详情")
    def click_first_event_detail(self):
        """点击第一个事件进入详情页"""
        self.click_element(self.FIRST_EVENT)

    @allure.step("验证事件详情页标题显示")
    def verify_event_detail_title(self):
        """验证详情页标题是否显示"""
        return self.get_text(self.EVENT_DETAIL_TITLE)

    @allure.step("验证事件详情页日期显示")
    def verify_event_detail_date(self):
        """验证详情页日期是否显示"""
        assert self.is_visible(self.EVENT_DETAIL_DATE), "详情页日期未显示"
        return True



    @allure.step("滚动到健康资讯区域")
    def scroll_to_health_info(self):
        """滚动到健康资讯区域"""
        self.scroll_to_element(self.HEALTH_INFO_SECTION)

    @allure.step("验证健康资讯分类显示")
    def verify_health_info_categories(self):
        """验证健康资讯的分类标签是否显示"""
        assert self.get_text(self.CATEGORY_ALL) == "全部"
        assert self.get_text(self.CATEGORY_CARDIOVASCULAR) == "心血管"
        assert self.get_text(self.CATEGORY_DINGXIANG) == "丁香公开课"

        print("✓ 健康资讯分类显示正常")
        return True

    @allure.step("点击'心血管'分类")
    def click_cardiovascular_category(self):
        """点击心血管分类筛选"""
        self.click_element(self.CATEGORY_CARDIOVASCULAR)
        self.wait(1000)

    @allure.step("验证心血管文章显示")
    def verify_cardiovascular_articles(self):
        """验证心血管分类的文章是否显示"""
        assert self.is_visible(self.ARTICLE_CARDIOVASCULAR_1), "心血管文章1未显示"
        return True

    @allure.step("点击'丁香公开课'分类")
    def click_dingxiang_category(self):
        """点击丁香公开课分类筛选"""
        self.click_element(self.CATEGORY_DINGXIANG)
        self.wait(1000)

    @allure.step("验证丁香公开课文章显示")
    def verify_dingxiang_articles(self):
        """验证丁香公开课分类的文章是否显示"""
        assert self.is_visible(self.ARTICLE_DINGXIANG), "丁香公开课文章未显示"
        return True

    @allure.step("点击第一篇健康资讯")
    def click_first_health_article(self):
        """点击第一篇健康资讯进入详情"""
        self.click_element(self.ARTICLE_DINGXIANG)

    @allure.step("验证资讯详情页标题显示")
    def verify_article_detail_title(self):
        """验证资讯详情页标题是否显示"""
        assert self.is_visible(self.EVENT_DETAIL_TITLE), "资讯标题未显示"
        return True

    @allure.step("验证资讯详情页日期显示")
    def verify_article_detail_date(self):
        """验证资讯详情页日期是否显示"""
        assert self.is_visible(self.EVENT_DETAIL_DATE), "资讯日期未显示"
        return True
