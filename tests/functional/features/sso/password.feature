@sso
@dev-only
@captcha
Feature: SSO password management


  @ED-2146
  @account
  @manage
  @password
  @fake-sso-email-verification
  Scenario: Suppliers with just SSO/great.gov.uk account should be able to reset password
    Given "Peter Alder" created a "verified Individual" profile
    And "Peter Alder" signed out from SSO/great.gov.uk account
    And "Peter Alder" requested and received a password reset email

    When "Peter Alder" changes the password to a new one using the password reset link

    Then "Peter Alder" should be on Welcome to your great.gov.uk profile page


  @bug
  @TT-876
  @fixed
  @ED-2251
  @account
  @manage
  @password
  @dev-only
  @captcha
  @no-sso-email-verification-required
  Scenario: Suppliers with unverified Business Profile should be able to reset password
    Given "Peter Alder" created an "unpublished unverified LTD, PLC or Royal Charter" profile for a random company "Y"
    And "Peter Alder" signed out from SSO/great.gov.uk account
    And "Peter Alder" requested and received a password reset email

    When "Peter Alder" changes the password to a new one using the password reset link

    Then "Peter Alder" should be on Welcome to your great.gov.uk profile page


  @ED-2251
  @account
  @manage
  @password
  @dev-only
  @captcha
  @fake-sso-email-verification
  Scenario: Suppliers with verified Business Profile should be able to reset password
    Given "Peter Alder" created a "published LTD, PLC or Royal Charter" profile for a random company "Y"
    And "Peter Alder" signed out from SSO/great.gov.uk account
    And "Peter Alder" requested and received a password reset email

    When "Peter Alder" changes the password to a new one using the password reset link

    Then "Peter Alder" should be on Welcome to your great.gov.uk profile page


  @bug
  @TT-1297
  @fixme
  @ED-2251
  @account
  @manage
  @password
  @fake-sso-email-verification
  Scenario: Suppliers should not be able to change the password to one with only letters
    Given "Peter Alder" created a "verified Individual" profile
    And "Peter Alder" signed out from SSO/great.gov.uk account
    And "Peter Alder" requested and received a password reset email

    When "Peter Alder" attempts to change the password to one with only letters and using the password reset link

    Then "Peter Alder" should see "This password contains letters only." message


  @ED-2146
  @account
  @manage
  @password
  @fake-sso-email-verification
  Scenario: Suppliers should be able to reset (change) the password to the same one
    Given "Peter Alder" created a "verified Individual" profile
    And "Peter Alder" requested and received a password reset email

    When "Peter Alder" changes the password to the same one using the password reset link

    Then "Peter Alder" should be on Welcome to your great.gov.uk profile page


  @ED-2146
  @account
  @manage
  @password
  @fake-sso-email-verification
  Scenario: Suppliers should not be able to use the password reset link more than once
    Given "Peter Alder" created a "verified Individual" profile
    And "Peter Alder" signed out from SSO/great.gov.uk account
    And "Peter Alder" requested and received a password reset email

    When "Peter Alder" changes the password to a new one using the password reset link
    Then "Peter Alder" should be on Welcome to your great.gov.uk profile page

    When "Peter Alder" opens the password reset link

    Then "Peter Alder" should be told that password reset link is invalid
