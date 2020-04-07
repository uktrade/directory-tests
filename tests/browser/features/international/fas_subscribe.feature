@no-sso-email-verification-required
@allure.suite:International
Feature: FAS - Search

  Background:
    Given test authentication is done


  @allure.link:TT-2194
  @subscribe
  @dev-only
  @captcha
  Scenario: Buyers should be able to subscribe to receive email updates of the latest UK companies in randomly selected sector
    Given "Robert" visited "Find a Supplier - Subscribe for email updates" page

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Find a Supplier - Thank you for registering" page
    And "Robert" should be signed up for email updates of the latest UK companies in selected industry


  @allure.link:TT-2194
  @bug
  @allure.issue:TT-2186
  @fixed
  @search
  @subscribe
  @dev-only
  @captcha
  Scenario Outline: Buyers should be able to subscribe to receive email updates of the latest UK companies in "<specific>" sector
    Given "Robert" searched for companies using "<following>" keyword in "<specific>" sector

    When "Robert" fills out and submits "subscribe for email updates" form

    Then "Robert" should be on the "Find a Supplier - Thank you for registering" page
    And "Robert" should be signed up for email updates of the latest UK companies in selected industry

    Examples: Industries
      | following  | specific                               |
      | plants     | Agriculture horticulture and fisheries |
