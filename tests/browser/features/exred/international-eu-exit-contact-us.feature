@international-page
@contact-us
Feature: International Page - EU Exit - Contact us

  Background:
    Given hawk cookie is set on "Export Readiness - Home" page

  @TT-617
  @eu-exit
  Scenario: International Visitors should see all expected page sections on "International EU Exit - Contact Us form" page
    Given "Robert" visits the "Export Readiness - International EU Exit - Contact Us" page

    Then "Robert" should see following sections
      | sections        |
      | header bar      |
      | header menu     |
      | heading         |
      | form            |
      | error reporting |
    And "Robert" should not see following section
      | section           |
      | language selector |
      | not translated    |


  @TT-617
  @eu-exit
  Scenario Outline: International Visitors should not be able view "International EU Exit - Contact Us form" in "<preferred_language>"
    Given "Robert" visits the "Export Readiness - International EU Exit - Contact Us" page

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
  @eu-exit
  Scenario: International Visitors should be able to submit their questions regarding EU Exit
    Given "Robert" visits the "Export Readiness - International EU Exit - Contact Us" page

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Export Readiness - International EU Exit - Thank you for contacting us" page
    And "Robert" should receive an "Thank you for your EU exit enquiry" confirmation email
