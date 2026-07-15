"""
Login page assertions - validation methods.
Contains verification and assertion methods for login page validation.
"""

from typing import Optional
from core.logger import logger
from pages.login.locators import LoginLocators
from pages.login.page import LoginPage


class LoginAssertions:
    """Login page validation and assertions."""
    
    def __init__(self, page: LoginPage):
        """
        Initialize LoginAssertions.
        
        Args:
            page: LoginPage instance
        """
        self.page = page
    
    async def verify_page_loaded(self) -> bool:
        """
        Verify login page is loaded.
        
        Returns:
            True if page loaded successfully
        """
        try:
            # Check if key elements are visible
            email_visible = await self.page.page.locator(
                LoginLocators.EMAIL_INPUT
            ).is_visible()
            password_visible = await self.page.page.locator(
                LoginLocators.PASSWORD_INPUT
            ).is_visible()
            login_button_visible = await self.page.page.locator(
                LoginLocators.LOGIN_BUTTON
            ).is_visible()
            
            page_loaded = email_visible and password_visible and login_button_visible
            
            if page_loaded:
                logger.info("Login page loaded successfully")
            else:
                logger.warning(
                    f"Login page not fully loaded. "
                    f"Email: {email_visible}, Password: {password_visible}, "
                    f"Button: {login_button_visible}"
                )
            
            return page_loaded
        
        except Exception as e:
            logger.error(f"Failed to verify page load: {e}")
            return False
    
    async def verify_success_message(self, expected_text: str = None) -> bool:
        """
        Verify success message is displayed.
        
        Args:
            expected_text: Expected text in success message
            
        Returns:
            True if success message found
        """
        try:
            message = await self.page.get_success_message()
            
            if not message:
                logger.warning("Success message not found")
                return False
            
            if expected_text and expected_text not in message:
                logger.warning(
                    f"Success message '{message}' does not contain '{expected_text}'"
                )
                return False
            
            logger.info(f"Success message verified: {message}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to verify success message: {e}")
            return False
    
    async def verify_error_message(self, expected_text: str = None) -> bool:
        """
        Verify error message is displayed.
        
        Args:
            expected_text: Expected text in error message
            
        Returns:
            True if error message found
        """
        try:
            message = await self.page.get_error_message()
            
            if not message:
                logger.warning("Error message not found")
                return False
            
            if expected_text and expected_text not in message:
                logger.warning(
                    f"Error message '{message}' does not contain '{expected_text}'"
                )
                return False
            
            logger.info(f"Error message verified: {message}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to verify error message: {e}")
            return False
    
    async def verify_email_field_visible(self) -> bool:
        """Verify email input field is visible."""
        try:
            is_visible = await self.page.page.locator(
                LoginLocators.EMAIL_INPUT
            ).is_visible()
            
            if is_visible:
                logger.info("Email field is visible")
            else:
                logger.warning("Email field is not visible")
            
            return is_visible
        
        except Exception as e:
            logger.error(f"Failed to verify email field visibility: {e}")
            return False
    
    async def verify_password_field_visible(self) -> bool:
        """Verify password input field is visible."""
        try:
            is_visible = await self.page.page.locator(
                LoginLocators.PASSWORD_INPUT
            ).is_visible()
            
            if is_visible:
                logger.info("Password field is visible")
            else:
                logger.warning("Password field is not visible")
            
            return is_visible
        
        except Exception as e:
            logger.error(f"Failed to verify password field visibility: {e}")
            return False
    
    async def verify_login_button_enabled(self) -> bool:
        """Verify login button is enabled."""
        try:
            is_enabled = await self.page.page.locator(
                LoginLocators.LOGIN_BUTTON
            ).is_enabled()
            
            if is_enabled:
                logger.info("Login button is enabled")
            else:
                logger.warning("Login button is disabled")
            
            return is_enabled
        
        except Exception as e:
            logger.error(f"Failed to verify login button status: {e}")
            return False
    
    async def verify_email_value(self, expected_email: str) -> bool:
        """
        Verify email field contains expected value.
        
        Args:
            expected_email: Expected email value
            
        Returns:
            True if email matches
        """
        try:
            actual_email = await self.page.get_email_value()
            
            if actual_email == expected_email:
                logger.info(f"Email value verified: {actual_email}")
                return True
            else:
                logger.warning(
                    f"Email mismatch. Expected: {expected_email}, Actual: {actual_email}"
                )
                return False
        
        except Exception as e:
            logger.error(f"Failed to verify email value: {e}")
            return False
    
    async def verify_email_field_empty(self) -> bool:
        """Verify email field is empty."""
        try:
            email_value = await self.page.get_email_value()
            
            if not email_value:
                logger.info("Email field is empty")
                return True
            else:
                logger.warning(f"Email field is not empty: {email_value}")
                return False
        
        except Exception as e:
            logger.error(f"Failed to verify email field is empty: {e}")
            return False
    
    async def verify_email_error(self, expected_error_text: str = None) -> bool:
        """
        Verify email field error message.
        
        Args:
            expected_error_text: Expected error text
            
        Returns:
            True if error found
        """
        try:
            error_element = self.page.page.locator(LoginLocators.EMAIL_ERROR)
            
            if not await error_element.is_visible():
                logger.warning("Email error message not visible")
                return False
            
            error_text = await error_element.text_content()
            
            if expected_error_text and expected_error_text not in error_text:
                logger.warning(
                    f"Error text mismatch. Expected: {expected_error_text}, "
                    f"Actual: {error_text}"
                )
                return False
            
            logger.info(f"Email error verified: {error_text}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to verify email error: {e}")
            return False
    
    async def verify_page_title(self, expected_title: str = "Login") -> bool:
        """
        Verify page title.
        
        Args:
            expected_title: Expected page title
            
        Returns:
            True if title matches
        """
        try:
            actual_title = await self.page.page.title()
            
            if expected_title in actual_title:
                logger.info(f"Page title verified: {actual_title}")
                return True
            else:
                logger.warning(
                    f"Title mismatch. Expected: {expected_title}, Actual: {actual_title}"
                )
                return False
        
        except Exception as e:
            logger.error(f"Failed to verify page title: {e}")
            return False
