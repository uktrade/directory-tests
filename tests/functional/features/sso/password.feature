Feature: SSO password management


    @ED-2146
    @sso
    @account
    @manage
    @password
    Scenario: Suppliers with just SSO/great.gov.uk account should be able to reset password
      Given "Peter Alder" has a verified standalone SSO/great.gov.uk account
      And "Peter Alder" signed out from SSO/great.gov.uk account
      And "Peter Alder" received a password reset email

      When "Peter Alder" changes the password to a new one using the password reset link

      Then "Peter Alder" should be on Welcome to your great.gov.uk profile page


    @ED-2251
    @sso
    @account
    @manage
    @password
    Scenario: Suppliers with unverified FAB profile should be able to reset password
      Given "Peter Alder" created an unverified profile for randomly selected company "Y"
      And "Peter Alder" signed out from Find a Buyer service
      And "Peter Alder" received a password reset email

      When "Peter Alder" changes the password to a new one using the password reset link

      Then "Peter Alder" should be on Welcome to your great.gov.uk profile page


    @ED-2251
    @sso
    @account
    @manage
    @password
    Scenario: Suppliers with verified FAB profile should be able to reset password
      Given "Peter Alder" has created and verified profile for randomly selected company "Y"
      And "Peter Alder" signed out from Find a Buyer service
      And "Peter Alder" received a password reset email

      When "Peter Alder" changes the password to a new one using the password reset link

      Then "Peter Alder" should be on Welcome to your great.gov.uk profile page


    @ED-2146
    @sso
    @account
    @manage
    @password
    Scenario: Suppliers should be able to reset (change) the password to the same one
      Given "Peter Alder" has a verified standalone SSO/great.gov.uk account
      And "Peter Alder" received a password reset email

      When "Peter Alder" changes the password to the same one using the password reset link

      Then "Peter Alder" should be on Welcome to your great.gov.uk profile page


    @ED-2146
    @sso
    @account
    @manage
    @password
    Scenario: Suppliers should not be to use the password reset link more than once
      Given "Peter Alder" has a verified standalone SSO/great.gov.uk account
      And "Peter Alder" signed out from SSO/great.gov.uk account
      And "Peter Alder" received a password reset email

      When "Peter Alder" changes the password to a new one using the password reset link
      Then "Peter Alder" should be on Welcome to your great.gov.uk profile page

      When "Peter Alder" opens the password reset link

      Then "Peter Alder" should be told that password reset link is invalid
