"""Page object and action for the Short Advisory flow."""

from appium.webdriver.common.appiumby import AppiumBy

from core.logger import logger
from mobile_pages.login.page import MobileLoginPage


class ShortAdvisoryPage(MobileLoginPage):
    SHORT_ADVISORY = (
        (
            AppiumBy.XPATH,
            '//android.view.View[@content-desc="Short Advisory"]',
        ),
    )

    def click_short_advisory(self) -> None:
        self._find(self.SHORT_ADVISORY).click()
        logger.info("Clicked Short Advisory")


class ShortAdvisoryActions:
    def __init__(self, page: ShortAdvisoryPage):
        self.page = page

    def click_short_advisory(self) -> None:
        self.page.click_short_advisory()
