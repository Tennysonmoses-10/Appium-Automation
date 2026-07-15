"""
Login page actions - business workflows.
Contains high-level business operations composed from page interactions.
"""

from typing import Optional
from core.logger import logger
from core.retry_handler import retry_on_exception
from pages.login.page import LoginPage


class LoginActions:
    """Login page business actions."""
    
    def __init__(self, page: LoginPage):
        """
        Initialize LoginActions.
        
        Args:
            page: LoginPage instance
        """
        self.page = page
    
    @retry_on_exception(max_attempts=3, delay=1.0)
    async def perform_login(
        self,
        email: str,
        password: str,
        remember_me: bool = False,
    ) -> None:
        """
        Perform complete login action.
        
        Args:
            email: User email
            password: User password
            remember_me: Whether to check remember me checkbox
            
        Raises:
            Exception: If login fails
        """
        try:
            logger.info(f"Performing login for: {email}")
            
            # Clear fields first
            await self.page.clear_email_field()
            await self.page.clear_password_field()
            
            # Enter credentials
            await self.page.enter_email(email)
            await self.page.enter_password(password)
            
            # Check remember me if requested
            if remember_me:
                await self.page.check_remember_me()
            
            # Click login
            await self.page.click_login_button()
            
            # Wait for navigation
            await self.page.wait_for_page_load(timeout=10)
            
            logger.info(f"Login successful for: {email}")
        
        except Exception as e:
            logger.error(f"Login failed for {email}: {e}")
            raise
    
    async def perform_login_with_invalid_email(
        self,
        email: str,
        password: str,
    ) -> None:
        """
        Perform login with invalid email.
        
        Args:
            email: Invalid email
            password: Password
        """
        try:
            logger.info(f"Performing login with invalid email: {email}")
            
            await self.page.clear_email_field()
            await self.page.enter_email(email)
            await self.page.enter_password(password)
            await self.page.click_login_button()
            
            logger.info("Invalid email login attempt completed")
        
        except Exception as e:
            logger.error(f"Failed to perform login with invalid email: {e}")
            raise
    
    async def perform_login_with_empty_fields(self) -> None:
        """Perform login with empty email and password."""
        try:
            logger.info("Performing login with empty fields")
            
            await self.page.clear_email_field()
            await self.page.clear_password_field()
            await self.page.click_login_button()
            
            logger.info("Empty fields login attempt completed")
        
        except Exception as e:
            logger.error(f"Failed to perform login with empty fields: {e}")
            raise
    
    async def go_to_forgot_password(self) -> None:
        """Navigate to forgot password page."""
        try:
            logger.info("Navigating to forgot password page")
            await self.page.click_forgot_password()
        except Exception as e:
            logger.error(f"Failed to navigate to forgot password: {e}")
            raise
    
    async def go_to_sign_up(self) -> None:
        """Navigate to sign up page."""
        try:
            logger.info("Navigating to sign up page")
            await self.page.click_sign_up()
        except Exception as e:
            logger.error(f"Failed to navigate to sign up: {e}")
            raise
    
    async def toggle_password_visibility_and_verify(self) -> bool:
        """
        Toggle password visibility and verify it changes.
        
        Returns:
            True if password visibility changed
        """
        try:
            logger.info("Toggling password visibility")
            
            # Get initial password input type
            password_input = self.page.page.locator("//input[@id='password']")
            initial_type = await password_input.get_attribute("type")
            
            # Toggle visibility
            await self.page.toggle_password_visibility()
            
            # Get new password input type
            new_type = await password_input.get_attribute("type")
            
            changed = initial_type != new_type
            logger.info(f"Password visibility toggled: {changed}")
            
            return changed
        
        except Exception as e:
            logger.error(f"Failed to toggle password visibility: {e}")
            raise
    
    async def verify_remember_me_state(self, should_be_checked: bool) -> bool:
        """
        Verify remember me checkbox state.
        
        Args:
            should_be_checked: Expected checked state
            
        Returns:
            True if state matches expectation
        """
        try:
            checkbox = self.page.page.locator("//input[@id='remember-me']")
            is_checked = await checkbox.is_checked()
            
            matches = is_checked == should_be_checked
            logger.info(f"Remember me checkbox state: {is_checked} (expected: {should_be_checked})")
            
            return matches
        
        except Exception as e:
            logger.error(f"Failed to verify remember me state: {e}")
            raise
