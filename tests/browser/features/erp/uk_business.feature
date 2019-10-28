@erp
@uk_business
Feature: ERP - UK business


  @TT-2073
  Scenario: A UK business should be able to tell whether they're importing from overseas or not
    Given "Robert" visits the "ERP - User type" page

    When "Robert" says that he represents a "UK business"

    Then "Robert" should be on the "ERP - Import from overseas (UK business)" page
    And "Robert" should see following options
      | options |
      | Yes     |
      | No      |
    And "Robert" should see following sections
      | Sections |
      | Header   |
      | Beta bar |
      | Go back  |
      | Form     |
      | Footer   |


  @TT-2074
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should see a list of product codes which might be affected by Brexit
    Given "Robert" got to "ERP - Import from overseas (UK business)" from "ERP - User type" via "UK business"

    When "Robert" says that affected goods are "<imported or not>" from overseas

    Then "Robert" should be on the "ERP - <expected>" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Hierarchy codes |
      | Footer          |

    Examples:
      | imported or not | expected                     |
      | imported        | Product search (UK importer) |
      | not imported    | Product search (UK business) |


  @TT-2075
  @drill
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to select goods affected by Brexit
    Given "Robert" got to "ERP - Product search (<business type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes

    Then "Robert" should be on the "ERP - Product detail (<business type>)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Save for later  |
      | Footer          |

    Examples:
      | imported or not | business type |
      | imported        | UK importer   |
      | not imported    | UK business   |


  @TT-2076
  @drill
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to change the goods previously selected
    Given "Robert" got to "ERP - Product search (<business type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business type>)" page

    When "Robert" decides to "change goods"
    Then "Robert" should be on the "ERP - Product search (<business type>)" page

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business type>)" page

    Examples:
      | imported or not | business type |
      | imported        | UK importer   |
      | not imported    | UK business   |


  @TT-2077
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to tell where do they import goods from
    Given "Robert" got to "ERP - Product search (<business type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business type>)" page

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
      | imported or not | business type | expected                               |
      | imported        | UK importer   | Where do you import from (UK importer) |


  @TT-2078
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to specify what were UK sales volumes for these goods before Brexit
    Given "Robert" got to "ERP - Product search (<business type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - <expected>" page
    Then "Robert" should see following options
      | options                     |
      | kilograms (kg)              |
      | litres                      |
      | meters                      |
      | units (number of items)     |
      | Other                       |
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Save for later  |
      | Footer          |

    Examples:
      | imported or not | business type | expected                    |
      | not imported    | UK business   | Sales volumes (UK business) |
