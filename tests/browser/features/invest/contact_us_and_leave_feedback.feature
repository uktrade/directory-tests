@contact-us
@allure.suite:Invest
Feature: Invest - Contact us and Leave feedback

  Background:
    Given test authentication is done


  @allure.link:CMS-237
  @contact-us
  @dev-only
  @captcha
  @header
  @footer
  Scenario: An email should be sent after visitor submits the contact-us form
    Given "Robert" visits the "Invest - landing" page
    And "Robert" decided to "Get in touch"
    And "Robert" is on the "Invest - Contact us" page

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Invest - Thank you for your message" page
    And an "email" notification entitled "Contact form user email subject" should be sent to "Robert"
    And an email notification about "Robert"'s enquiry should be send to "Invest mailbox"
