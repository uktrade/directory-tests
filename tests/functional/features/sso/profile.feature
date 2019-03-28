Feature: SSO profile


  @ED-1757
  @sso
  @login
  @verification
  @no-sso-email-verification-required
  Scenario: Suppliers without verified email should be told to verify the email address first before being able to log in
    Given "Annette Geissinger" is an unauthenticated supplier
    And "Annette Geissinger" created an unverified SSO/great.gov.uk account

    When "Annette Geissinger" attempts to sign in to SSO/great.gov.uk account

    Then "Annette Geissinger" should be told that she needs to verify her email address first


  @ED-1756
  @sso
  @account
  @real-email-verification
  Scenario: Suppliers should receive an email verification msg after creating a standalone SSO/great.gov.uk account
    Given "Peter Alder" is an unauthenticated supplier

    When "Peter Alder" creates an unverified SSO/great.gov.uk account

    Then "Peter Alder" should be told about the verification email
    And "Peter Alder" should receive an email verification msg entitled "Your great.gov.uk account: Please Confirm Your E-mail Address"


  @ED-1756
  @ED-1692
  @sso
  @account
  @verification
  @real-sso-email-verification
  Scenario: Suppliers should be able to confirm email address for a standalone SSO/great.gov.uk account
    Given "Peter Alder" created a standalone SSO/great.gov.uk account with unverified email address
    And "Peter Alder" received the email verification message with the email confirmation link

    When "Peter Alder" decides to confirm her email address by using the email confirmation link
    And "Peter Alder" confirms the email address for SSO/great.gov.uk account

    Then "Peter Alder" should be on Welcome to your great.gov.uk profile page
    And "Peter Alder" should be signed in to SSO/great.gov.uk account


  @ED-2145
  @sso
  @account
  @no-sso-email-verification-required
  Scenario: Suppliers should not be able to register with the same email again
    # No error should be displayed when Supplier attempts to register with an
    # existing email address (intended behaviour) yet no verification email
    # should be sent. Moreover there's no point in checking in DB whether
    # there's only 1 account with the same email address as there's `unique`
    # constraint configured on the `email` column.
    Given "Peter Alder" is an unauthenticated supplier

    When "Peter Alder" creates an unverified SSO/great.gov.uk account
    Then "Peter Alder" should be told about the verification email

    When "Peter Alder" creates an unverified SSO/great.gov.uk account
    Then "Peter Alder" should be told about the verification email


  @ED-2147
  @sso
  @account
  @fake-sso-email-verification
  Scenario: Suppliers should be able to sign out and sign back in
    Given "Peter Alder" has a verified standalone SSO/great.gov.uk account
    And "Peter Alder" signed out from SSO/great.gov.uk account

    When "Peter Alder" signs in to SSO/great.gov.uk account

    Then "Peter Alder" should be signed in to SSO/great.gov.uk account


  @ED-1769
  @login
  @fab
  @dev-only
  @fake-sso-email-verification
  Scenario: Suppliers with unverified company profile should be able to logout and log back in
    Given "Annette Geissinger" created an unverified business profile for randomly selected company "Company X"
    And "Annette Geissinger" signed out from SSO/great.gov.uk account

    When "Annette Geissinger" signs in to SSO/great.gov.uk account from "FAB Landing"

    Then "Annette Geissinger" should be on "Profile - edit company profile" page


  @ED-1758
  @fab
  @login
  @dev-only
  @fake-sso-email-verification
  Scenario: Suppliers with verified company profile should be able to logout and log back in
    Given "Peter Alder" has created verified and published business profile for randomly selected company "Y"
    And "Peter Alder" signed out from SSO/great.gov.uk account

    When "Peter Alder" signs in to SSO/great.gov.uk account from "FAB Landing"

    Then "Peter Alder" should be on "Profile - edit company profile" page
