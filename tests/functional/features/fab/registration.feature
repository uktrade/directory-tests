Feature: Trade Profile


    @ED-2094
    @profile
    @verification
    @letter
    @fake-sso-email-verification
    Scenario: Logged-in Supplier should be able to verify profile by using code and link from the letter
      Given "Annette Geissinger" created a verified SSO/great.gov.uk account associated with randomly selected company "Company X"
      And "Annette Geissinger" built the company profile
      And "Annette Geissinger" set the company description
      And "Annette Geissinger" received the letter with verification code

      When "Annette Geissinger" goes to the verification link from the letter as authenticated user
      And "Annette Geissinger" submits the verification code

      Then "Annette Geissinger" should be told that company has been verified


    @ED-2094
    @profile
    @verification
    @letter
    @fake-sso-email-verification
    Scenario: Logged-out Supplier should be able to verify profile by using code and link from the letter
      Given "Annette Geissinger" created a verified SSO/great.gov.uk account associated with randomly selected company "Company X"
      And "Annette Geissinger" built the company profile
      And "Annette Geissinger" set the company description
      And "Annette Geissinger" signed out from Find a Buyer service
      And "Annette Geissinger" received the letter with verification code

      When "Annette Geissinger" goes to the verification link from the letter as unauthenticated user
      And "Annette Geissinger" submits the verification code

      Then "Annette Geissinger" should be told that company has been verified
