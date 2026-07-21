"""Low-level Appium interactions for the mobile login screen."""

import time
from typing import Iterable, Optional, Tuple

from selenium.common.exceptions import NoSuchElementException

from config.settings import settings
from core.logger import logger
from mobile_pages.login.locators import MobileLoginLocators

Locator = Tuple[str, str]


class MobileLoginPage:
    """Encapsulates native mobile login-screen interactions."""

    def __init__(self, driver):
        self.driver = driver

    def _find(self, locators: Iterable[Locator]):
        """Return the first matching element from the supported locator set."""
        candidate_locators = tuple(locators)
        deadline = time.monotonic() + settings.appium.explicit_wait

        while time.monotonic() <= deadline:
            for by, value in candidate_locators:
                elements = self.driver.find_elements(by, value)
                if elements:
                    return elements[0]
            time.sleep(0.5)

        raise NoSuchElementException(f"No element matched locators: {candidate_locators}")

    def is_visible(self, locators: Iterable[Locator]) -> bool:
        """Return whether any candidate locator is currently visible."""
        try:
            return self._find(locators).is_displayed()
        except NoSuchElementException:
            return False

    def enter_english(self) -> None:
        self._find(MobileLoginLocators.LANGUAGE_SELECTION).click()
        logger.info("Clicked English language selection")


    def proceed_button(self) -> None:
        self._find(MobileLoginLocators.PROCEED_BUTTON).click()
        logger.info("Clicked proceed button")


    def enter_email(self, email: str) -> None:
        field = self._find(MobileLoginLocators.EMAIL_INPUT)
        field.clear()
        field.send_keys(email)
        logger.info("Entered mobile login email")

    def enter_password(self, password: str) -> None:
        field = self._find(MobileLoginLocators.PASSWORD_INPUT)
        field.clear()
        field.send_keys(password)
        logger.info("Entered mobile login password")

    def click_login(self) -> None:
        self._find(MobileLoginLocators.LOGIN_BUTTON).click()
        logger.info("Tapped mobile login button")

    def click_forgot_password(self) -> None:
        self._find(MobileLoginLocators.FORGOT_PASSWORD_LINK).click()

    def click_sign_up(self) -> None:
        self._find(MobileLoginLocators.SIGN_UP_LINK).click()

    def get_error_message(self) -> Optional[str]:
        try:
            return self._find(MobileLoginLocators.ERROR_MESSAGE).text
        except NoSuchElementException:
            return None
