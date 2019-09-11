@international-page
@contact-us
Feature: INTL - Brexit help - Contact us

  Background:
    Given basic authentication is done for "International - Landing" page

  @TT-617
  @brexit
  @dev-only
  Scenario: International Visitors should see all expected page sections on "International Brexit help - Contact Us form" page
    Given "Robert" visits the "International - Brexit help - Contact Us" page

    Then "Robert" should see following sections
      | sections        |
      | header          |
      | heading         |
      | form            |
      | error reporting |
    And "Robert" should not see following section
      | section           |
      | language selector |
      | not translated    |


  # Missing translations
  @wip
  @TT-617
  @brexit
  @dev-only
  Scenario Outline: International Visitors should not be able view "International Brexit help - Contact Us form" in "<preferred_language>"
    Given "Robert" visits the "International - Brexit help - Contact Us" page

    When "Robert" manually change the page language to "<preferred_language>"

    Then "Robert" should see following sections
      | sections        |
      | not translated  |

    Examples: languages
      | preferred_language |
      | zh-hans            |
      | de                 |
      | ja                 |
      | es                 |
      | pt                 |
      | ar                 |


  @TT-617
  @dev-only
  @captcha
  @brexit
  @dev-only
  Scenario: International Visitors should be able to submit their questions regarding EU Exit
    Given "Robert" visits the "International - Brexit help - Contact Us" page

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "International - Brexit help - Thank you for contacting us" page
    And "Robert" should receive an "Thank you for your EU exit enquiry" confirmation email
