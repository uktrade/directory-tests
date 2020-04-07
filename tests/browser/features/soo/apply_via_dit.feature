@allure.suite:SOO
Feature: SOO - Apply via DIT

  Background:
    Given test authentication is done


  @allure.link:XOT-689
  @exopps
  @captcha
  @dev-only
  @soo-long-domestic
  @account-support
  @read-only
  Scenario Outline: Anonymous Enquirers should be redirected to SSO login page
    Given "Robert" found a marketplace in "<country>" to sell "<products>"

    When "Robert" decides to "Apply now"

    Then "Robert" should be on the "SSO - Sign in" page

    Examples: products and countries
      | country   | products                 |
      | Australia | Clothing and accessories |


  @allure.link:XOT-740
  @exopps
  @captcha
  @dev-only
  @soo-long-domestic
  @account-support
  Scenario Outline: Logged in Domestic "Selling Online Overseas" Enquirers should be able to get the Enquiry page
    Given "Robert" has created a great.gov.uk account for a "UK taxpayer"
    And "Robert" found a marketplace in "<country>" to sell "<products>"

    When "Robert" decides to "Apply now"

    Then "Robert" should be on the "Domestic - Contact details (SOO)" page
    And "Robert" should see following fields populated with values provided on other forms
      | form                                                                       | fields |
      | Profile - Enter your email address and set a password (UK taxpayer) - form | email  |

    Examples: products and countries
      | country   | products                 |
      | Australia | Clothing and accessories |


  @allure.link:XOT-689
  @allure.link:XOT-741
  @exopps
  @captcha
  @dev-only
  @soo-long-domestic
  @account-support
  Scenario Outline: Enquirers representing a "LTD, PLC or Royal Charter" organisation should see SOO contact form pre-populated with their details
    Given "Robert" has created a great.gov.uk account for a "LTD, PLC or Royal Charter"
    And "Robert" found a marketplace in "<country>" to sell "<products>"

    When "Robert" decides to "Apply now"
    Then "Robert" should be on the "Domestic - Contact details (SOO)" page
    And "Robert" should see following fields populated with values provided on other forms
      | form                                                                              | fields                |
      | Profile - Enter your email address and set a password (LTD, PLC or Royal Charter) | email                 |
      | Profile - Enter your details (LTD, PLC or Royal Charter)                          | first name, last name |

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Domestic - About your business (SOO)" page
    And "Robert" should see following fields populated with values provided on other forms
      | form                                           | fields                                                 |
      | Profile - Enter your business details [step 2] | company name, company number, company website, address |

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Domestic - About your products (SOO)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Domestic - Your experience (SOO)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Domestic - Thank you for your enquiry (SOO)" page

    Then a "zendesk" notification entitled "great.gov.uk Selling Online Overseas contact form" should be sent to "Robert"

    Examples: products and countries
      | country   | products                 |
      | Australia | Clothing and accessories |
