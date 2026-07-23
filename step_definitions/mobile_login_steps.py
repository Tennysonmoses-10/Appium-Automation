"""BDD step definitions for native mobile login scenarios."""

from pytest_bdd import given, parsers, scenarios, then, when

from core.logger import logger

scenarios("../features/mobile_login.feature")


@given("the mobile language screen is displayed")
def mobile_login_screen_is_displayed(mobile_login_page_fixtures):
    login_page, _, _ = mobile_login_page_fixtures
    login_page.enter_english()

@given("Proceed Button was pressed")
def proceed_button_was_pressed(mobile_login_page_fixtures):
    _, actions, _ = mobile_login_page_fixtures
    actions.proceed_button()


@given("Get Started Button was pressed")
def get_started_button_was_pressed(mobile_login_page_fixtures):
    _, actions, _ = mobile_login_page_fixtures
    actions.get_started()


@when(parsers.parse('the user enters mobile number "{mobile_number}"'))
def enter_mobile_number(mobile_login_page_fixtures, mobile_number):
    _, actions, _ = mobile_login_page_fixtures
    actions.enter_mobile_number(mobile_number)


@when("Proceed Login Button was pressed")
def proceed_login_button_was_pressed(mobile_login_page_fixtures):
    _, actions, _ = mobile_login_page_fixtures
    actions.proceed_login()


@when(parsers.parse('the user enters otp "{otp}"'))
def enter_otp(mobile_login_page_fixtures, otp):
    _, actions, _ = mobile_login_page_fixtures
    actions.enter_otp(otp)


@when("Confirm Button was pressed")
def confirm_button_was_pressed(mobile_login_page_fixtures):
    _, actions, _ = mobile_login_page_fixtures
    actions.confirm_otp()

@when("Clicked Advisory")
def advisory_button_was_clicked(mobile_login_page_fixtures):
    _, actions, _ = mobile_login_page_fixtures
    actions.click_advisory()


@when("Clicked Ask Expert")
def ask_expert_button_was_clicked(mobile_login_page_fixtures):
    _, actions, _ = mobile_login_page_fixtures
    actions.click_ask_expert()


@when("Clicked Short Advisory")
def short_advisory_button_was_clicked(mobile_login_page_fixtures):
    from mobile_pages.login.short_advisory import ShortAdvisoryActions, ShortAdvisoryPage

    login_page, _, _ = mobile_login_page_fixtures
    ShortAdvisoryActions(ShortAdvisoryPage(login_page.driver)).click_short_advisory()


@when("Clicked Full Advisory")
def full_advisory_button_was_clicked(mobile_login_page_fixtures):
    from mobile_pages.login.full_advisory import FullAdvisoryActions, FullAdvisoryPage

    login_page, _, _ = mobile_login_page_fixtures
    FullAdvisoryActions(FullAdvisoryPage(login_page.driver)).click_full_advisory()


@then("a mobile login error should be displayed")
def mobile_login_error_is_displayed(mobile_login_page_fixtures):
    _, _, assertions = mobile_login_page_fixtures
    assert assertions.verify_error_message(), "Mobile login error is not displayed"
