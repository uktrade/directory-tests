@TT-1033
@TT-1094
@enrol
@new-registration
Feature: Profile - CH enrolment flows

  Background:
    Given basic authentication is done for "Domestic - Home" page

  @TT-1115
  Scenario: Users should be presented with the Enrolment Steps prior to starting the registration process
    Given "Natalia" visits the "Profile - Create an account" page

    When "Natalia" decides to "start"

    Then "Natalia" should be on the "Profile - Select your business type" page
    And "Natalia" should see following sections
      | sections               |
      | Breadcrumbs            |
      | Form                   |
      | Enrolment progress bar |
    And "Natalia" should see following form choices
      | radio elements                        |
      | LTD, PLC or Royal Charter             |
      | Sole trader or other type of business |
      | UK taxpayer                           |
      | Overseas Company                      |


  @TT-1115
  Scenario: Users should be presented with the Enrolment Steps prior to starting the registration process
    Given "Natalia" visits the "Profile - Select your business type" page

    When "Natalia" chooses "LTD, PLC or Royal Charter" option

    Then "Natalia" should be on the "Profile - Enter your email address and set a password (LTD, PLC or Royal Charter)" page
    And "Natalia" should see following sections
      | sections                  |
      | Breadcrumbs               |
      | Registration form         |
      | Enrolment progress bar    |


  @TT-1117
  @ltd-plc-royal
  @tax-payer
  Scenario Outline: "<business type>" representative should be asked to enter their email and set a password after selecting their business type
    Given "Natalia" visits the "Profile - Enter your email address and set a password (<business type>)" page

    Then "Natalia" should see following sections
      | sections               |
      | Registration form      |
      | Enrolment progress bar |

    Examples:
      | business type             |
      | LTD, PLC or Royal Charter |


  @dev-only
  @TT-1120
  @ltd-plc-royal
  @sole-trader-other-business
  @tax-payer
  Scenario Outline: "<business type>" representative should receive an email with confirmation code
    Given "Natalia" visits the "Profile - Enter your email address and set a password (<business type>)" page

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Enter your confirmation code" page
    And "Natalia" should see following sections
      | sections                     |
      | Confirmation code message    |
      | Confirmation code form       |
      | An option to resend the code |
      | Enrolment progress bar       |
    And "Natalia" should receive email confirmation code

    Examples:
      | business type             |
      | LTD, PLC or Royal Charter |


  @dev-only
  @TT-1121
  @ltd-plc-royal
  @sole-trader-other-business
  Scenario Outline: A representative of a "<selected business type>" company should be asked to enter their business details after providing email confirmation code
    Given "Natalia" has received the email confirmation code by opting to register as "<selected business type>"
    And "Natalia" is on the "Profile - Enter your confirmation code" page

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Enter your business details (<selected business type>)" page
    And "Natalia" should see following sections
      | sections                    |
      | Enter your business details |
      | Enrolment progress bar      |

    Examples:
      | selected business type    |
      | LTD, PLC or Royal Charter |


  @dev-only
  @TT-1123
  @ltd-plc-royal
  @sole-trader-other-business
  Scenario Outline: A representative of a "<selected business type>" company should be asked to enter their details after providing business details
    Given "Natalia" has received the email confirmation code by opting to register as "<selected business type>"
    And "Natalia" is on the "Profile - Enter your confirmation code" page

    When "Natalia" fills out and submits the form
    Then "Natalia" should be on the "Profile - Enter your business details (<selected business type>)" page

    When "Natalia" fills out and submits the form (and go 1 page back on error)
    Then "Natalia" should be on the "Profile - Enter your business details [step 2] (<selected business type>)" page

    When "Natalia" fills out and submits the form
    Then "Natalia" should be on the "Profile - Enter your details (<selected business type>)" page
    And "Natalia" should see following sections
      | sections                    |
      | Enter your details form     |
      | Enrolment progress bar      |

    Examples:
      | selected business type      |
      | LTD, PLC or Royal Charter   |


  @dev-only
  @TT-1124
  @ltd-plc-royal
  @sole-trader-other-business
  @uk-taxpayer
  Scenario Outline: A representative of a "selected business type" company should receive a confirmation email when a great.gov.uk account is created
    Given "Natalia" has received the email confirmation code by opting to register as "<selected business type>"
    And "Natalia" is on the "Profile - Enter your confirmation code" page

    When "Natalia" fills out and submits the form
    Then "Natalia" should be on the "Profile - Enter your business details (<selected business type>)" page

    When "Natalia" fills out and submits the form (and go 1 page back on error)
    Then "Natalia" should be on the "Profile - Enter your business details [step 2] (<selected business type>)" page

    When "Natalia" fills out and submits the form
    Then "Natalia" should be on the "Profile - Enter your details (<selected business type>)" page

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Account created" page
    And "Natalia" should see following sections
      | sections                   |
      | Confirmation email message |
