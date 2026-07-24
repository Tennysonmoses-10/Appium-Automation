Feature: Mobile advisory flows

  @mobile @android @login @shortadvisory @smoke
  Scenario: Open Short Advisory after mobile login
    Given the mobile language screen is displayed
    And Proceed Button was pressed
    And Get Started Button was pressed
    When the user enters mobile number "8652513863"
    And Proceed Login Button was pressed
    And the user enters otp "2655"
    And Confirm Button was pressed
    And Clicked Advisory
    And Clicked Ask Expert
    When Clicked Short Advisory
    And the location permission is allowed
    When Clicked Farmblock
    And Selected Farmblock "WTC"
    And Clicked Proceed after Farmblock selection
    When Clicked Crop dropdown
    And Selected Crop "Grapes"
    And Clicked Crop Variety dropdown
    And Selected Crop Variety "Anushka"
    And Clicked Text toggle
    And Entered observations "Grapes crop is healthy and requires regular irrigation."
    And Camera permission is set to "allow"
    And Added 1 image from Camera

    #And Saved As Draft

  @mobile @android @login @invalidmobile
  Scenario Outline: Reject invalid mobile number
    Given the mobile language screen is displayed
    And Proceed Button was pressed
    And Get Started Button was pressed
    When the user enters mobile number "<mobile_number>"
    And Proceed Login Button was pressed
    Then a mobile login error should be displayed

    Examples:
      | mobile_number |
      | 12345         |
      | 86525138630   |

  @mobile @android @login @invalidotp
  Scenario Outline: Reject invalid OTP
    Given the mobile language screen is displayed
    And Proceed Button was pressed
    And Get Started Button was pressed
    When the user enters mobile number "8652513863"
    And Proceed Login Button was pressed
    And the user enters otp "<otp>"
    And Confirm Button was pressed
    Then a mobile login error should be displayed

    Examples:
      | otp  |
      | 0000 |
      | 1234 |

  @mobile @android @login @fulladvisory @smoke
  Scenario: Open Full Advisory after mobile login
    Given the mobile language screen is displayed
    And Proceed Button was pressed
    And Get Started Button was pressed
    When the user enters mobile number "8652513863"
    And Proceed Login Button was pressed
    And the user enters otp "2655"
    And Confirm Button was pressed
    And Clicked Advisory
    And Clicked Ask Expert
    When Clicked Full Advisory
