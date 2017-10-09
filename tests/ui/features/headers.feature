Feature: Export is Great common page header


  Scenario Outline: Header should look the same
    Given "Adam" goes to the "<specific>" page

    Then "Adam" should see the standard Directory page header

    Examples:
      | specific          |
      | New to exporting  |