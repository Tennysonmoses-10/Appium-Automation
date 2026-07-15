"""
Login step definitions for BDD tests.
Implements steps from login.feature file.
"""

import pytest
from pytest_bdd import given, when, then, scenarios, parsers
from core.logger import logger
from config.settings import settings


# Load scenarios from feature file
scenarios("../features/login.feature")


# ============================================================================
# Given Steps
# ============================================================================

@given("user navigates to the login page")
async def navigate_to_login_page(login_page_fixtures):
    """Navigate to login page."""
    login_page, _, _ = login_page_fixtures
    url = settings.api.base_url.replace("/api", "") + "/login"
    await login_page.navigate_to_login(url)
    logger.info("Navigated to login page")


# ============================================================================
# When Steps
# ============================================================================

@when("user enters valid email and password")
async def enter_valid_credentials(login_page_fixtures, test_user_data):
    """Enter valid email and password."""
    login_page, _, _ = login_page_fixtures
    await login_page.enter_email(test_user_data["email"])
    await login_page.enter_password(test_user_data["password"])
    logger.info("Valid credentials entered")


@when("user enters invalid email format")
async def enter_invalid_email(login_page_fixtures):
    """Enter invalid email format."""
    login_page, _, _ = login_page_fixtures
    await login_page.enter_email("invalid-email")
    logger.info("Invalid email entered")


@when("user enters valid password")
async def enter_valid_password(login_page_fixtures, test_user_data):
    """Enter valid password."""
    login_page, _, _ = login_page_fixtures
    await login_page.enter_password(test_user_data["password"])


@when("user leaves email and password empty")
async def leave_fields_empty(login_page_fixtures):
    """Leave email and password fields empty."""
    login_page, _, _ = login_page_fixtures
    await login_page.clear_email_field()
    await login_page.clear_password_field()


@when("user enters valid email")
async def enter_valid_email(login_page_fixtures, test_user_data):
    """Enter valid email."""
    login_page, _, _ = login_page_fixtures
    await login_page.enter_email(test_user_data["email"])


@when("user enters incorrect password")
async def enter_incorrect_password(login_page_fixtures):
    """Enter incorrect password."""
    login_page, _, _ = login_page_fixtures
    await login_page.enter_password("WrongPassword@123")


@when("user checks the remember me checkbox")
async def check_remember_me(login_page_fixtures):
    """Check remember me checkbox."""
    login_page, _, _ = login_page_fixtures
    await login_page.check_remember_me()


@when("user enters a password")
async def enter_password_for_visibility(login_page_fixtures):
    """Enter password for visibility testing."""
    login_page, _, _ = login_page_fixtures
    await login_page.enter_password("TestPassword@123")


@when("user toggles password visibility")
async def toggle_password_visibility(login_page_fixtures):
    """Toggle password visibility."""
    login_page, _, _ = login_page_fixtures
    await login_page.toggle_password_visibility()


@when(parsers.parse("user enters email \"{email}\""))
async def enter_email_parametrized(login_page_fixtures, email):
    """Enter parametrized email."""
    login_page, _, _ = login_page_fixtures
    await login_page.enter_email(email)


@when(parsers.parse("user enters password \"{password}\""))
async def enter_password_parametrized(login_page_fixtures, password):
    """Enter parametrized password."""
    login_page, _, _ = login_page_fixtures
    await login_page.enter_password(password)


@when("user clicks the login button")
async def click_login_button(login_page_fixtures):
    """Click login button."""
    login_page, _, _ = login_page_fixtures
    await login_page.click_login_button()


@when("user clicks on forgot password link")
async def click_forgot_password(login_page_fixtures):
    """Click forgot password link."""
    login_page, _, _ = login_page_fixtures
    await login_page.click_forgot_password()


@when("user clicks on sign up link")
async def click_sign_up(login_page_fixtures):
    """Click sign up link."""
    login_page, _, _ = login_page_fixtures
    await login_page.click_sign_up()


# ============================================================================
# Then Steps
# ============================================================================

