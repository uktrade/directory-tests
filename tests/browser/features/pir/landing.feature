@pir
@no-sso-email-verification-required
Feature: PIR - Landing page

  Background:
    Given basic authentication is done for "Domestic - Home" page

  Scenario: Buyers should be able to view "PIR - Landing" page
    Given "Robert" visits the "PIR - Landing" page

    Then "Robert" should see following sections
      | Sections |
      | Header   |
      | Hero     |
      | Form     |
      | Footer   |


  @contact-us
  @dev-only
  @captcha
  @<value>
  Scenario Outline: Buyers should be able to request a Perfect Fit Prospectus
    Given "Robert" visits the "PIR - Landing" page

    When "Robert" fills out and submits the form
      | field  | value   |
      | sector | <value> |

    Then "Robert" should be on the "International - Thank you for requesting the Perfect Fit Prospectus" page
    And "Robert" should receive "The UK for your business – your tailored Perfect Fit Prospectus" confirmation email from "PIR"

    Examples: sector
      | value              |
      | tech               |
      | automotive         |
      | creative-services  |
      | financial-services |
      | life-sciences      |
      | renewable-energy   |


  @contact-us
  @dev-only
  @captcha
  Scenario: Buyers should be able to request a Perfect Fit Prospectus
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
