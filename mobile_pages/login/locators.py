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

    HINDI=((
        AppiumBy.XPATH,
        '//android.view.View[@content-desc="हिंदी''आपके लिए, आपकी अपनी भाषा में"]'
           ),
    )
    hindi=HINDI

    MARATHI=((
        AppiumBy.XPATH,
        '//android.view.View[@content-desc="मराठी तुमच्यासाठी, तुमच्या स्वतःच्या भाषेत"]'
    ),
    )
    marathi=MARATHI

    PROCEED_BUTTON = ((
        AppiumBy.XPATH,'//android.view.View[@content-desc="Proceed"]',
                      ),
    )
    Proceed_BUTTON = PROCEED_BUTTON

    GET_STARTED=((
        AppiumBy.XPATH,
    '//android.view.View[@content-desc="Get Started"]'
    ),
    )
    get_started=GET_STARTED

    ENTER_MOBILENUMBER=((
        AppiumBy.XPATH,
    '//android.widget.EditText'
    ),
    )
    enter_mobilenumbers = ENTER_MOBILENUMBER

    PROCEED_LOGIN = ((
                              AppiumBy.XPATH,
                              '//android.view.View[@content-desc="Proceed"]'
                          ),
    )
    Proceed_Login = PROCEED_LOGIN


    ENTER_OTP = (
        (
            AppiumBy.XPATH,
"//android.widget.EditText[@focused='true']",
         #   "//android.widget.EditText[@max-text-length='4' and ancestor::android.view.View[contains(@content-desc,'Enter your verification code')]",
        ),
    )
    enter_otp = ENTER_OTP

    CONFIRM=((
        AppiumBy.XPATH,
        '//android.view.View[@content-desc="Confirm"]'
    ),
    )
    CONFIRM_BUTTON = CONFIRM

    ADVISORY_BUTTON=((
        AppiumBy.XPATH,
        '//android.widget.ImageView[@content-desc="Advisory"]'
    ),
    )
    advisory= ADVISORY_BUTTON

    ASK_EXPERT_BUTTON = (
        (
            AppiumBy.XPATH,
            '//android.view.View[@content-desc="Ask Expert"]',
        ),
    )
    ask_expert = ASK_EXPERT_BUTTON


    ERROR_MESSAGE = (
        (AppiumBy.ACCESSIBILITY_ID, "error_message"),
        (AppiumBy.ID, "com.partnerapp:id/error_message"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*:id/.*error.*")'),
    )
