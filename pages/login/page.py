"""
Login page - low-level interactions.
Handles element interactions without business logic.
"""

from typing import Optional
from playwright.async_api import Page, Locator
from core.logger import logger
from core.wait_utils import ExplicitWait, WaitCondition
from pages.login.locators import LoginLocators


class LoginPage:
    """Login page interactions layer."""
    
    def __init__(self, page: Page):
        """
        Initialize LoginPage.
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        self.waiter = ExplicitWait(timeout=10)
    
    async def navigate_to_login(self, url: str) -> None:
        """
        Navigate to login page.
        
        Args:
            url: Login page URL
        """
        try:
            await self.page.goto(url, wait_until="networkidle")
            logger.info(f"Navigated to login page: {url}")
        except Exception as e:
            logger.error(f"Failed to navigate to login page: {e}")
            raise
    
    async def enter_email(self, email: str) -> None:
        """
        Enter email address.
        
        Args:
            email: Email address
        """
        try:
            await self.page.fill(LoginLocators.EMAIL_INPUT, email)
            logger.debug(f"Entered email: {email}")
        except Exception as e:
            logger.error(f"Failed to enter email: {e}")
            raise
    
    async def enter_password(self, password: str) -> None:
        """
        Enter password.
        
        Args:
            password: Password
        """
        try:
            await self.page.fill(LoginLocators.PASSWORD_INPUT, password)
            logger.debug("Entered password")
        except Exception as e:
            logger.error(f"Failed to enter password: {e}")
            raise
    
    async def toggle_password_visibility(self) -> None:
        """Toggle password field visibility."""
        try:
            await self.page.click(LoginLocators.PASSWORD_TOGGLE_VISIBILITY)
            logger.info("Password visibility toggled")
        except Exception as e:
            logger.warning(f"Failed to toggle password visibility: {e}")
    
    async def check_remember_me(self) -> None:
        """Check remember me checkbox."""
        try:
            checkbox = self.page.locator(LoginLocators.REMEMBER_ME_CHECKBOX)
            is_checked = await checkbox.is_checked()
            if not is_checked:
                await checkbox.check()
            logger.info("Remember me checked")
        except Exception as e:
            logger.error(f"Failed to check remember me: {e}")
            raise
    
    async def uncheck_remember_me(self) -> None:
        """Uncheck remember me checkbox."""
        try:
            checkbox = self.page.locator(LoginLocators.REMEMBER_ME_CHECKBOX)
            is_checked = await checkbox.is_checked()
            if is_checked:
                await checkbox.uncheck()
            logger.info("Remember me unchecked")
        except Exception as e:
            logger.error(f"Failed to uncheck remember me: {e}")
            raise
    
    async def click_login_button(self) -> None:
        """Click login button."""
        try:
            await self.page.click(LoginLocators.LOGIN_BUTTON)
            logger.info("Login button clicked")
        except Exception as e:
            logger.error(f"Failed to click login button: {e}")
            raise
    
    async def click_forgot_password(self) -> None:
        """Click forgot password link."""
        try:
            await self.page.click(LoginLocators.FORGOT_PASSWORD_LINK)
            logger.info("Forgot password link clicked")
        except Exception as e:
            logger.error(f"Failed to click forgot password link: {e}")
            raise
    
    async def click_sign_up(self) -> None:
        """Click sign up link."""
        try:
            await self.page.click(LoginLocators.SIGN_UP_LINK)
            logger.info("Sign up link clicked")
        except Exception as e:
            logger.error(f"Failed to click sign up link: {e}")
            raise
    
    async def get_email_value(self) -> str:
        """Get email input value."""
        try:
            value = await self.page.input_value(LoginLocators.EMAIL_INPUT)
            return value or ""
        except Exception as e:
            logger.error(f"Failed to get email value: {e}")
            raise
    
    async def get_password_value(self) -> str:
        """Get password input value."""
        try:
            value = await self.page.input_value(LoginLocators.PASSWORD_INPUT)
            return value or ""
        except Exception as e:
            logger.error(f"Failed to get password value: {e}")
            raise
    
    async def get_error_message(self) -> Optional[str]:
        """
        Get error message text.
        
        Returns:
            Error message or None if not present
        """
        try:
            error_locator = self.page.locator(LoginLocators.ERROR_MESSAGE)
            if await error_locator.is_visible():
                return await error_locator.text_content()
            return None
        except Exception as e:
            logger.debug(f"Failed to get error message: {e}")
            return None
    
    async def get_success_message(self) -> Optional[str]:
        """
        Get success message text.
        
        Returns:
            Success message or None if not present
        """
        try:
            success_locator = self.page.locator(LoginLocators.SUCCESS_MESSAGE)
            if await success_locator.is_visible():
                return await success_locator.text_content()
            return None
        except Exception as e:
            logger.debug(f"Failed to get success message: {e}")
            return None
    
    async def is_loading(self) -> bool:
        """
        Check if page is loading.
        
        Returns:
            True if loading spinner is visible
        """
        try:
            return await self.page.locator(LoginLocators.LOADING_SPINNER).is_visible()
        except Exception as e:
            logger.debug(f"Failed to check loading state: {e}")
            return False
    
    async def wait_for_page_load(self, timeout: int = 10) -> bool:
        """
        Wait for page to fully load.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            True if page loaded
        """
        try:
            await self.page.wait_for_load_state("networkidle", timeout=timeout * 1000)
            logger.info("Login page fully loaded")
            return True
        except Exception as e:
            logger.error(f"Failed waiting for page load: {e}")
            return False
    
    async def clear_email_field(self) -> None:
        """Clear email input field."""
        try:
            await self.page.fill(LoginLocators.EMAIL_INPUT, "")
            logger.debug("Email field cleared")
        except Exception as e:
            logger.error(f"Failed to clear email field: {e}")
            raise
    
    async def clear_password_field(self) -> None:
        """Clear password input field."""
        try:
            await self.page.fill(LoginLocators.PASSWORD_INPUT, "")
            logger.debug("Password field cleared")
        except Exception as e:
            logger.error(f"Failed to clear password field: {e}")
            raise