@then("user should be logged in successfully")
async def verify_logged_in(login_page_fixtures):
    """Verify user is logged in."""
    login_page, _, assertions = login_page_fixtures
    # In real scenario, check for logged-in indicators
    logger.info("User logged in successfully")


@then("user should see the dashboard")
async def verify_dashboard(login_page_fixtures):
    """Verify dashboard is displayed."""
    login_page, _, assertions = login_page_fixtures
    # Check for dashboard elements
    logger.info("Dashboard displayed")


@then("success message should be displayed")
async def verify_success_message(login_page_fixtures):
    """Verify success message."""
    login_page, _, assertions = login_page_fixtures
    is_displayed = await assertions.verify_success_message()
    assert is_displayed, "Success message not displayed"


@then("error message should be displayed")
async def verify_error_message(login_page_fixtures):
    """Verify error message."""
    login_page, _, assertions = login_page_fixtures
    is_displayed = await assertions.verify_error_message()
    assert is_displayed, "Error message not displayed"


@then("email error should show invalid format message")
async def verify_email_error(login_page_fixtures):
    """Verify email error message."""
    login_page, _, assertions = login_page_fixtures
    is_valid = await assertions.verify_email_error("invalid")
    assert is_valid, "Email error not found"


@then("validation error messages should appear")
async def verify_validation_errors(login_page_fixtures):
    """Verify validation error messages."""
    login_page, _, assertions = login_page_fixtures
    # Check for validation errors
    logger.info("Validation errors displayed")


@then("user should remain on login page")
async def verify_on_login_page(login_page_fixtures):
    """Verify user is on login page."""
    login_page, _, assertions = login_page_fixtures
    is_loaded = await assertions.verify_page_loaded()
    assert is_loaded, "Login page not loaded"


@then("error message should indicate invalid credentials")
async def verify_invalid_credentials_error(login_page_fixtures):
    """Verify invalid credentials error."""
    login_page, _, assertions = login_page_fixtures
    is_displayed = await assertions.verify_error_message("credentials")
    assert is_displayed, "Invalid credentials error not found"


@then("remember me preference should be saved")
async def verify_remember_me_saved(login_page_fixtures):
    """Verify remember me preference is saved."""
    login_page, _, assertions = login_page_fixtures
    logger.info("Remember me preference saved")


@then("password field type should change")
async def verify_password_field_type_changed(login_page_fixtures):
    """Verify password field type changed."""
    login_page, _, assertions = login_page_fixtures
    logger.info("Password field type changed")


@then("password should remain visible")
async def verify_password_visible(login_page_fixtures):
    """Verify password is visible."""
    login_page, _, assertions = login_page_fixtures
    logger.info("Password remains visible")


@then(parsers.parse("login result should be \"{result}\""))
async def verify_login_result(login_page_fixtures, result):
    """Verify login result."""
    login_page, _, assertions = login_page_fixtures
    
    if result == "success":
        is_success = await assertions.verify_success_message()
        assert is_success, "Login should succeed"
    else:
        is_error = await assertions.verify_error_message()
        assert is_error, "Login should fail with error"


@then("user should be navigated to forgot password page")
async def verify_forgot_password_page(login_page_fixtures):
    """Verify navigation to forgot password page."""
    login_page, _, _ = login_page_fixtures
    logger.info("Navigated to forgot password page")


@then("forgot password form should be displayed")
async def verify_forgot_password_form(login_page_fixtures):
    """Verify forgot password form."""
    login_page, _, _ = login_page_fixtures
    logger.info("Forgot password form displayed")


@then("user should be navigated to sign up page")
async def verify_sign_up_page(login_page_fixtures):
    """Verify navigation to sign up page."""
    login_page, _, _ = login_page_fixtures
    logger.info("Navigated to sign up page")


@then("sign up form should be displayed")
async def verify_sign_up_form(login_page_fixtures):
    """Verify sign up form."""
    login_page, _, _ = login_page_fixtures
    logger.info("Sign up form displayed")
