@TT-1033
@TT-1094
@enrol
@new-registration
Feature: New Enrolment flow

  Background:
    Given basic authentication is done for "Profile - About" page

  @TT-1115
  Scenario: Users should be presented with the Enrolment Steps prior to starting the registration process
    Given "Natalia" visits the "Profile - Create an account" page

    When "Natalia" decides to "Start now"

    Then "Natalia" should be on the "Profile - Enter your business email address and set a password" page
    And "Natalia" should see following sections
      | sections                  |
      | Breadcrumbs               |
      | Registration form         |
      | Enrolment progress bar    |


  @TT-1117
  @ltd-plc-royal
  @tax-payer
  Scenario Outline: "<business type>" representative should be asked to enter their email and set a password after selecting their business type
    Given "Natalia" visits the "Profile - Enter your business email address and set a password (<business type>)" page

    Then "Natalia" should see following sections
      | sections               |
      | Registration form      |
      | Enrolment progress bar |

    Examples:
      | business type             |
      | LTD, PLC or Royal Charter |


  @TT-1120
  @ltd-plc-royal
  @sole-trader-other-business
  @tax-payer
  Scenario Outline: "<selected business type>" representative should receive an email with confirmation code
    Given "Natalia" visits the "Profile - Enter your business email address and set a password (<business type>)" page

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


  @TT-1124
  @ltd-plc-royal
  @sole-trader-other-business
  @uk-taxpayer
  Scenario Outline: A representative of a "selected business type" company should receive a confirmation email when a great.gov.uk account is created
#    Given "Natalia" got to the "Profile - Enter your details (for <selected business type>)" by opting to register as "<selected business type>"
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
      | Next steps                 |

    Examples:
      | selected business type     |
      | LTD, PLC or Royal Charter  |


  @wip
  @TT-1125
  @TT-1017
  Scenario: When CH record doesn't include business' address the business representative should be referred to a contact page
    Given "Natalia" has received the email confirmation code by opting to register as "LTD, PLC or Royal Charter"
    And "Natalia" is on the "Profile - Enter your confirmation code" page

    When "Natalia" decides to use "I cannot find my business name" link

    Then "Natalia" should be on the "Export Readiness - I cannot find my business name - Dedicated Support Content" page


  @TT-1126
  @TT-1031
  Scenario: Companies House company enrolment creates a business profile
    Given "Natalia" has created a great.gov.uk account for a "LTD, PLC or Royal Charter"

    When "Natalia" goes to the "Find A Buyer - Edit Company Profile" page

    Then "Natalia" should be on the "Find A Buyer - Edit Company Profile" page


  @wip
  @TT-1127
  @TT-1035
  Scenario Outline: Handle case of if the email already present in Profile-Profile
    Given "Natalia" opted to register for a great.gov.uk account as "<selected business type>"
    And "Natalia" is on the "Profile - Enter your email and set a password" page

    When "Natalia" fills out and submits the form
      | field              | value                             |
      | Your email address | already-registered-email@test.com |

    Then "Natalia" should be on the "Profile - Enter your confirmation code" page
    And "Natalia" should receive "Someone is trying to create an account with us. You already have an account." email

    Examples:
      | selected business type                |
      | LTD, PLC or Royal Charter             |
      | Sole trader or other type of business |
      | UK taxpayer                           |


  @wip
  @TT-1128
  @TT-1036
  Scenario Outline: Handle invalid user state - has company already - redirect to their profile
    Given "Natalia" created a verified Profile/great.gov.uk account associated with randomly selected company "X"

    When "Natalia" goes to the "<specific>" page

    Then "Natalia" should be on the "Find A Buyer - Edit Company Profile" page

    Examples:
      | specific                |
      | Profile - Sign in           |
      | Profile - Create an account |


  @wip
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
  @TT-1130
  @TT-1037
  Scenario Outline: Log user in on verification submit, not on account creation
    Given "Natalia" has received the email confirmation code by opting to register as "<selected business type>"
    And "Natalia" is on the "Profile - Enter your confirmation code" page

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Enter your business details (<selected business type>)" page
    And "Natalia" should be logged in

    Examples:
      | selected business type                |
      | LTD, PLC or Royal Charter             |
      | Sole trader or other type of business |
