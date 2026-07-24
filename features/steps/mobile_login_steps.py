"""Behave step definitions for running mobile_login.feature directly."""

from behave import given, then, when

from core.logger import logger


@given("the mobile language screen is displayed")
def mobile_language_screen_is_displayed(context):
    context.mobile_login_page.enter_english()


@given("Proceed Button was pressed")
def proceed_button_was_pressed(context):
    context.mobile_login_actions.proceed_button()


@given("Get Started Button was pressed")
def get_started_button_was_pressed(context):
    context.mobile_login_actions.get_started()


@when('the user enters mobile number "{mobile_number}"')
def enter_mobile_number(context, mobile_number):
    context.mobile_login_actions.enter_mobile_number(mobile_number)


@when("Proceed Login Button was pressed")
def proceed_login_button_was_pressed(context):
    context.mobile_login_actions.proceed_login()


@when('the user enters otp "{otp}"')
def enter_otp(context, otp):
    context.mobile_login_actions.enter_otp(otp)


@when("Confirm Button was pressed")
def confirm_button_was_pressed(context):
    context.mobile_login_actions.confirm_otp()


@when("Clicked Advisory")
def advisory_button_was_clicked(context):
    context.mobile_login_actions.click_advisory()


@when("Clicked Ask Expert")
def ask_expert_button_was_clicked(context):
    context.mobile_login_actions.click_ask_expert()


@when("Clicked Short Advisory")
def short_advisory_button_was_clicked(context):
    context.short_advisory_actions.click_short_advisory()


@when("the location permission is allowed")
def location_permission_is_allowed(context):
    context.short_advisory_actions.allow_location_permission()


@when("Clicked Farmblock")
def farmblock_button_was_clicked(context):
    context.short_advisory_actions.click_farmblock()


@when('Selected Farmblock "{farmblock}"')
def farmblock_was_selected(context, farmblock):
    context.short_advisory_actions.select_farmblock(farmblock)


@when("Clicked Proceed after Farmblock selection")
def proceed_after_farmblock_selection(context):
    context.short_advisory_actions.click_proceed_after_farmblock()


@when("Clicked Crop dropdown")
def crop_dropdown_was_clicked(context):
    context.short_advisory_actions.click_crop_dropdown()


@when('Selected Crop "{crop}"')
def crop_was_selected(context, crop):
    context.short_advisory_actions.select_crop(crop)


@when("Clicked Crop Variety dropdown")
def crop_variety_dropdown_was_clicked(context):
    context.short_advisory_actions.click_crop_variety_dropdown()


@when('Selected Crop Variety "{crop_variety}"')
def crop_variety_was_selected(context, crop_variety):
    context.short_advisory_actions.select_crop_variety(crop_variety)


@when("Clicked Text toggle")
def text_toggle_was_clicked(context):
    context.short_advisory_actions.click_text_toggle()


@when('Entered observations "{observations}"')
def observations_were_entered(context, observations):
    context.short_advisory_actions.enter_observations(observations)


@when('Camera permission is set to "{decision}"')
def camera_permission_is_set(context, decision):
    context.short_advisory_actions.set_camera_permission(decision)


@when("Added {count} image from Camera")
def images_were_added(context, count):
    context.short_advisory_actions.add_images(int(count))


@when("Saved As Draft")
def advisory_was_saved_as_draft(context):
    context.short_advisory_actions.save_as_draft()


@when("Clicked Full Advisory")
def full_advisory_button_was_clicked(context):
    context.full_advisory_actions.click_full_advisory()


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
