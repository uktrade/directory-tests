Feature: New Contact-us form
  @XOT-631
  @exopps
  @captcha
  @dev-only
  @soo-long-domestic
  @account-support
  Scenario: Domestic "Selling Online Overseas" Enquirers should be able to contact us
    Given "Robert" visits the "Selling Online Overseas - Home" page
    When "Robert" decides to "Start your search now"
    Then "Robert" should be on the "Selling Online Overseas - Search results" page
    When "Robert" randomly selects a marketplace
    Then "Robert" should be on the "Selling Online Overseas - Marketplace" page
    When "Robert" decides to "Apply now via DIT"
    Then "Robert" should be on the "Export Readiness - Long Domestic (Your Business)" page
    When "Robert" fills out and submits the form
      | field                         | value     |
      | I don't have a company number | unchecked |
    Then "Robert" should be on the "Export Readiness - Long Domestic (Organisation details)" page
    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Export Readiness - Long Domestic (Your experience)" page
    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Export Readiness - Long Domestic (Contact details)" page
    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Export Readiness - Long Domestic (Thank you for your enquiry)" page
    And "Robert" should receive a "great.gov.uk Selling Online Overseas contact form" confirmation email from Zendesk


  @XOT-632
  @exopps
  @captcha
  @dev-only
  @soo-long-domestic
  @account-support
  Scenario Outline: Domestic "Selling Online Overseas" Enquirers should be able to contact us for
    Given "Robert" visits the "Selling Online Overseas - Home" page
    When "Robert" decides to "Start your search now"
    Then "Robert" should be on the "Selling Online Overseas - Search results" page
    When "Robert" decides to find marketplaces in "<country name>" to sell "<product type>"
    Then "Robert" should see the expected markets in "<country name>"
    Examples: product type and country name
      | product type  | country name              |
      | Shoes,Clothes | United States,China,India |
    When "Robert" randomly selects a marketplace
    Then "Robert" should be on the "Selling Online Overseas - Marketplace" page
    When "Robert" decides to "Apply now via DIT"
    Then "Robert" should be on the "Export Readiness - Long Domestic (Your Business)" page
    When "Robert" fills out and submits the form
      | field                         | value     |
      | I don't have a company number | unchecked |
    Then "Robert" should be on the "Export Readiness - Long Domestic (Organisation details)" page
    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Export Readiness - Long Domestic (Your experience)" page
    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Export Readiness - Long Domestic (Contact details)" page
    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Export Readiness - Long Domestic (Thank you for your enquiry)" page
    And "Robert" should receive a "great.gov.uk Selling Online Overseas contact form" confirmation email from Zendesk


  @TT-833
  @exopps
  @captcha
  @dev-only
  @soo-long-domestic
  @account-support
  Scenario: Domestic "Selling Online Overseas" Enquirers should be able to contact us
    Given "Robert" visits the "Selling Online Overseas - Long Domestic (Your Business)" page

    When "Robert" fills out and submits the form
      | field                         | value     |
      | I don't have a company number | unchecked |
    Then "Robert" should be on the "Selling Online Overseas - Long Domestic (Organisation details)" page
    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Selling Online Overseas - Long Domestic (Your experience)" page
    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Selling Online Overseas - Long Domestic (Contact details)" page
    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Selling Online Overseas - Long Domestic (Thank you for your enquiry)" page
    And "Robert" should receive a "great.gov.uk Selling Online Overseas contact form" confirmation email from Zendesk


  @TT-833
  @exopps
  @captcha
  @dev-only
  @soo-long-domestic
  @account-support
  Scenario: Domestic "Selling Online Overseas" Enquirers should be able to contact us even if they're not registered with Companies House
    Given "Robert" visits the "Selling Online Overseas - Long Domestic (Your Business)" page

    When "Robert" fills out and submits the form
      | field                         | value   |
      | I don't have a company number | checked |
    Then "Robert" should be on the "Selling Online Overseas - Long Domestic (Organisation details)" page
    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Selling Online Overseas - Long Domestic (Your experience)" page
    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Selling Online Overseas - Long Domestic (Contact details)" page
    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Selling Online Overseas - Long Domestic (Thank you for your enquiry)" page
    And "Robert" should receive a "great.gov.uk Selling Online Overseas contact form" confirmation email from Zendesk
