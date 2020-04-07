@dev-only
@erp
@uk_business
@allure.suite:ERP
Feature: ERP - UK business


  Background:
    Given test authentication is done for "ERP"


  @allure.link:TT-2074
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should see a list of product codes which might be affected by Brexit
    Given "Robert" got to "ERP - Import from overseas (UK business)" from "ERP - User type" via "UK business"

    When "Robert" says that affected goods are "<imported or not>" from overseas

    Then "Robert" should be on the "ERP - Product search (<business_type>)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Hierarchy codes |
      | Footer          |

    Examples:
      | imported or not | business_type |
      | imported        | UK importer   |


  @allure.link:TT-2075
  @drill
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to select goods affected by Brexit
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes

    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Save for later  |
      | Footer          |

    Examples:
      | imported or not | business_type |
      | imported        | UK importer   |


  @allure.link:TT-2076
  @<business_type>
  @drill
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to change the goods previously selected
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "change goods"
    Then "Robert" should be on the "ERP - Product search (<business_type>)" page

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    Examples:
      | imported or not | business_type |
      | imported        | UK importer   |


  @allure.link:TT-2077
  @full
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


  @allure.link:TT-2101
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to tell whether imported goods are used to make something else or not
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Where do you import from (UK importer)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are there goods used to make something else (<business_type>)" page
    Then "Robert" should see following options
      | options |
      | yes     |
      | no      |
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Save for later  |
      | Footer          |

    Examples:
      | imported or not | business_type |
      | imported        | UK importer   |


  @allure.link:TT-2102
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to tell what were company's UK sales volumes for these goods before Brexit
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Where do you import from (UK importer)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are there goods used to make something else (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales volumes (<business_type>)" page
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
      | imported or not | business_type |
      | imported        | UK importer   |


  @allure.link:TT-2103
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to tell what were company's UK export volumes before Brexit
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Where do you import from (UK importer)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are there goods used to make something else (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales volumes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales revenue (<business_type>)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Save for later  |
      | Footer          |

    Examples:
      | imported or not | business_type |
      | imported        | UK importer   |


  @allure.link:TT-2104
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to tell whether they're aware of changes to UK imports for selected goods since Brexit
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Where do you import from (UK importer)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are there goods used to make something else (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales volumes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales revenue (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of sales changes (<business_type>)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Save for later  |
      | Footer          |

    Examples:
      | imported or not | business_type |
      | imported        | UK importer   |


  @allure.link:TT-2105
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to tell whether they're aware of changes to their sales for selected goods since Brexit
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Where do you import from (UK importer)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are there goods used to make something else (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales volumes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales revenue (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of sales changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of market size changes (<business_type>)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Save for later  |
      | Footer          |

    Examples:
      | imported or not | business_type |
      | imported        | UK importer   |


  @allure.link:TT-2106
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to tell whether they're aware of other changes for selected goods since Brexit
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Where do you import from (UK importer)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are there goods used to make something else (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales volumes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales revenue (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of sales changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of market size changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of other changes (<business_type>)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Save for later  |
      | Footer          |

    Examples:
      | imported or not | business_type |
      | imported        | UK importer   |


  @allure.link:TT-2107
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to tell us what percentage of their production do these goods make up
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Where do you import from (UK importer)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are there goods used to make something else (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales volumes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales revenue (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of sales changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of market size changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of other changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - What percentage of your production do these goods make up (<business_type>)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Save for later  |
      | Footer          |

    Examples:
      | imported or not | business_type |
      | imported        | UK importer   |


  @allure.link:TT-2108
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to tell us if there are equivalent goods made in the UK
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Where do you import from (UK importer)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are there goods used to make something else (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales volumes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales revenue (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of sales changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of market size changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of other changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - What percentage of your production do these goods make up (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are there equivalent goods made in the UK (<business_type>)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Save for later  |
      | Footer          |

    Examples:
      | imported or not | business_type |
      | imported        | UK importer   |


  @allure.link:TT-2109
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to tell us what's the total UK market value of these goods
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Where do you import from (UK importer)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are there goods used to make something else (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales volumes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales revenue (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of sales changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of market size changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of other changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - What percentage of your production do these goods make up (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are there equivalent goods made in the UK (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Market size (<business_type>)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Save for later  |
      | Footer          |

    Examples:
      | imported or not | business_type |
      | imported        | UK importer   |


  @allure.link:TT-2110
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to tell us what outcome they're seeking for
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Where do you import from (UK importer)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are there goods used to make something else (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales volumes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales revenue (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of sales changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of market size changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of other changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - What percentage of your production do these goods make up (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are there equivalent goods made in the UK (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Market size (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - What outcome are you seeking for (<business_type>)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Save for later  |
      | Footer          |

    Examples:
      | imported or not | business_type |
      | imported        | UK importer   |


  @allure.link:TT-2111
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to provide us with their business details
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Where do you import from (UK importer)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are there goods used to make something else (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales volumes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales revenue (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of sales changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of market size changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of other changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - What percentage of your production do these goods make up (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are there equivalent goods made in the UK (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Market size (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - What outcome are you seeking for (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Business details (<business_type>)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Save for later  |
      | Footer          |

    Examples:
      | imported or not | business_type |
      | imported        | UK importer   |


  @allure.link:TT-2112
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to provide us with their personal details
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Where do you import from (UK importer)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are there goods used to make something else (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales volumes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales revenue (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of sales changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of market size changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of other changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - What percentage of your production do these goods make up (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are there equivalent goods made in the UK (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Market size (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - What outcome are you seeking for (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Business details (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Personal details (<business_type>)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Save for later  |
      | Footer          |

    Examples:
      | imported or not | business_type |
      | imported        | UK importer   |


  @allure.link:TT-2113
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to see form summary before submitting it
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Where do you import from (UK importer)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are there goods used to make something else (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales volumes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales revenue (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of sales changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of market size changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of other changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - What percentage of your production do these goods make up (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are there equivalent goods made in the UK (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Market size (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - What outcome are you seeking for (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Business details (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Personal details (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Summary (<business_type>)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Save for later  |
      | Footer          |

    Examples:
      | imported or not | business_type |
      | imported        | UK importer   |


  @allure.link:TT-2114
  @dev-only
  @captcha
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to submit the form
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Where do you import from (UK importer)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are there goods used to make something else (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales volumes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales revenue (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of sales changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of market size changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of other changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - What percentage of your production do these goods make up (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are there equivalent goods made in the UK (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Market size (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - What outcome are you seeking for (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Business details (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Personal details (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Summary (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Finished (<business_type>)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Form submitted  |
      | Footer          |

    Examples:
      | imported or not | business_type |
      | imported        | UK importer   |


  @allure.link:TT-2115
  @save-for-later
  @restore-session
  @bug
  @allure.issue:TT-2098
  @fixed
  Scenario Outline: A UK importer should be able to resume progress giving feedback from "<expected>" page
    Given "Robert" got to "<expected>" ERP page as "UK importer"

    When "Robert" saves progress for later
    Then "Robert" should receive an email with a link to restore saved ERP session

    When "Robert" clears the cookies
    And "Robert" decides to restore saved ERP progress using the link he received

    Then "Robert" should be on the "ERP - <expected>" page
    And "Robert" should be able to resume giving feedback as "UK importer" from "<expected>" page

    Examples: stages at which user can save progress
      | expected                                                                |
      | Product detail (UK importer)                                            |
      | Where do you import from (UK importer)                                  |
      | Are there goods used to make something else (UK importer)               |
      | Sales volumes (UK importer)                                             |
      | Sales revenue (UK importer)                                             |
      | Are you aware of sales changes (UK importer)                            |
      | Are you aware of market size changes (UK importer)                      |
      | Are you aware of other changes (UK importer)                            |
      | What percentage of your production do these goods make up (UK importer) |
      | Are there equivalent goods made in the UK (UK importer)                 |
      | Market size (UK importer)                                               |
      | What outcome are you seeking for (UK importer)                          |
      | Business details (UK importer)                                          |
      | Personal details (UK importer)                                          |
      | Summary (UK importer)                                                   |
