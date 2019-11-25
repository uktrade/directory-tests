@no-sso-email-verification-required
Feature: FAS - Search

  Background:
    Given basic authentication is done for "International - Landing" page


  @subscribe
  @dev-only
  @captcha
  Scenario: Buyers should be able to subscribe to receive email updates of the latest UK companies in randomly selected sector
    Given "Robert" visited "Find a Supplier - Subscribe for email updates" page

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Find a Supplier - Thank you for registering" page


  @bug
  @TT-2186
  @fixed
  @search
  @subscribe
  @dev-only
  @captcha
  Scenario Outline: Buyers should be able to subscribe to receive email updates of the latest UK companies in "<specific>" sector
    Given "Robert" searched for companies using "<following>" keyword in "<specific>" sector

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Find a Supplier - Thank you for registering" page

    Examples: Industries
      | following  | specific                               |
      | plants     | Agriculture horticulture and fisheries |
