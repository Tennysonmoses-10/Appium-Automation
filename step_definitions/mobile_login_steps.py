"""BDD step definitions for native mobile login scenarios."""

from pytest_bdd import given, parsers, scenarios, then, when

from core.logger import logger

scenarios("../features/mobile_login.feature")


@given("the mobile language screen is displayed")
def mobile_login_screen_is_displayed(mobile_login_page_fixtures):
    login_page, _, _ = mobile_login_page_fixtures
    login_page.enter_english()  # or login_page.enter_english() depending on your method name

@when("the user logs in on mobile with valid credentials")
def login_with_valid_mobile_credentials(mobile_login_page_fixtures, test_user_data):
    _, actions, _ = mobile_login_page_fixtures
    actions.login(test_user_data["email"], test_user_data["password"])


@when(parsers.parse('the user logs in on mobile with email "{email}" and password "{password}"'))
def login_with_mobile_credentials(mobile_login_page_fixtures, email, password):
    _, actions, _ = mobile_login_page_fixtures
    actions.login(email, password)


@then("the mobile dashboard should be displayed")
def mobile_dashboard_is_displayed(mobile_login_page_fixtures):
    _, _, assertions = mobile_login_page_fixtures
    assert assertions.verify_dashboard_displayed(), "Mobile dashboard is not displayed"
    logger.info("Mobile dashboard displayed")


@then("a mobile login error should be displayed")
def mobile_login_error_is_displayed(mobile_login_page_fixtures):
    _, _, assertions = mobile_login_page_fixtures
    assert assertions.verify_error_message(), "Mobile login error is not displayed"
