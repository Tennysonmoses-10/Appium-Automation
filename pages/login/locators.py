"""
Login page locators for Partner App.
Centralized selector definitions following POM principles.
"""

from typing import Dict


class LoginLocators:
    """Locators for login page."""
    
    # Navigation and header
    PARTNER_APP_LOGO = "//img[@alt='Partner App Logo']"
    PAGE_TITLE = "//h1[contains(text(), 'Login')]"
    
    # Email/Username field
    EMAIL_INPUT = "//input[@id='email' or @name='email' or @data-testid='email-input']"
    EMAIL_LABEL = "//label[@for='email']"
    EMAIL_ERROR = "//span[@id='email-error' or @data-testid='email-error']"
    
    # Password field
    PASSWORD_INPUT = "//input[@id='password' or @name='password' or @type='password']"
    PASSWORD_LABEL = "//label[@for='password']"
    PASSWORD_ERROR = "//span[@id='password-error' or @data-testid='password-error']"
    PASSWORD_TOGGLE_VISIBILITY = "//button[@aria-label='Toggle password visibility']"
    
    # Remember me & forgot password
    REMEMBER_ME_CHECKBOX = "//input[@id='remember-me' or @name='remember_me']"
    REMEMBER_ME_LABEL = "//label[@for='remember-me']"
    FORGOT_PASSWORD_LINK = "//a[contains(text(), 'Forgot Password?')]"
    
    # Login button
    LOGIN_BUTTON = "//button[@id='login-btn' or @data-testid='login-button' or contains(text(), 'Login')]"
    
    # Social login (if applicable)
    GOOGLE_LOGIN_BUTTON = "//button[contains(text(), 'Google')]"
    MICROSOFT_LOGIN_BUTTON = "//button[contains(text(), 'Microsoft')]"
    
    # Links
    SIGN_UP_LINK = "//a[contains(text(), 'Create Account') or contains(text(), 'Sign Up')]"
    PRIVACY_POLICY_LINK = "//a[contains(text(), 'Privacy Policy')]"
    TERMS_OF_SERVICE_LINK = "//a[contains(text(), 'Terms of Service')]"
    
    # Messages
    SUCCESS_MESSAGE = "//div[@role='alert' and contains(text(), 'success')]"
    ERROR_MESSAGE = "//div[@role='alert' and contains(text(), 'error') or @class='error-message']"
    LOADING_SPINNER = "//div[@class='spinner' or @data-testid='loading']"
    
    # Generic selectors for flexibility
    FORM_CONTAINER = "//form[@id='login-form'] | //div[@class='login-form']"
    SUBMIT_BUTTON = "//button[@type='submit']"
    
    @classmethod
    def get_all_locators(cls) -> Dict[str, str]:
        """Get all locators as dictionary."""
        return {
            key: value for key, value in cls.__dict__.items()
            if not key.startswith("_") and isinstance(value, str)
        }
