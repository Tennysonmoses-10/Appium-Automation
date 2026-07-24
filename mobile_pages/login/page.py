"""Low-level Appium interactions for the mobile login screen."""

import time
from typing import Iterable, Optional, Tuple

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    WebDriverException,
)
from selenium.webdriver.common.keys import Keys

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

    def _dismiss_keyboard(self) -> None:
        """Hide the soft keyboard when it is present."""
        try:
            self.driver.hide_keyboard()
            logger.info("Dismissed mobile keyboard")
        except WebDriverException:
            logger.info("Mobile keyboard was not open or could not be dismissed")

    def _set_field_text(self, field, value: str) -> None:
        """Set text on a mobile input, with Flutter-friendly fallbacks."""
        field.click()

        try:
            field.clear()
        except WebDriverException:
            logger.info("Could not clear field before entering text")

        try:
            field.send_keys(value)
            return
        except WebDriverException:
            logger.info("send_keys failed, trying set_value")

        try:
            field.set_value(value)
            return
        except (WebDriverException, AttributeError):
            logger.info("set_value failed, trying mobile: replaceElementValue")

        self.driver.execute_script(
            "mobile: replaceElementValue",
            {"elementId": field.id, "value": value},
        )

    def enter_english(self) -> None:
        self._find(MobileLoginLocators.LANGUAGE_SELECTION).click()
        logger.info("Clicked English language selection")

    def enter_hindi(self) -> None:
        self._find(MobileLoginLocators.HINDI).click()
        logger.info("Clicked HINDI language selection")

    def enter_marathi(self) -> None:
        self._find(MobileLoginLocators.MARATHI).click()
        logger.info("Clicked MARATHI language selection")

    def proceed_button(self) -> None:
        self._find(MobileLoginLocators.PROCEED_BUTTON).click()
        logger.info("Clicked proceed button")

    def get_started(self) -> None:
        self._find(MobileLoginLocators.GET_STARTED).click()
        logger.info("Clicked Get Started button")

    def enter_mobilenumbers(self, mobile_number: str) -> None:
        field = self._find(MobileLoginLocators.ENTER_MOBILENUMBER)
        field.click()
        field.send_keys(mobile_number)
        self._dismiss_keyboard()
        logger.info(f"Entered mobile number: {mobile_number}")

    def Proceed_Login(self) -> None:
        self._find(MobileLoginLocators.PROCEED_LOGIN).click()
        logger.info("Clicked Proceed Login button")

    def enter_otp(self, otp: str) -> None:
        otp_digits = otp.strip()

        # OTP input may be a specialized component; sometimes typing the full string doesn't populate it.
        # We'll verify the field value after entry and fall back to per-digit typing if needed.
        field = None
        for by, value in MobileLoginLocators.ENTER_OTP:
            candidates = [f for f in self.driver.find_elements(by, value) if f.is_displayed()]
            if candidates:
                field = candidates[0]
                break

        if field is None:
            raise NoSuchElementException(f"No OTP input matched locators: {MobileLoginLocators.ENTER_OTP}")

        try:
            field.click()
        except StaleElementReferenceException:
            logger.info("OTP field refreshed before click; locating it again")
            field = self._find(MobileLoginLocators.ENTER_OTP)
            field.click()

        # Clear attempts
        try:
            field.clear()
        except WebDriverException:
            logger.info("Could not clear OTP field with clear()")

        # Backspace fallback (some inputs ignore clear()).
        try:
            current = (field.get_attribute("text") or field.get_attribute("value") or "").strip()
            for _ in range(len(current)):
                field.send_keys(Keys.BACKSPACE)
        except Exception:
            pass

        # Primary attempt: full OTP
        self._set_field_text(field, otp_digits)
        value_after = (field.get_attribute("text") or field.get_attribute("value") or "").strip()

        # Give the OTP input a moment to render/populate.
        for _ in range(10):
            if value_after == otp_digits:
                break
            time.sleep(0.2)
            value_after = (field.get_attribute("text") or field.get_attribute("value") or "").strip()

        # Fallback: type per digit if value didn't populate.
        if value_after != otp_digits:
            logger.info(
                f"OTP mismatch after typing. expected={otp_digits} actual={value_after!r}; typing per digit"
            )
            field.click()
            for d in otp_digits:
                field.send_keys(d)
                time.sleep(0.1)
            value_after = (field.get_attribute("text") or field.get_attribute("value") or "").strip()
            for _ in range(10):
                if value_after == otp_digits:
                    break
                time.sleep(0.2)
                value_after = (field.get_attribute("text") or field.get_attribute("value") or "").strip()

        logger.info(f"Entered OTP: expected={otp_digits} actual={value_after!r}")
        if value_after != otp_digits:
            raise AssertionError(f"OTP field did not populate. expected={otp_digits} actual={value_after!r}")

        self._dismiss_keyboard()

    def confirm_otp(self) -> None:
        self._find(MobileLoginLocators.CONFIRM_BUTTON).click()
        logger.info("Clicked Confirm button")

    def click_advisory(self) -> None:
        self._find(MobileLoginLocators.ADVISORY_BUTTON).click()
        logger.info("Clicked Advisory button")

    def click_ask_expert(self) -> None:
        self._find(MobileLoginLocators.ASK_EXPERT_BUTTON).click()
        logger.info("Clicked Ask Expert button")

    def get_error_message(self) -> Optional[str]:
        try:
            return self._find(MobileLoginLocators.ERROR_MESSAGE).text
        except NoSuchElementException:
            return None
