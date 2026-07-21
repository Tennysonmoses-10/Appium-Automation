"""Assertions and state checks for the mobile login screen."""

from core.logger import logger
from mobile_pages.login.locators import MobileLoginLocators
from mobile_pages.login.page import MobileLoginPage


class MobileLoginAssertions:
    """Provides boolean checks consumed by BDD step definitions."""

    def __init__(self, page: MobileLoginPage):
        self.page = page

    def verify_login_screen_loaded(self) -> bool:
        loaded = (
            self.page.is_visible(MobileLoginLocators.EMAIL_INPUT)
            and self.page.is_visible(MobileLoginLocators.PASSWORD_INPUT)
            and self.page.is_visible(MobileLoginLocators.LOGIN_BUTTON)
        )
        logger.info("Mobile login screen loaded: %s", loaded)
        return loaded

    def verify_dashboard_displayed(self) -> bool:
        return self.page.is_visible(MobileLoginLocators.DASHBOARD_TITLE)

    def verify_error_message(self, expected_text: str = "") -> bool:
        message = self.page.get_error_message()
        return bool(message) and expected_text.lower() in message.lower()
