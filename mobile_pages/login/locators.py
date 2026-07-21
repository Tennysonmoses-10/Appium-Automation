"""Appium locator definitions for the mobile login screen."""

from appium.webdriver.common.appiumby import AppiumBy


class MobileLoginLocators:
    """Android-first locators with accessibility-id fallbacks for iOS support."""

    LANGUAGE_SELECTION = (
        (
            AppiumBy.XPATH,
            '//android.view.View[@content-desc="English\nFor you, in your own language"]',
        ),
    )
    Language_Selection = LANGUAGE_SELECTION
    EMAIL_INPUT = (
        (AppiumBy.ACCESSIBILITY_ID, "email_input"),
        (AppiumBy.ID, "com.meerolink.app:id/email"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*:id/email")'),
        (AppiumBy.IOS_PREDICATE, "name == 'email_input' OR name == 'email'"),
    )
    PASSWORD_INPUT = (
        (AppiumBy.ACCESSIBILITY_ID, "password_input"),
        (AppiumBy.ID, "com.partnerapp:id/password"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*:id/password")'),
        (AppiumBy.IOS_PREDICATE, "name == 'password_input' OR name == 'password'"),
    )
    LOGIN_BUTTON = (
        (AppiumBy.ACCESSIBILITY_ID, "login_button"),
        (AppiumBy.ID, "com.partnerapp:id/login_button"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textMatches("(?i)login|sign in")'),
        (AppiumBy.IOS_PREDICATE, "name == 'login_button' OR label IN {'Login', 'Sign In'}"),
    )
    FORGOT_PASSWORD_LINK = (
        (AppiumBy.ACCESSIBILITY_ID, "forgot_password"),
        (AppiumBy.ID, "com.partnerapp:id/forgot_password"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Forgot")'),
    )
    SIGN_UP_LINK = (
        (AppiumBy.ACCESSIBILITY_ID, "sign_up"),
        (AppiumBy.ID, "com.partnerapp:id/sign_up"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textMatches("(?i)sign up|create account")'),
    )
    ERROR_MESSAGE = (
        (AppiumBy.ACCESSIBILITY_ID, "error_message"),
        (AppiumBy.ID, "com.partnerapp:id/error_message"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*:id/.*error.*")'),
    )
    DASHBOARD_TITLE = (
        (AppiumBy.ACCESSIBILITY_ID, "dashboard_title"),
        (AppiumBy.ID, "com.partnerapp:id/dashboard_title"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Dashboard")'),
    )
