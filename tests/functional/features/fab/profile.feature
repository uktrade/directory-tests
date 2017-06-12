Feature: Trade Profile


    @registration
    Scenario Outline: Supplier should receive a verification email after successful registration
      Given "Peter Alder" is an unauthenticated supplier

      And the supplier accepts the SSO T&Cs
      When "Peter Alder" randomly selects an active company without a profile identified by an alias "Company X"
      And "Peter Alder" confirms that "Company X" is the correct one
      And "Peter Alder" confirms that the export status of "Company X" is "<current>"

      Then the supplier should be told about the verification email
      And the supplier should receive a verification email entitled "Your great.gov.uk account: Please Confirm Your E-mail Address"

      Examples:
        | current                        |
        | Yes, in the last year          |
        | Yes, 1 to 2 years ago          |
        | Yes, but more than 2 years ago |
        | No, but we are preparing to    |