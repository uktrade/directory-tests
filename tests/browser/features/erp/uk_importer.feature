@erp
@uk_business
Feature: ERP - UK business


  @TT-2077
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to tell where do they import goods from
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - <expected>" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Save for later  |
      | Footer          |

    Examples:
      | imported or not | business_type | expected                               |
      | imported        | UK importer   | Where do you import from (UK importer) |
