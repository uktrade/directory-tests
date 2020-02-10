@sso
@allure.suite:SSO
Feature: SSO - login


  @account
  @manage
  @password
  @no-sso-email-verification-required
  Scenario: Unregistered users shouldn't be able to login to SSO/great.gov.uk account
    Given "Peter Alder" is an unauthenticated supplier

    When "Peter Alder" attempts to sign in to SSO/great.gov.uk account

    Then "Peter Alder" should see "The e-mail address and/or password you specified are not correct" message
