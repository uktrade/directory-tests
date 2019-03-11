@TT-1033
@TT-1094
@enrol
@new-registration
Feature: New Enrolment flow

  Background:
    Given hawk cookie is set on "Profile - About" page

  @wip
  @TT-1115
  Scenario: Users should be presented with the Enrolment Steps prior to starting the registration process
    Given "Natalia" visits the "Profile - Sign in" page

    When "Natalia" decides to "Start now"

    Then "Natalia" should be on the "SUD - Select your business type" page
    And "Natalia" should see following sections
      | sections                  |
      | Breadcrumbs               |
      | Description               |
      | Enrolment progress bar    |

  @wip
  @TT-1116
  Scenario: Users should be asked for their business type once they start the registration process
    Given "Natalia" visits the "Profile - Create an account" page

    When "Natalia" decides to "Start now"

    Then "Natalia" should be on the "Profile - Select your business type" page
    And "Natalia" should see following form choices
      | radio elements                        |
      | LTD, PLC or Royal Charter             |
      | Sole trader or other type of business |
      | UK taxpayer                           |
      | Overseas Company                      |


  @wip
  @TT-1117
  @ltd-plc-royal
  @tax-payer
  Scenario Outline: "<business type>" representative should be asked to enter their email and set a password after selecting their business type
    Given "Natalia" visits the "Profile - Select your business type" page

    When "Natalia" chooses "<business type>" option

    Then "Natalia" should be on the "Profile - Enter your email and set a password (<business type>)" page
    And "Natalia" should see following sections
      | sections               |
      | Registration form      |
      | Enrolment progress bar |

    Examples:
      | business type             |
      | LTD, PLC or Royal Charter |
      | UK taxpayer               |


  @wip
  @TT-1118
  @sole-trader-other-business
  Scenario Outline: "<business type>" representative should be asked to specify the type of their business before being asked to enter their email and set a password
    Given "Natalia" visits the "Profile - Select your business type" page

    When "Natalia" picks "Sole trader or other type of business" option
    Then "Natalia" should see following sections
      | sections                |
      | Select type of business |

    When "Natalia" selects "<business type>" from "Select type" dropdown
    And "Natalia" submits the form
    Then "Natalia" should be on the "Profile - Enter your email and set a password" page
    And "Natalia" should see following sections
      | sections               |
      | Registration form      |
      | Enrolment progress bar |

    Examples:
      | business type       |
      | Sole trader         |
      | Overseas Company    |
      | other options ????? |


  @wip
  @TT-1119
  @foreign-business
  Scenario: Only UK business can create a great.gov.uk account
    Given "Mirko" is on the "Profile - Select your business type" page

    When "Mirko" picks "Company not registered in the UK" option
    Then "Mirko" should not see following sections
      | sections               |
      | Enrolment progress bar |

    When "Mirko" submits the form
    Then "Mirko" should be on the "Profile - You cannot create an account" page
    And "Mirko" should see following sections
      | sections               |
      | Explanation            |
      | Links to other sites   |


  @wip
  @TT-1120
  @ltd-plc-royal
  @sole-trader-other-business
  @tax-payer
  Scenario Outline: "<selected business type>" representative should receive an email with confirmation code
    Given "Natalia" opted to register for a great.gov.uk account as "<selected business type>"
    And "Natalia" is on the "Profile - Enter your email and set a password" page

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Enter your confirmation code" page
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
  @TT-1121
  @ltd-plc-royal
  @sole-trader-other-business
  Scenario Outline: A representative of a "<selected business type>" company should be asked to enter their business details after providing email confirmation code
    Given "Natalia" has received the email confirmation code by opting to register as "<selected business type>"
    And "Natalia" is on the "Profile - Enter your confirmation code" page

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Enter your business details (for <selected business type>)" page
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
  @TT-1122
  @uk-taxpayer
  Scenario: A UK taxpayers wanting to register should be asked to enter their details after providing email confirmation code
    Given "Natalia" has received the email confirmation code by opting to register as "UK taxpayer"
    And "Natalia" is on the "Profile - Enter your confirmation code" page

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Enter your details (for UK taxpayer)" page
    And "Natalia" should see following sections
      | sections               |
      | Your business type     |
      | Enter your details     |
      | Enrolment progress bar |



  @wip
  @TT-1123
  @ltd-plc-royal
  @sole-trader-other-business
  Scenario Outline: A representative of a "<selected business type>" company should be asked to enter their details after providing business details
    Given "Natalia" has received the email confirmation code by opting to register as "<selected business type>"
    And "Natalia" is on the "Profile - Enter your business details (for <selected business type>)" page

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Enter your details (for <selected business type>)" page
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
  @TT-1124
  @ltd-plc-royal
  @sole-trader-other-business
  @uk-taxpayer
  Scenario Outline: A representative of a "<selected business type>" company should receive a confirmation email when a great.gov.uk account is created
    Given "Natalia" got to the "Profile - Enter your details (for <selected business type>)" by opting to register as "<selected business type>"

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
  @TT-1125
  @TT-1017
  Scenario: When CH record doesn't include business' address the business representative should be referred to a contact page
    Given "Natalia" has received the email confirmation code by opting to register as "<selected business type>"
    And "Natalia" is on the "Profile - Enter your confirmation code" page

    When "Natalia" decides to use "I cannot find my business name" link

    Then "Natalia" should be on the "Export Readiness - I cannot find my business name - Dedicated Support Content" page


  @wip
  @TT-1126
  @TT-1031
  Scenario: Companies House company enrolment creates a business profile
    Given "Natalia" has created a great.gov.uk account for a "LTD, PLC or Royal Charter"

    When "Natalia" goes to the "FAB - Edit Company Profile" page

    Then "Natalia" should be on the "FAB - Edit Company Profile" page


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

    Then "Natalia" should be on the "FAB - Edit Company Profile" page

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
    Then "Natalia" should be on the "Profile - Enter your business details (for <selected business type>)" page

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

    Then "Natalia" should be on the "Profile - Enter your business details (for <selected business type>)" page
    And "Natalia" should be logged in

    Examples:
      | selected business type                |
      | LTD, PLC or Royal Charter             |
      | Sole trader or other type of business |
