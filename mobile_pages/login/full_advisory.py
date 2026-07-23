"""Page object and action for the Full Advisory flow."""

from appium.webdriver.common.appiumby import AppiumBy

from core.logger import logger
from mobile_pages.login.page import MobileLoginPage


class FullAdvisoryPage(MobileLoginPage):
    FULL_ADVISORY = (
        (
            AppiumBy.XPATH,
            '//android.view.View[@content-desc="Full Advisory"]',
        ),
    )

    def click_full_advisory(self) -> None:
        self._find(self.FULL_ADVISORY).click()
        logger.info("Clicked Full Advisory")


class FullAdvisoryActions:
    def __init__(self, page: FullAdvisoryPage):
        self.page = page

    def click_full_advisory(self) -> None:
        self.page.click_full_advisory()
