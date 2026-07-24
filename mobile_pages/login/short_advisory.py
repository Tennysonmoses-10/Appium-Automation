"""Page object and action for the Short Advisory flow."""

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time

from core.logger import logger
from mobile_pages.login.page import MobileLoginPage


class ShortAdvisoryPage(MobileLoginPage):
    FARMBLOCK = (
        (
            AppiumBy.XPATH,
            '//android.widget.Button[contains(@content-desc, "Farmblock") and contains(@content-desc, "Select Farm")]',
        ),
    )
    PROCEED_AFTER_FARMBLOCK = (
        (
            AppiumBy.XPATH,
            '//android.widget.Button[@content-desc="Proceed"] | //android.view.View[@content-desc="Proceed"]',
        ),
    )
    CROP_DROPDOWN = (
        (
            AppiumBy.XPATH,
            '//android.view.View[contains(@content-desc, "Crop") and not(contains(@content-desc, "Variety"))]',
        ),
    )
    CROP_VARIETY_DROPDOWN = (
        (
            AppiumBy.XPATH,
            '//android.widget.Button[@content-desc="Crop Variety\nSelect Crop Variety"]',
        ),
    )
    TEXT_TOGGLE = ((AppiumBy.XPATH, '//android.widget.CheckBox[@content-desc="Text"]'),)
    OBSERVATIONS = ((AppiumBy.XPATH, '//android.widget.EditText'),)
    ADD_IMAGE = ((AppiumBy.XPATH, '//android.view.View[@content-desc="Add"]'),)
    SAVE_AS_DRAFT = ((AppiumBy.XPATH, '//android.view.View[@content-desc="Save As Draft"]'),)
    CAMERA_OPTION = (
        (AppiumBy.ACCESSIBILITY_ID, "Camera"),
        (AppiumBy.XPATH, '//*[contains(@content-desc, "Camera") or @text="Camera"]'),
    )
    CAMERA_SHUTTER = (
        (AppiumBy.ACCESSIBILITY_ID, "Shutter"),
        (AppiumBy.ACCESSIBILITY_ID, "Take photo"),
        (AppiumBy.ACCESSIBILITY_ID, "Capture"),
        (AppiumBy.XPATH, '//android.widget.ImageButton[@content-desc="Shutter"]'),
        (AppiumBy.XPATH, '//android.widget.ImageButton[@content-desc="Take photo"]'),
    )
    USE_PHOTO = (
        (AppiumBy.ACCESSIBILITY_ID, "Use photo"),
        (AppiumBy.ACCESSIBILITY_ID, "Done"),
        (AppiumBy.XPATH, '//*[contains(@content-desc, "Use photo") or @text="Use photo"]'),
    )

    def __init__(self, driver):
        super().__init__(driver)
        self.camera_permission_decision = "allow"

    SHORT_ADVISORY = (
        (
            AppiumBy.XPATH,
            '//android.view.View[@content-desc="Short Advisory"]',
        ),
    )

    def click_short_advisory(self) -> None:
        self._find(self.SHORT_ADVISORY).click()
        logger.info("Clicked Short Advisory")

    def click_farmblock(self) -> None:
        self._find(self.FARMBLOCK).click()
        logger.info("Opened farmblock dropdown")

    def select_farmblock(self, farmblock: str) -> None:
        # Farm blocks are exposed as buttons whose content-desc is the block name.
        locator = ((AppiumBy.XPATH, f'//android.widget.Button[@content-desc="{farmblock}"]'),)
        self._find(locator).click()
        logger.info("Selected farmblock: %s", farmblock)

    def click_proceed_after_farmblock(self) -> None:
        self._find(self.PROCEED_AFTER_FARMBLOCK).click()
        logger.info("Clicked Proceed after farmblock selection")

    def click_crop_dropdown(self) -> None:
        self._find(self.CROP_DROPDOWN).click()
        logger.info("Opened crop dropdown")

    def select_crop(self, crop: str) -> None:
        locator = ((AppiumBy.XPATH, f'//android.widget.Button[@content-desc="{crop}"]'),)
        self._find(locator).click()
        logger.info("Selected crop: %s", crop)

    def click_crop_variety_dropdown(self) -> None:
        self._find(self.CROP_VARIETY_DROPDOWN).click()
        logger.info("Opened crop variety dropdown")

    def select_crop_variety(self, crop_variety: str) -> None:
        locator = ((AppiumBy.XPATH, f'//android.widget.Button[@content-desc="{crop_variety}"]'),)
        self._find(locator).click()
        logger.info("Selected crop variety: %s", crop_variety)

    def click_text_toggle(self) -> None:
        self._find(self.TEXT_TOGGLE).click()
        logger.info("Enabled text observations")

    def enter_observations(self, observations: str) -> None:
        field = self._find(self.OBSERVATIONS)
        self._set_field_text(field, observations)
        self._dismiss_keyboard()
        logger.info("Entered observations")

    def set_camera_permission(self, decision: str) -> None:
        normalized = decision.strip().lower()
        if normalized not in {"allow", "deny"}:
            raise ValueError("Camera permission must be either 'allow' or 'deny'")
        self.camera_permission_decision = normalized
        self._handle_camera_permission()

    def _handle_camera_permission(self) -> None:
        labels = (
            ("While using the app", "Allow"),
            ("Only this time", "Allow"),
            ("Allow", "Allow"),
            ("Don\'t allow", "Deny"),
            ("Deny", "Deny"),
        )
        for label, action in labels:
            if (self.camera_permission_decision == "allow") != (action == "Allow"):
                continue
            try:
                elements = self.driver.find_elements(AppiumBy.ACCESSIBILITY_ID, label)
                visible = [element for element in elements if element.is_displayed()]
                if visible:
                    visible[0].click()
                    logger.info("Camera permission decision: %s", self.camera_permission_decision)
                    return
            except (NoSuchElementException, WebDriverException):
                continue
        logger.info(
            "Camera permission prompt was not displayed; camera is assumed to be ready; decision=%s",
            self.camera_permission_decision,
        )

    def _click_if_present(self, locators) -> bool:
        """Click a visible control without failing when the app skips it."""
        for by, value in locators:
            try:
                elements = self.driver.find_elements(by, value)
                visible = [element for element in elements if element.is_displayed()]
                if visible:
                    visible[0].click()
                    return True
            except (NoSuchElementException, WebDriverException):
                continue
        return False

    def _click_camera_shutter(self) -> None:
        """Click the camera shutter, including unlabeled emulator controls."""
        if self._click_if_present(self.CAMERA_SHUTTER):
            return

        # The emulator camera exposes the shutter as an unlabeled ImageButton.
        # Choose the lowest visible button so flash/rear-camera controls at the
        # top of the camera screen are not clicked.
        try:
            width, height = (
                self.driver.get_window_size()["width"],
                self.driver.get_window_size()["height"],
            )
            candidates = []
            for class_name in ("android.widget.ImageButton", "android.widget.Button"):
                elements = self.driver.find_elements(AppiumBy.CLASS_NAME, class_name)
                for element in elements:
                    if element.is_displayed():
                        rect = element.rect
                        if rect["y"] > height * 0.70:
                            candidates.append((rect["y"] + rect["height"], element))
            if candidates:
                candidates.sort(key=lambda item: item[0], reverse=True)
                candidates[0][1].click()
                return

            # Last fallback for camera implementations that expose no shutter
            # element at all: tap the standard bottom-center shutter position.
            self.driver.execute_script(
                "mobile: clickGesture",
                {"x": width // 2, "y": int(height * 0.93)},
            )
        except WebDriverException as exc:
            raise NoSuchElementException("Camera shutter could not be located or clicked") from exc

    def add_images(self, count: int = 6) -> None:
        for index in range(1, count + 1):
            self._find(self.ADD_IMAGE).click()
            logger.info("Clicked Add for image %d/%d", index, count)
            self._handle_camera_permission()
            if self._click_if_present(self.CAMERA_OPTION):
                logger.info("Selected Camera for image %d/%d", index, count)
            else:
                logger.info("Camera was already open for image %d/%d", index, count)

            self._click_camera_shutter()
            logger.info(f"Captured image {index}/{count}")
            self._click_if_present(self.USE_PHOTO)
            self._dismiss_keyboard()

    def save_as_draft(self) -> None:
        self._find(self.SAVE_AS_DRAFT).click()
        logger.info("Saved advisory as draft")

    def allow_location_permission(self) -> None:
        """Allow the Android location prompt when it is displayed.

        Android changes the permission button label between OS versions. The
        prompt is optional because Appium may already have granted permissions.
        """
        permission_buttons = (
            (AppiumBy.ACCESSIBILITY_ID, "While using the app"),
            (AppiumBy.ACCESSIBILITY_ID, "Only this time"),
            (AppiumBy.ACCESSIBILITY_ID, "Allow"),
            (AppiumBy.XPATH, "//*[contains(@text, 'While using the app') or contains(@text, 'Only this time') or @text='Allow']"),
        )
        deadline = time.monotonic() + 5
        while time.monotonic() <= deadline:
            for by, value in permission_buttons:
                try:
                    elements = self.driver.find_elements(by, value)
                    visible = [element for element in elements if element.is_displayed()]
                    if visible:
                        visible[0].click()
                        logger.info("Allowed location permission")
                        return
                except (NoSuchElementException, WebDriverException):
                    continue
            time.sleep(0.25)

        logger.info("Location permission prompt was not displayed; continuing")


class ShortAdvisoryActions:
    def __init__(self, page: ShortAdvisoryPage):
        self.page = page

    def click_short_advisory(self) -> None:
        self.page.click_short_advisory()

    def allow_location_permission(self) -> None:
        self.page.allow_location_permission()

    def click_farmblock(self) -> None:
        self.page.click_farmblock()

    def select_farmblock(self, farmblock: str) -> None:
        self.page.select_farmblock(farmblock)

    def click_proceed_after_farmblock(self) -> None:
        self.page.click_proceed_after_farmblock()

    def click_crop_dropdown(self) -> None:
        self.page.click_crop_dropdown()

    def select_crop(self, crop: str) -> None:
        self.page.select_crop(crop)

    def click_crop_variety_dropdown(self) -> None:
        self.page.click_crop_variety_dropdown()

    def select_crop_variety(self, crop_variety: str) -> None:
        self.page.select_crop_variety(crop_variety)

    def click_text_toggle(self) -> None:
        self.page.click_text_toggle()

    def enter_observations(self, observations: str) -> None:
        self.page.enter_observations(observations)

    def set_camera_permission(self, decision: str) -> None:
        self.page.set_camera_permission(decision)

    def add_images(self, count: int = 6) -> None:
        self.page.add_images(count)

    def save_as_draft(self) -> None:
        self.page.save_as_draft()
