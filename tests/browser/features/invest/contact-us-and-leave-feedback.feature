@contact-us
Feature: Contact us and Leave feedback

  Background:
    Given basic authentication is done for "Invest - Home" page

  @CMS-237
  @contact-us
  @dev-only
  @captcha
  @header
  @footer
  Scenario Outline: An email should be sent after visitor submits the contact-us form
    Given "Robert" visits the "Invest - <selected>" page
    And "Robert" decided to "Get in touch"
    And "Robert" is on the "Invest - Contact us" page

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Invest - Thank you for your message" page
    And "Robert" should receive a contact confirmation email from "no-reply@mailgun.directory.uktrade.io"
    And Invest mailbox admin should also receive a contact confirmation email from "no-reply@mailgun.directory.uktrade.io"

    Examples: Various pages
      | selected                          |
      | Home                              |
