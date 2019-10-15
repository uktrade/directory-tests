@TT-1033
@TT-1094
@enrol
@new-registration
Feature: Profile - Non-CH enrolment flows

  Background:
    Given basic authentication is done for "Domestic - Home" page


  @TT-1118
  @sole-trader-other-business
  Scenario: "Sole trader" representative should be asked to specify the type of their business before being asked to enter their email and set a password
    Given "Natalia" visits the "Profile - Select your business type" page

    When "Natalia" chooses "Sole trader or other type of business" option

    Then "Natalia" should be on the "Profile - Enter your email address and set a password (Sole trader or other type of business)" page
    And "Natalia" should see following sections
      | sections               |
      | Registration form      |
      | Enrolment progress bar |


  @TT-1119
  @uk-taxpayer
  Scenario: UK taxpayers can create an SSO account
    Given "Mirko" visits the "Profile - Select your business type" page

    When "Mirko" chooses "UK taxpayer" option

    Then "Mirko" should be on the "Profile - Enter your email address and set a password (UK taxpayer)" page
    And "Mirko" should see following sections
      | sections               |
      | Registration form      |
      | Enrolment progress bar |


  @TT-1119
  @foreign-business
  Scenario: Only UK business can create a great.gov.uk account
    Given "Mirko" visits the "Profile - Select your business type" page

    When "Mirko" chooses "Overseas company" option

    Then "Mirko" should be on the "Profile - You cannot create an account" page
    And "Mirko" should see following sections
      | sections               |
      | Explanation            |


  @foreign-business
  Scenario: Foreing business representative should be able to come back to our International site after learning that they can't create an account
    Given "Mirko" visits the "Profile - You cannot create an account" page

    When "Mirko" decides to "visit our site for international businesses"

    Then "Mirko" should be on the "International - landing" page


  @dev-only
  @TT-1120
  @ltd-plc-royal
  @sole-trader-other-business
  @tax-payer
  Scenario Outline: "<selected business type>" representative should receive an email with confirmation code
    Given "Natalia" visits the "Profile - Enter your email address and set a password (<selected business type>)" page

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Enter your confirmation code (<selected business type>)" page
    And "Natalia" should see following sections
      | sections                     |
      | Confirmation code message    |
      | Confirmation code form       |
      | An option to resend the code |
      | Enrolment progress bar       |
    And "Natalia" should receive email confirmation code

    Examples:
      | selected business type                |
      | Sole trader or other type of business |
      | UK taxpayer                           |


  @dev-only
  @TT-1121
  @ltd-plc-royal
  @sole-trader-other-business
  Scenario Outline: A representative of a "<selected business type>" company should be asked to enter their business details after providing email confirmation code
    Given "Natalia" has received the email confirmation code by opting to register as "<selected business type>"
    And "Natalia" is on the "Profile - Enter your confirmation code (<selected business type>)" page

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Enter your business details (<selected business type>)" page
    And "Natalia" should see following sections
      | sections                    |
      | Your business type          |
      | Enter your business details |
      | Enrolment progress bar      |

    Examples:
      | selected business type                |
      | LTD, PLC or Royal Charter             |
      | Sole trader or other type of business |


  @dev-only
  @TT-1122
  @uk-taxpayer
  Scenario: A UK taxpayers wanting to register should be asked to enter their details after providing email confirmation code
    Given "Natalia" has received the email confirmation code by opting to register as "UK taxpayer"
    And "Natalia" is on the "Profile - Enter your confirmation code (UK taxpayer)" page

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Enter your details (UK taxpayer)" page
    And "Natalia" should see following sections
      | sections               |
      | Your business type     |
      | Enter your details     |
      | Enrolment progress bar |



  @dev-only
  @TT-1123
  @ltd-plc-royal
  @sole-trader-other-business
  Scenario Outline: A representative of a "<selected business type>" company should be asked to enter their details after providing business details
    Given "Natalia" has received the email confirmation code by opting to register as "<selected business type>"
    And "Natalia" is on the "Profile - Enter your confirmation code (<selected business type>)" page

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Enter your business details (<selected business type>)" page
    And "Natalia" should see following sections
      | sections                    |
      | Your business type          |
      | Enter your business details |
      | Enrolment progress bar      |

    Examples:
      | selected business type                |
      | LTD, PLC or Royal Charter             |
      | Sole trader or other type of business |


  @captcha
  @dev-only
  @sole-trader-other-business
  @TT-1128
  @TT-1036
  Scenario: Handle invalid user state - has company already - redirect to their profile
    Given "Natalia" has created a great.gov.uk account for a "Sole trader or other type of business"

    When "Natalia" goes to the "SSO - Sign in" page
    Then "Natalia" should be on the "Profile - About" page

    When "Natalia" goes to the "Profile - Create an account" page
    Then "Natalia" should be on the "Profile - Edit Company Profile" page


  @captcha
  @dev-only
  @uk-taxpayer
  @TT-1128
  @TT-1036
  Scenario: Handle invalid user state - has company already - redirect to their profile
    Given "Natalia" has created a great.gov.uk account for a "UK taxpayer"

    When "Natalia" goes to the "SSO - Sign in" page
    Then "Natalia" should be on the "Profile - About" page

    When "Natalia" goes to the "Profile - Create an account" page
    Then "Natalia" should be on the "Profile - Create an account" page


  @wip
  @dev-only
  @TT-1130
  @TT-1037
  Scenario Outline: Log user in on verification submit, not on account creation
    Given "Natalia" has received the email confirmation code by opting to register as "<selected business type>"
    And "Natalia" is on the "Profile - Enter your confirmation code (<selected business type>)" page

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Enter your business details (<selected business type>)" page
    And "Natalia" should be logged in

    Examples:
      | selected business type                |
      | LTD, PLC or Royal Charter             |
      | Sole trader or other type of business |


  @TT-1560
  @uk-taxpayer
  Scenario: New registration for an individual who starts journey in Business profiles
    Given "Mirko" visited the "Find a Buyer - Home" page
    And "Mirko" decided to "Start now"
    And "Mirko" got to the "SSO - Sign in" page
    And "Mirko" decided to "Create account"
    And "Mirko" got to the "Profile - Create an account" page
    And "Mirko" decided to "start"
    And "Mirko" got to the "Profile - Select your business type" page

    When "Mirko" chooses "UK taxpayer" option

    Then "Mirko" should be on the "Profile - Start as Individual" page
    And "Mirko" should see following sections
      | sections    |
      | Breadcrumbs |
      | Explanation |
      | Links       |
