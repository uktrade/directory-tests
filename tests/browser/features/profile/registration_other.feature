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

    When "Mirko" decides to "view our site for international businesses"

    Then "Mirko" should be on the "International - landing" page


  @wip
  @dev-only
  @TT-1120
  @ltd-plc-royal
  @sole-trader-other-business
  @tax-payer
  Scenario Outline: "<selected business type>" representative should receive an email with confirmation code
    Given "Natalia" opted to register for a great.gov.uk account as "<selected business type>"
    And "Natalia" is on the "Profile - Enter your email and set a password (<selected business type>)" page

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Enter your confirmation code (<selected business type>)" page
    And "Natalia" should see following sections
      | sections                     |
      | Confirmation code message    |
      | Confirmation code form       |
      | An option to resend the code |
      | Enrolment progress bar       |
    And "Natalia" should receive a "Your confirmation code" email

    Examples:
      | selected business type                |
      | LTD, PLC or Royal Charter             |
      | Sole trader or other type of business |
      | UK taxpayer                           |


  @wip
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


  @wip
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



  @wip
  @dev-only
  @TT-1123
  @ltd-plc-royal
  @sole-trader-other-business
  Scenario Outline: A representative of a "<selected business type>" company should be asked to enter their details after providing business details
    Given "Natalia" has received the email confirmation code by opting to register as "<selected business type>"
    And "Natalia" is on the "Profile - Enter your business details (<selected business type>)" page

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Enter your details (<selected business type>)" page
    And "Natalia" should see following sections
      | sections                    |
      | Your business type          |
      | Your business details       |
      | Enter your details form     |
      | Enrolment progress bar      |

    Examples:
      | selected business type                |
      | LTD, PLC or Royal Charter             |
      | Sole trader or other type of business |


  @wip
  @dev-only
  @TT-1124
  @ltd-plc-royal
  @sole-trader-other-business
  @uk-taxpayer
  Scenario Outline: A representative of a "<selected business type>" company should receive a confirmation email when a great.gov.uk account is created
    Given "Natalia" got to the "Profile - Enter your details (<selected business type>)" by opting to register as "<selected business type>"

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Account created" page
    And "Natalia" should see following sections
      | sections                   |
      | Confirmation email message |
      | Next steps                 |
    And "Natalia" should receive "Account registration confirmation" email

    Examples:
      | selected business type                |
      | LTD, PLC or Royal Charter             |
      | Sole trader or other type of business |
      | UK taxpayer                           |


  @wip
  @dev-only
  @TT-1125
  @TT-1017
  Scenario: When CH record doesn't include business' address the business representative should be referred to a contact page
    Given "Natalia" has received the email confirmation code by opting to register as "<selected business type>"
    And "Natalia" is on the "Profile - Enter your confirmation code (<selected business type>)" page

    When "Natalia" decides to use "I cannot find my business name" link

    Then "Natalia" should be on the "Domestic - I cannot find my business name - Dedicated Support Content" page


  @wip
  @dev-only
  @TT-1126
  @TT-1031
  Scenario: Companies House company enrolment creates a business profile
    Given "Natalia" has created a great.gov.uk account for a "LTD, PLC or Royal Charter"

    When "Natalia" goes to the "Find a Buyer - Edit Company Profile" page

    Then "Natalia" should be on the "Find a Buyer - Edit Company Profile" page


  @wip
  @dev-only
  @TT-1127
  @TT-1035
  Scenario Outline: Handle case of if the email already present in Profile-Profile
    Given "Natalia" opted to register for a great.gov.uk account as "<selected business type>"
    And "Natalia" is on the "Profile - Enter your email and set a password (<selected business type>)" page

    When "Natalia" fills out and submits the form
      | field              | value                             |
      | Your email address | already-registered-email@test.com |

    Then "Natalia" should be on the "Profile - Enter your confirmation code (<selected business type>)" page
    And "Natalia" should receive "Someone is trying to create an account with us. You already have an account." email

    Examples:
      | selected business type                |
      | LTD, PLC or Royal Charter             |
      | Sole trader or other type of business |
      | UK taxpayer                           |


  @wip
  @dev-only
  @TT-1128
  @TT-1036
  Scenario Outline: Handle invalid user state - has company already - redirect to their profile
    Given "Natalia" created a verified Profile/great.gov.uk account associated with randomly selected company "X"

    When "Natalia" goes to the "<specific>" page

    Then "Natalia" should be on the "Find a Buyer - Edit Company Profile" page

    Examples:
      | specific                    |
      | Profile - Sign in           |
      | Profile - Create an account |


  @wip
  @dev-only
  @TT-1129
  @TT-1036
  Scenario Outline: Handle invalid user state - already logged in - skip ahead to page where they enter business details
    Given "Natalia" has a verified standalone Profile/great.gov.uk account

    When "Natalia" goes to the "Create an account" page
    Then "Natalia" should be on the "Profile - Select your business type" page

    When "Natalia" chooses "<selected business type>" option
    Then "Natalia" should be on the "Profile - Enter your business details (<selected business type>)" page

    Examples:
      | selected business type                |
      | LTD, PLC or Royal Charter             |
      | Sole trader or other type of business |


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