#      | Next steps                 |

    Examples:
      | selected business type     |
      | LTD, PLC or Royal Charter  |


  @dev-only
  @TT-1126
  @TT-1031
  Scenario: Companies House company enrolment creates a business profile
    Given "Natalia" has created a great.gov.uk account for a "LTD, PLC or Royal Charter"

    When "Natalia" goes to the "Profile - Edit Company Profile" page

    Then "Natalia" should be on the "Profile - Edit Company Profile" page


  @dev-only
  @verification-code
  Scenario: Users should be able to resend email verification code
    Given "Natalia" has received the email confirmation code by opting to register as "LTD, PLC or Royal Charter"
    And "Natalia" is on the "Profile - Enter your confirmation code" page

    When "Natalia" decides to use "Resend my code" link
    Then "Natalia" should be on the "Domestic - I have not received a verification code - Dedicated Support Content" page

    When "Natalia" decides to use "Resend your code" link
    Then "Natalia" should be on the "Profile - Resend your verification code" page

    When "Natalia" fills out and submits the form
    Then "Natalia" should be on the "Profile - Re-enter your confirmation code" page
    And "Natalia" should receive email with a new confirmation code

    When "Natalia" fills out and submits the form
    Then "Natalia" should be on the "Profile - Enter your business details (LTD, PLC or Royal Charter)" page


  @wip
  @dev-only
  @TT-1125
  @TT-1017
  Scenario: When CH record doesn't include business' address the business representative should be referred to a contact page
    Given "Natalia" has received the email confirmation code by opting to register as "LTD, PLC or Royal Charter"
    And "Natalia" is on the "Profile - Enter your confirmation code" page

    When "Natalia" decides to use "I cannot find my business name" link

    Then "Natalia" should be on the "Domestic - I cannot find my business name - Dedicated Support Content" page


  @dev-only
  @TT-1127
  @TT-1035
  Scenario Outline: Handle case of if the email already present in Profile-Profile
    Given "Natalia" has a verified standalone SSO/great.gov.uk account
    And "Natalia" decided to create a great.gov.uk account as "<selected business type>"

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "<email verification>" page
    And "Natalia" should receive "Sign in to great.gov.uk services" email containing "There is an account already registered to this email address" message

    Examples:
      | selected business type                | email verification                                                   |
      | LTD, PLC or Royal Charter             | Profile - Enter your confirmation code                               |
      | Sole trader or other type of business | Profile - Enter your confirmation code (Sole trader or other type of business) |
      | UK taxpayer                           | Profile - Enter your confirmation code (Individual)                  |


  @captcha
  @dev-only
  @TT-1128
  @TT-1036
  Scenario: Handle invalid user state - has company already - redirect to their profile
    Given "Natalia" has created a great.gov.uk account for a "LTD, PLC or Royal Charter"

    When "Natalia" goes to the "SSO - Sign in" page
    Then "Natalia" should be on the "Profile - About" page

    When "Natalia" goes to the "Profile - Create an account" page
    Then "Natalia" should be on the "Profile - Edit Company Profile" page


  @dev-only
  @TT-1129
  @TT-1036
  Scenario Outline: Handle invalid user state - already logged in - skip ahead to page where they enter business details for "<selected business type>"
    Given "Natalia" has a verified standalone SSO/great.gov.uk account
    And "Natalia" is signed in

    When "Natalia" goes to the "Profile - Create an account" page
    And "Natalia" decides to "start"
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
  Scenario Outline: Log user in on verification submit, not on account creation for "<selected business type>"
    Given "Natalia" has received the email confirmation code by opting to register as "<selected business type>"
    And "Natalia" is on the "Profile - Enter your confirmation code" page

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Enter your business details (<selected business type>)" page
    And "Natalia" should be logged in

    Examples:
      | selected business type                |
      | LTD, PLC or Royal Charter             |
      | Sole trader or other type of business |


  @bug
  @TT-1281
  @fixed
  @captcha
  @dev-only
  Scenario Outline: Newly registered users should see their business type on "Profile - Business profile" page
    Given "Natalia" has created a great.gov.uk account for a "<selected business type>"

    When "Natalia" goes to the "Profile - Edit Company Profile" page

    Then "Natalia" should see "<expected business type>" on the page

    Examples: business types
      | selected business type                | expected business type                        |
      | LTD, PLC or Royal Charter             | UK business registered in Companies House     |
      | Sole trader or other type of business | UK business not registered in Companies House |
      | UK taxpayer                           | Get a business profile                        |
