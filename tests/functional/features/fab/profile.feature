Feature: Trade Profile


    @registration
    Scenario Outline: Supplier should receive a verification email after successful registration
      Given "Peter Alder" is an unauthenticated supplier

      When the supplier randomly selects an active company without a profile identified by an alias "Company X"
      And the supplier confirms that "Company X" is the correct one
      And the supplier confirms that the export status of "Company X" is "<current>"
      And the supplier provides "valid" SSO registration details
      And the supplier accepts the SSO T&Cs

      Then the supplier should be told about the verification email
      And the supplier should receive a verification email entitled "Your great.gov.uk account: Please Confirm Your E-mail Address"

      Examples:
        | current                        |
        | Yes, in the last year          |
        | Yes, 1 to 2 years ago          |
        | Yes, but more than 2 years ago |
        | No, but we are preparing to    |