@wip
@isd
@allure.suite:ISD
Feature: Investment Support Directory - Profiles


  @TT-1459
  @captcha
  @dev-only
  @fake-sso-email-verification
  Scenario: Once verified Company's ISD Business Profile should be published on ISD
    Given "Peter Alder" has created verified and published ISD business profile for company "Y"

    When "Peter Alder" decides to view published ISD Business Profile

    Then "Peter Alder" should be on "Y"'s ISD Business Profile page
