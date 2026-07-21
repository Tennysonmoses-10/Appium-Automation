"""Behave step definitions for running mobile_login.feature directly."""

from behave import given, then, when

from core.logger import logger


@given("the mobile language screen is displayed")
def mobile_language_screen_is_displayed(context):
    context.mobile_login_page.enter_english()


@given("Proceed Button was pressed")
def proceed_button_was_pressed(context):
    context.mobile_login_actions.proceed_button()


@when("the user logs in on mobile with valid credentials")
def login_with_valid_mobile_credentials(context):
    email = context.config.userdata.get("email", "test@example.com")
    password = context.config.userdata.get("password", "TestPassword@123")
    context.mobile_login_actions.login(email, password)


@when('the user logs in on mobile with email "{email}" and password "{password}"')
def login_with_mobile_credentials(context, email, password):
    context.mobile_login_actions.login(email, password)


@then("the mobile dashboard should be displayed")
def mobile_dashboard_is_displayed(context):
    assert context.mobile_login_assertions.verify_dashboard_displayed(), "Mobile dashboard is not displayed"
    logger.info("Mobile dashboard displayed")


@then("a mobile login error should be displayed")
def mobile_login_error_is_displayed(context):
    assert context.mobile_login_assertions.verify_error_message(), "Mobile login error is not displayed"
