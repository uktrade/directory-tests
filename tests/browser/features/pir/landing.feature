@pir
@no-sso-email-verification-required
@allure.suite:PIR
Feature: PIR - Landing page

  Background:
    Given test authentication is done


  Scenario: Buyers should be able to view "PIR - Landing" page
    Given "Robert" visits the "PIR - Landing" page

    Then "Robert" should see following sections
      | Sections |
      | Header   |
      | Hero     |
      | Form     |
      | Footer   |


  @skip-in-firefox
  @contact-us
  @dev-only
  @captcha
  @<value>
  Scenario Outline: Buyers should be able to request a Perfect Fit Prospectus for "<sector>" sector
    Given "Robert" visits the "PIR - Landing" page

    When "Robert" fills out and submits the form
      | field  | value    |
      | sector | <sector> |

    Then "Robert" should be on the "International - Thank you for requesting the Perfect Fit Prospectus" page
    And "Robert" should receive "The UK for your business – your tailored Perfect Fit Prospectus" confirmation email from "PIR"

    Examples: sector
      | sector             |
      | tech               |
      | automotive         |
      | creative-services  |
      | financial-services |
      | life-sciences      |
      | renewable-energy   |


  @skip-in-firefox
  @contact-us
  @dev-only
  @captcha
  Scenario: Buyers should be able to request a Perfect Fit Prospectus without specifying specific sector
    Given "Robert" visits the "PIR - Landing" page

    When "Robert" fills out and submits the form
      | field  | value |
      | sector | other |

    Then "Robert" should be on the "International - Thank you for requesting the Perfect Fit Prospectus" page
    And "Robert" should receive "The UK for your business – your prospectus" confirmation email from "PIR"
    And "Robert" should see following sections
      | sections          |
      | Header            |
      | Breadcrumbs       |
      | Thank you message |
      | Error reporting   |
      | Footer            |
