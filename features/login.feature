"""
Login feature tests using BDD.
Business-readable scenarios for login functionality.
"""

Feature: User Authentication

  @smoke @sanity @critical
  Scenario: Successful login with valid credentials
    Given user navigates to the login page
    When user enters valid email and password
    And user clicks the login button
    Then user should be logged in successfully
    And user should see the dashboard
    And success message should be displayed

  @sanity @regression
  Scenario: Login with invalid email format
    Given user navigates to the login page
    When user enters invalid email format
    And user enters valid password
    And user clicks the login button
    Then error message should be displayed
    And email error should show invalid format message

  @sanity @regression
  Scenario: Login with empty credentials
    Given user navigates to the login page
    When user leaves email and password empty
    And user clicks the login button
    Then validation error messages should appear
    And user should remain on login page

  @regression
  Scenario: Login with incorrect password
    Given user navigates to the login page
    When user enters valid email
    And user enters incorrect password
    And user clicks the login button
    Then error message should be displayed
    And error message should indicate invalid credentials

  @regression
  Scenario: Remember me checkbox functionality
    Given user navigates to the login page
    When user enters valid credentials
    And user checks the remember me checkbox
    And user clicks the login button
    Then user should be logged in successfully
    And remember me preference should be saved

  @regression
  Scenario: Password visibility toggle
    Given user navigates to the login page
    When user enters a password
    And user toggles password visibility
    Then password field type should change
    And password should remain visible

  @sanity @e2e
  Scenario Outline: Login with multiple user accounts
    Given user navigates to the login page
    When user enters email "<email>"
    And user enters password "<password>"
    And user clicks the login button
    Then login result should be "<result>"

    Examples:
      | email                    | password          | result    |
      | valid.user@partnerapp.co | ValidPass@123     | success   |
      | invalid.user@test.com    | InvalidPass@123   | failure   |
      | test@example.com         | WrongPassword     | failure   |

  @regression
  Scenario: Navigate to forgot password
    Given user navigates to the login page
    When user clicks on forgot password link
    Then user should be navigated to forgot password page
    And forgot password form should be displayed

  @regression
  Scenario: Navigate to sign up
    Given user navigates to the login page
    When user clicks on sign up link
    Then user should be navigated to sign up page
    And sign up form should be displayed
