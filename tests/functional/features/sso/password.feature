Feature: SSO password management


    @ED-2146
    @sso
    @account
    @manage
    @password
    Scenario: Suppliers without FAB profile should receive a message with password reset link
      Given "Peter Alder" has a verified standalone SSO/great.gov.uk account
      And "Peter Alder" is signed out from SSO/great.gov.uk account

      When "Peter Alder" resets the password

      Then "Peter Alder" should be told that password was reset
      And "Peter Alder" should receive a password reset email


    @ED-2251
    @sso
    @account
    @manage
    @password
    Scenario: Suppliers with verified FAB profile should receive a message with password reset link
      Given "Peter Alder" has created and verified profile for randomly selected company "Y"
      And "Peter Alder" signed out from Find a Buyer service

      When "Peter Alder" resets the password

      Then "Peter Alder" should be told that password was reset
      And "Peter Alder" should receive a password reset email


    @ED-2251
    @sso
    @account
    @manage
    @password
    Scenario: Suppliers with unverified FAB profile should receive a message with password reset link
      Given "Peter Alder" created an unverified profile for randomly selected company "Y"
      And "Peter Alder" signed out from Find a Buyer service

      When "Peter Alder" resets the password

      Then "Peter Alder" should be told that password was reset
      And "Peter Alder" should receive a password reset email


    @wip
    @ED-2146
    @sso
    @account
    @manage
    @password
    Scenario: Suppliers with FAB profile should be able to reset password
      Given "Peter Alder" created an unverified profile for randomly selected company "Y"
      And "Peter Alder" received a password reset email

      When "Peter Alder" changes the password to a new one using the password reset link


    @wip
    @ED-2146
    @sso
    @account
    @manage
    @password
    Scenario: Suppliers without FAB profile should be able to reset password
      Given "Peter Alder" has a verified standalone SSO/great.gov.uk account
      And "Peter Alder" received a password reset email

      When "Peter Alder" changes the password to a new one using the password reset link


    @wip
    @ED-2146
    @sso
    @account
    @manage
    @password
    Scenario: Suppliers should be able to reset (change) the password to the same one
      Given "Peter Alder" has a verified standalone SSO/great.gov.uk account
      And "Peter Alder" is signed out from SSO/great.gov.uk account

      When "Peter Alder" changes the password to the same one using the password reset link

      Then "Peter Alder" should be told that password was reset


    @wip
    @ED-2146
    @sso
    @account
    @manage
    @password
    Scenario: Suppliers should not be to use the password reset link more than once
