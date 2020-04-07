@allure.link:TT-1033
@allure.link:TT-1094
@enrol
@new-registration
@allure.suite:Profile
Feature: Profile - CH enrolment flows

  Background:
    Given test authentication is done


  @allure.link:TT-1115
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


  @allure.link:TT-1117
  @ltd-plc-royal
  Scenario Outline: "<business type>" representative should be asked to enter their email and set a password after selecting their business type
    Given "Natalia" visits the "Profile - Enter your email address and set a password (<business type>)" page

    Then "Natalia" should see following sections
      | sections               |
      | Breadcrumbs            |
      | Registration form      |
      | Enrolment progress bar |

    Examples:
      | business type             |
      | LTD, PLC or Royal Charter |


  @dev-only
  @allure.link:TT-1120
  @ltd-plc-royal
  Scenario Outline: "<business type>" representative should receive an email with confirmation code
    Given "Natalia" visits the "Profile - Enter your email address and set a password (<business type>)" page

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Enter your confirmation code (<business type>)" page
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
  @allure.link:TT-2176
  @allure.link:TT-2193
  @password
  @ltd-plc-royal
  Scenario Outline: "<business type>" representative shouldn't be able to use a password that doesn't meet requirements otherwise their going to see "<an error message>"
    Given "Natalia" visits the "Profile - Enter your email address and set a password (<business type>)" page

    When "Natalia" fills out and submits the form
      | field            | value              |
      | password         | <password>         |
      | confirm password | <confirm password> |

    Then "Natalia" should be on the "Profile - Enter your email address and set a password (<business type>)" page
    And "Natalia" should see "<an error message>" on the page

    Examples:
      | business type             | password    | confirm password | an error message                                                   |
      | LTD, PLC or Royal Charter | letters     | letters          | This password contains letters only                                |
      | LTD, PLC or Royal Charter | abcdefghij  | abcdefghij       | This password contains letters only                                |
      | LTD, PLC or Royal Charter | abcdefghijk | abcdefghijk      | This password contains letters only                                |
      | LTD, PLC or Royal Charter | 0123456789  | 0123456789       | This password is entirely numeric                                  |
      | LTD, PLC or Royal Charter | password    | don't match      | Passwords don't match                                              |
      | LTD, PLC or Royal Charter | password    | empty            | This field is required                                             |
      | LTD, PLC or Royal Charter | empty       | empty            | This field is required                                             |
      | LTD, PLC or Royal Charter | password    | password         | This password contains the word 'password'                         |
      | LTD, PLC or Royal Charter | 123 short   | 123 short        | This password is too short. It must contain at least 10 characters |
      | LTD, PLC or Royal Charter | empty       | password         | This field is required                                             |


  @bug
  @allure.issue:TT-2192
  @fixed
  @dev-only
  @ltd-plc-royal
  Scenario Outline: "<selected business type>" representative should be able to use spaces in password
    Given "Natalia" visits the "Profile - Enter your email address and set a password (<selected business type>)" page

    When "Natalia" fills out and submits the form
      | field            | value      |
      | password         | <password> |
      | confirm password | <password> |

    Then "Natalia" should be on the "Profile - Enter your confirmation code (<selected business type>)" page

    Examples: examples affected by bug TT-2192
      | selected business type    | password    |
      | LTD, PLC or Royal Charter | a b c d e f |
      | LTD, PLC or Royal Charter | 1 2 3 4 5 6 |


  @dev-only
  @allure.link:TT-1121
  @ltd-plc-royal
  Scenario Outline: A representative of a "<selected business type>" company should be asked to enter their business details after providing email confirmation code
    Given "Natalia" has received the email confirmation code by opting to register as "<selected business type>"
    And "Natalia" is on the "Profile - Enter your confirmation code (<selected business type>)" page

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
  @allure.link:TT-1123
  @ltd-plc-royal
  Scenario Outline: A representative of a "<selected business type>" company should be asked to enter their details after providing business details
    Given "Natalia" has received the email confirmation code by opting to register as "<selected business type>"
    And "Natalia" is on the "Profile - Enter your confirmation code (<selected business type>)" page

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
  @allure.link:TT-1124
  @ltd-plc-royal
  Scenario Outline: A representative of a "<selected business type>" company should be told when account is created and the are the next possible steps
    Given "Natalia" has received the email confirmation code by opting to register as "<selected business type>"
    And "Natalia" is on the "Profile - Enter your confirmation code (<selected business type>)" page

    When "Natalia" fills out and submits the form
    Then "Natalia" should be on the "Profile - Enter your business details (<selected business type>)" page

    When "Natalia" fills out and submits the form (and go 1 page back on error)
    Then "Natalia" should be on the "Profile - Enter your business details [step 2] (<selected business type>)" page

    When "Natalia" fills out and submits the form
    Then "Natalia" should be on the "Profile - Enter your details (<selected business type>)" page

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Account created (<selected business type>)" page
    And "Natalia" should see following sections
      | sections                   |
      | Confirmation email message |
      | Next steps                 |

    Examples:
      | selected business type     |
      | LTD, PLC or Royal Charter  |


  @dev-only
  @allure.link:TT-1126
  @allure.link:TT-1031
  @ltd-plc-royal
  Scenario: Companies House company enrolment creates a business profile
    Given "Natalia" has created a great.gov.uk account for a "LTD, PLC or Royal Charter"

    When "Natalia" goes to the "Profile - Edit Company Profile" page

    Then "Natalia" should be on the "Profile - Edit Company Profile" page


  @dev-only
  @verification-code
  @ltd-plc-royal
  Scenario: Users should be able to resend email verification code
    Given "Natalia" has received the email confirmation code by opting to register as "LTD, PLC or Royal Charter"
    And "Natalia" is on the "Profile - Enter your confirmation code (LTD, PLC or Royal Charter)" page

    When "Natalia" decides to use "Resend my code" link
    Then "Natalia" should be on the "Domestic - I have not received a verification code - Dedicated Support Content" page

    When "Natalia" decides to use "Resend my code" link
    Then "Natalia" should be on the "Profile - Resend your verification code" page

    When "Natalia" fills out and submits the form
    Then "Natalia" should be on the "Profile - Re-enter your confirmation code" page
    And "Natalia" should receive email with a new confirmation code

    When "Natalia" fills out and submits the form
    Then "Natalia" should be on the "Profile - Enter your business details (LTD, PLC or Royal Charter)" page


  @dev-only
  @allure.link:TT-1125
  @allure.link:TT-1017
  @ltd-plc-royal
  Scenario Outline: When CH record doesn't include business' address the business representative should be referred to a contact page
    Given "Natalia" has received the email confirmation code by opting to register as "<selected business type>"
    And "Natalia" filled out and submitted the form
    And "Natalia" got to the "Profile - Enter your business details (<selected business type>)" page

    When "Natalia" decides to use "I cannot find my business name" link
    And "Natalia" decides to "contact us"

    Then "Natalia" should be on the "Domestic - Short contact form (Tell us how we can help)" page

    Examples:
      | selected business type                |
      | LTD, PLC or Royal Charter             |


  # this scenario uses deprecated form of registration via SSO signup page
  @dev-only
  @legacy-sso-registration
  @allure.link:TT-1127
  @allure.link:TT-1035
  @ltd-plc-royal
  @sole-trader-other-business
  @uk-taxpayer
  Scenario Outline: User representing "<selected business type>" should be notified by email when there is an account already registered to their email address (legacy SSO registration)
    Given "Natalia" has a verified standalone SSO/great.gov.uk account
    And "Natalia" decided to create a great.gov.uk account as "<selected business type>"

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Enter your confirmation code (<selected business type>)" page
    And "Natalia" should receive "Sign in to great.gov.uk services" email containing "There is an account already registered to this email address" message

    Examples:
      | selected business type                |
      | LTD, PLC or Royal Charter             |
      | Sole trader or other type of business |
      | UK taxpayer                           |


  @dev-only
  @allure.link:TT-1127
  @allure.link:TT-1035
  @ltd-plc-royal
  @sole-trader-other-business
  @uk-taxpayer
  Scenario Outline: User representing "<selected business type>" should be notified by email when there is an account already registered to their email address
    Given "Natalia" has received the email confirmation code by opting to register as "<selected business type>"
    And "Natalia" quickly signed out
    And "Natalia" went to the "Profile - Enter your email address and set a password (<selected business type>)" page

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Enter your confirmation code (<selected business type>)" page
    And "Natalia" should receive "Sign in to great.gov.uk services" email containing "There is an account already registered to this email address" message

    Examples:
      | selected business type                |
      | LTD, PLC or Royal Charter             |
      | Sole trader or other type of business |
      | UK taxpayer                           |


  @captcha
  @dev-only
  @allure.link:TT-1128
  @allure.link:TT-1036
  @ltd-plc-royal
  Scenario: A logged-in user representing "LTD, PLC or Royal Charter" company should not be able to access SSO Sign in or Create an account pages
    Given "Natalia" has created a great.gov.uk account for a "LTD, PLC or Royal Charter"

    When "Natalia" goes to the "SSO - Sign in" page
    Then "Natalia" should be on the "Profile - About" page

    When "Natalia" goes to the "Profile - Create an account" page
    Then "Natalia" should be on the "Profile - Edit Company Profile" page


  @dev-only
  @allure.link:TT-1129
  @allure.link:TT-1036
  @ltd-plc-royal
  @sole-trader-other-business
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


  @dev-only
  @allure.link:TT-1130
  @allure.link:TT-1037
  @ltd-plc-royal
  @sole-trader-other-business
  Scenario Outline: Log user in on verification submit, not on account creation for "<selected business type>"
    Given "Natalia" has received the email confirmation code by opting to register as "<selected business type>"
    And "Natalia" is on the "Profile - Enter your confirmation code (<selected business type>)" page

    When "Natalia" fills out and submits the form

    Then "Natalia" should be on the "Profile - Enter your business details (<selected business type>)" page
    And "Natalia" should see that she can "Sign out"

    Examples:
      | selected business type                |
      | LTD, PLC or Royal Charter             |
      | Sole trader or other type of business |


  @bug
  @allure.issue:TT-1281
  @fixed
  @captcha
  @dev-only
  @ltd-plc-royal
  @sole-trader-other-business
  @uk-taxpayer
  Scenario Outline: Newly registered users should see "<expected business type>" business type on their "Profile - Business profile" page
    Given "Natalia" has created a great.gov.uk account for a "<selected business type>"

    When "Natalia" goes to the "Profile - Edit Company Profile" page

    Then "Natalia" should see "<expected business type>" on the page

    Examples: business types
      | selected business type                | expected business type                        |
      | LTD, PLC or Royal Charter             | UK business registered in Companies House     |
      | Sole trader or other type of business | UK business not registered in Companies House |
      | UK taxpayer                           | Get a business profile                        |
