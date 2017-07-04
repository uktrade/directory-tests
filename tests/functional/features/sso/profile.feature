Feature: SSO profile


    @ED-1756
    @sso
    @account
    Scenario: Suppliers should receive an email verification msg after creating a standalone SSO/great.gov.uk account
      Given "Peter Alder" is an unauthenticated supplier

      When "Peter Alder" creates a SSO/great.gov.uk account

      Then "Peter Alder" should be told about the verification email
      And "Peter Alder" should receive an email verification msg entitled "Your great.gov.uk account: Please Confirm Your E-mail Address"


    @ED-1756
    @sso
    @account
    Scenario: Suppliers should be able to confirm email address for a standalone SSO/great.gov.uk account
      Given "Peter Alder" created a standalone SSO/great.gov.uk account with unverified email address

      When "Peter Alder" decides to confirm her email address by using the email confirmation link
      And "Peter Alder" confirms the email address for SSO/great.gov.uk account

      Then "Peter Alder" should be on Welcome to your great.gov.uk profile page
      And "Peter Alder" should be signed in to SSO/great.gov.uk account
