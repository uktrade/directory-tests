@allure.link:TT-1033
@allure.link:TT-1094
@enrol
@new-registration
@allure.suite:Profile
Feature: Profile - Non-CH enrolment flows

  Background:
    Given test authentication is done


  @allure.link:TT-1118
  @sole-trader-other-business
  Scenario: "Sole trader" representative should be asked to specify the type of their business before being asked to enter their email and set a password
    Given "Natalia" visits the "Profile - Select your business type" page

    When "Natalia" chooses "Sole trader or other type of business" option

    Then "Natalia" should be on the "Profile - Enter your email address and set a password (Sole trader or other type of business)" page
    And "Natalia" should see following sections
      | sections               |
      | Registration form      |
      | Enrolment progress bar |


  @allure.link:TT-1119
  @uk-taxpayer
  Scenario: UK taxpayers can create an SSO account
    Given "Mirko" visits the "Profile - Select your business type" page

    When "Mirko" chooses "UK taxpayer" option

    Then "Mirko" should be on the "Profile - Enter your email address and set a password (UK taxpayer)" page
    And "Mirko" should see following sections
      | sections               |
      | Registration form      |
      | Enrolment progress bar |


  @allure.link:TT-1119
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
  @allure.link:TT-1120
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
  @allure.link:TT-2176
  @allure.link:TT-2193
  @password
  @sole-trader-other-business
  @tax-payer
  Scenario Outline: "<business type>" representative shouldn't be able to use a password ("<password>" & "<confirm password>") that doesn't meet requirements otherwise their going to see "<an error message>"
    Given "Natalia" visits the "Profile - Enter your email address and set a password (<business type>)" page

    When "Natalia" fills out and submits the form
      | field            | value              |
      | password         | <password>         |
      | confirm password | <confirm password> |

    Then "Natalia" should be on the "Profile - Enter your email address and set a password (<business type>)" page
    And "Natalia" should see "<an error message>" on the page

    Examples:
      | business type                         | password    | confirm password | an error message                                                   |
      | Sole trader or other type of business | letters     | letters          | This password contains letters only                                |
      | Sole trader or other type of business | abcdefghij  | abcdefghij       | This password contains letters only                                |
      | Sole trader or other type of business | abcdefghijk | abcdefghijk      | This password contains letters only                                |
      | Sole trader or other type of business | 0123456789  | 0123456789       | This password is entirely numeric                                  |
      | Sole trader or other type of business | password    | don't match      | Passwords don't match                                              |
      | Sole trader or other type of business | password    | empty            | This field is required                                             |
      | Sole trader or other type of business | empty       | empty            | This field is required                                             |
      | Sole trader or other type of business | empty       | password         | This field is required                                            |
      | Sole trader or other type of business | password    | password         | This password contains the word 'password'                         |
      | Sole trader or other type of business | 123 short   | 123 short        | This password is too short. It must contain at least 10 characters |
      | UK taxpayer                           | letters     | letters          | This password contains letters only                                |
      | UK taxpayer                           | abcdefghij  | abcdefghij       | This password contains letters only                                |
      | UK taxpayer                           | abcdefghijk | abcdefghijk      | This password contains letters only                                |
      | UK taxpayer                           | 0123456789  | 0123456789       | This password is entirely numeric                                  |
      | UK taxpayer                           | password    | don't match      | Passwords don't match                                              |
      | UK taxpayer                           | password    | empty            | This field is required                                             |
      | UK taxpayer                           | empty       | empty            | This field is required                                             |
      | UK taxpayer                           | empty       | password         | This field is required                                            |
      | UK taxpayer                           | password    | password         | This password contains the word 'password'                         |
      | UK taxpayer                           | 123 short   | 123 short        | This password is too short. It must contain at least 10 characters |


  @bug
  @allure.issue:TT-2192
  @fixed
  @dev-only
  @sole-trader-other-business
  @tax-payer
  Scenario Outline: "<selected business type>" representative should be able to use spaces in password
    Given "Natalia" visits the "Profile - Enter your email address and set a password (<selected business type>)" page

    When "Natalia" fills out and submits the form
      | field            | value      |
      | password         | <password> |
      | confirm password | <password> |

    Then "Natalia" should be on the "Profile - Enter your confirmation code (<selected business type>)" page

    Examples: examples affected by bug
      | selected business type                | password    |
      | Sole trader or other type of business | a b c d e f |
      | UK taxpayer                           | 1 2 3 4 5 6 |


  @dev-only
  @allure.link:TT-1121
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
      | Sole trader or other type of business |


  @dev-only
  @allure.link:TT-1122
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
  @allure.link:TT-1123
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
      | Sole trader or other type of business |


  @captcha
  @dev-only
  @allure.link:TT-1128
  @allure.link:TT-1036
  @sole-trader-other-business
  Scenario: A logged-in user representing "Sole trader or other type of business" should not be able to access SSO Sign in or Create an account pages
    Given "Natalia" has created a great.gov.uk account for a "Sole trader or other type of business"

    When "Natalia" goes to the "SSO - Sign in" page
    Then "Natalia" should be on the "Profile - About" page

    When "Natalia" goes to the "Profile - Create an account" page
    Then "Natalia" should be on the "Profile - Edit Company Profile" page


  @captcha
  @dev-only
  @allure.link:TT-1128
  @allure.link:TT-1036
  @uk-taxpayer
  Scenario: A logged-in user representing "UK taxpayer" should not be able to access SSO Sign in or Create an account pages
    Given "Natalia" has created a great.gov.uk account for a "UK taxpayer"

    When "Natalia" goes to the "SSO - Sign in" page
    Then "Natalia" should be on the "Profile - About" page

    When "Natalia" goes to the "Profile - Create an account" page
    Then "Natalia" should be on the "Profile - Create an account" page


  @allure.link:TT-1560
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
