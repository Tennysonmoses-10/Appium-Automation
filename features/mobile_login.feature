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
