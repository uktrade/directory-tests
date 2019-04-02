Feature: New Contact-us form

  Background:
    Given basic authentication is done for "Selling Online Overseas - Home" page
    And basic authentication is done for "Export Readiness - Home" page


  @XOT-631
  @XOT-689
  @exopps
  @dev-only
  @soo-long-domestic
  @account-support
  Scenario Outline: Visitors should be able to search for marketplaces to sell "<products>" in "<countries>"
    Given "Robert" visits the "Selling Online Overseas - Home" page

    When "Robert" searches for marketplaces in "<countries>" to sell "<products>"

    Then "Robert" should be on the "Selling Online Overseas - Search results" page
    And "Robert" should see marketplaces which operate globally or in multiple countries "<countries>"

    Examples: products and countries
      | products      | countries                 |
      | Shoes,Clothes | United States,China,India |


  @XOT-689
  @exopps
  @captcha
  @dev-only
  @soo-long-domestic
  @account-support
  Scenario Outline: Domestic "Selling Online Overseas" Enquirers should be able to view marketplace page
    Given "Robert" searches for marketplaces in "<countries>" to sell "<products>"

    When "Robert" randomly selects a marketplace

    Then "Robert" should be on the "Selling Online Overseas - Marketplace" page

    Examples: products and countries
      | products      | countries                 |
      | Shoes,Clothes | United States,China,India |


  @XOT-689
  @exopps
  @captcha
  @dev-only
  @soo-long-domestic
  @account-support
  Scenario Outline: Anonymous Enquirers should be redirected to SSO login page
    Given "Robert" found a marketplace in "<countries>" to sell "<products>"

    When "Robert" decides to "Apply now via DIT"

    Then "Robert" should be on the "Single Sign-On - Sign in" page

    Examples: product type and country name
      | products      | countries                 |
      | Shoes,Clothes | United States,China,India |


  @XOT-689
  @exopps
  @captcha
  @dev-only
  @soo-long-domestic
  @account-support
  Scenario Outline: Domestic "Selling Online Overseas" Enquirers should receive a enquiry confirmation email after submitting the contact us form
    Given "Robert" applied via DIT to contact randomly selected marketplace in "<countries>" to sell "<products>"

    When "Robert" submits the SOO contact-us form
      | field                         | value   |
      | I don't have a company number | checked |

    Then "Robert" should receive a "great.gov.uk Selling Online Overseas contact form" confirmation email from Zendesk

    Examples: products and countries
      | products      | countries                 |
      | Shoes,Clothes | United States,China,India |