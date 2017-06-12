Feature: Trade Profile


    @registration
    Scenario Outline: Supplier should receive a verification email after successful registration
      Given "Peter Alder" is an unauthenticated supplier

      When the supplier randomly selects an active company without a profile identified by an alias 'Company X'
      And the supplier confirms that the selected company is correct
      And the supplier confirms that "<export status>" his company sold products or services to overseas customers
      And the supplier provides “valid” registration details
      And the supplier accepts the T&Cs

      Then the supplier should be told about the verification email
      And the supplier should receive a verification email entitled "Your great.gov.uk account: Please Confirm Your E-mail Address"

      Examples:
        | export_status                  |
        | Yes, in the last year          |
#        | Yes, 1 to 2 years ago          |
#        | Yes, but more than 2 years ago |
#        | No, but we are preparing to    |