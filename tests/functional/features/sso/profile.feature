@sso
@dev-only
@captcha
Feature: SSO profile


  @bug
  @TT-1823
  @fixed
  @ED-1757
  @login
  @verification
  @no-sso-email-verification-required
  Scenario: Suppliers without verified email should be told to verify the email address first before being able to log in
    Given "Annette Geissinger" is an unauthenticated supplier
    And "Annette Geissinger" created an "unverified Individual" profile

    When "Annette Geissinger" attempts to sign in to SSO/great.gov.uk account

    Then "Annette Geissinger" should be told that she needs to verify her email address first


  @ED-2145
  @account
  @no-sso-email-verification-required
  Scenario: Suppliers should not be able to register with the same email again
    # No error should be displayed when Supplier attempts to register with an
    # existing email address (intended behaviour) yet no verification email
    # should be sent. Moreover there's no point in checking in DB whether
    # there's only 1 account with the same email address as there's `unique`
    # constraint configured on the `email` column.
    Given "Peter Alder" is an unauthenticated supplier

    When "Peter Alder" creates an "unverified Individual" profile
    Then "Peter Alder" should be on "Profile - Enter email verification code (UK taxpayer)" page

    When "Peter Alder" creates an "unverified Individual" profile
    Then "Peter Alder" should be on "Profile - Enter email verification code (UK taxpayer)" page


  @ED-2147
  @account
  @fake-sso-email-verification
  Scenario: Suppliers should be able to sign out and sign back in
    Given "Peter Alder" created a "verified Individual" profile
    And "Peter Alder" signed out from SSO/great.gov.uk account

    When "Peter Alder" signs in to SSO/great.gov.uk account

    Then "Peter Alder" should be signed in to SSO/great.gov.uk account
