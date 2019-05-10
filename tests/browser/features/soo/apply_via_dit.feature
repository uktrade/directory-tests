Feature: Apply via DIT

  Background:
    Given basic authentication is done for "Selling Online Overseas - Home" page
    And basic authentication is done for "Export Readiness - Home" page


  @XOT-689
  @exopps
  @captcha
  @dev-only
  @soo-long-domestic
  @account-support
  Scenario Outline: Anonymous Enquirers should be redirected to SSO login page
    Given "Robert" found a marketplace in "<country>" to sell "<products>"

    When "Robert" decides to "Apply now via DIT"

    Then "Robert" should be on the "Single Sign-On - Sign in" page

    Examples: products and countries
      | country   | products               |
      | Australia | Clothing & Accessories |


  @XOT-740
  @exopps
  @captcha
  @dev-only
  @soo-long-domestic
  @account-support
  Scenario Outline: Logged in Domestic "Selling Online Overseas" Enquirers should be able to get the Enquiry page
    Given "Robert" has a verified standalone SSO/great.gov.uk account
    And "Robert" is signed in
    And "Robert" found a marketplace in "<country>" to sell "<products>"

    When "Robert" decides to "Apply now via DIT"

    Then "Robert" should be on the "Export Readiness - Long Domestic (Your Business)" page

    Examples: products and countries
      | country   | products               |
      | Australia | Clothing & Accessories |


  @XOT-749
  @exopps
  @captcha
  @dev-only
  @soo-long-domestic
  @account-support
  Scenario Outline: Logged in Domestic "Selling Online Overseas" Enquirers should be able to fill the Enquiry page
    Given "Robert" has a verified standalone SSO/great.gov.uk account
    And "Robert" is signed in
    And "Robert" found a marketplace in "<country>" to sell "<products>"

    When "Robert" decides to "Apply now via DIT"

    Then "Robert" should be on the "Export Readiness - Long Domestic (Your Business)" page

    When "Robert" submits the SOO contact-us form
      | field                         | value   |
      | I don't have a company number | checked |

    Then "Robert" should be on the "Export Readiness - Long Domestic (Thank you for your enquiry)" page

    Examples: products and countries
      | country   | products               |
      | Australia | Clothing & Accessories |


  @XOT-741
  @exopps
  @captcha
  @dev-only
  @soo-long-domestic
  @account-support
  Scenario Outline: Logged in Domestic "Selling Online Overseas" Enquirers with a Business profile should be able to get pre-populated Enquiry page
    Given "Robert" has created a great.gov.uk account for a "LTD, PLC or Royal Charter"
    And "Robert" found a marketplace in "<country>" to sell "<products>"

    When "Robert" decides to "Apply now via DIT"

    Then "Robert" should be on the "Export Readiness - Long Domestic (Your Business)" page
    And "Robert" should see form fields populated with his company details

    Examples: products and countries
      | country   | products               |
      | Australia | Clothing & Accessories |


  @XOT-689
  @zendesk
  @exopps
  @captcha
  @dev-only
  @soo-long-domestic
  @account-support
  Scenario Outline: Logged in Domestic "Selling Online Overseas" Enquirers should receive a enquiry confirmation email after submitting the contact us form
    Given "Robert" has a verified standalone SSO/great.gov.uk account
    And "Robert" is signed in
    And "Robert" applied via DIT to contact randomly selected marketplace in "<country>" to sell "<products>"

    When "Robert" submits the SOO contact-us form
      | field                         | value   |
      | I don't have a company number | checked |

    Then "Robert" should receive a "great.gov.uk Selling Online Overseas contact form" confirmation email from Zendesk

    Examples: products and countries
      | country   | products               |
      | Australia | Clothing & Accessories |