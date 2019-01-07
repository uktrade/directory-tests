@TT-833
Feature: New Contact-us form


  @wip
  @TT-833
  @exopps
  @captcha
  @dev-only
  @soo-long-domestic
  @account-support
  Scenario: Domestic "Selling Online Overseas" Enquirers should be able to contact us
    Given "Robert" got to the "Selling Online Overseas - Long Domestic (Your Business)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Selling Online Overseas - Long Domestic (Organisation details)" page
    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Selling Online Overseas - Long Domestic (Your experience)" page
    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Selling Online Overseas - Long Domestic (Contact details)" page
    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Selling Online Overseas - Long Domestic (Thank you for your enquiry)" page
    And "Robert" should receive a "great.gov.uk Selling Online Overseas contact form" confirmation email from Zendesk


