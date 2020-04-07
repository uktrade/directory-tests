@dev-only
@erp
@uk_business
@allure.suite:ERP
Feature: ERP - UK business


  Background:
    Given test authentication is done for "ERP"


  @allure.link:TT-2073
  @UK_business
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


  @allure.link:TT-2074
  @full
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
      | not imported    | UK business   |


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
      | not imported    | UK business   |


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
      | not imported    | UK business   |


  @allure.link:TT-2078
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to specify what were UK sales volumes for these goods before Brexit
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

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
      | imported or not | business_type | expected                    |
      | not imported    | UK business   | Sales volumes (UK business) |


  @allure.link:TT-2079
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to specify what were UK export volumes before Brexit
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - <expected>" page

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
      | imported or not | business_type | expected                    |
      | not imported    | UK business   | Sales volumes (UK business) |


  @allure.link:TT-2080
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to tell us if they're aware of sales changes
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Sales volumes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales revenue (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of sales changes (<business_type>)" page
    Then "Robert" should see following options
      | options                     |
      | aware of volume changes     |
      | not aware of volume changes |
      | aware of price changes      |
      | not aware of price changes  |
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
      | not imported    | UK business   |


  @allure.link:TT-2081
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to tell us if they're aware of market size changes
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Sales volumes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales revenue (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of sales changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of market size changes (<business_type>)" page
    Then "Robert" should see following options
      | options                          |
      | aware of market size changes     |
      | not aware of market size changes |
      | aware of price changes           |
      | not aware of price changes       |
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
      | not imported    | UK business   |


  @allure.link:TT-2082
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to tell us if they're aware of other changes
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Sales volumes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales revenue (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of sales changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of market size changes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of other changes (<business_type>)" page
    Then "Robert" should see following options
      | options                    |
      | aware of other changes     |
      | not aware of other changes |
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
      | not imported    | UK business   |


  @allure.link:TT-2083
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to tell us about total UK market value of affected goods
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
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
    Then "Robert" should be on the "ERP - Market size (<business_type>)" page
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
      | not imported    | UK business   |


  @allure.link:TT-2084
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to tell us what outcome (in terms of tariffs and quotas) they are seeking for affected goods
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
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
    Then "Robert" should be on the "ERP - Market size (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - What outcome are you seeking for (<business_type>)" page
    Then "Robert" should see following options
      | options                                                 |
      | I want the tariff rate to increase                      |
      | I want the tariff rate to decrease                      |
      | I want the tariff rate to neither increase or decrease  |
      | I want the tariff quota to increase                     |
      | I want the tariff quota to decrease                     |
      | I want the tariff quota to neither increase or decrease |
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
      | not imported    | UK business   |


  @allure.link:TT-2085
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to provide us with business details
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
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
    Then "Robert" should be on the "ERP - Market size (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - What outcome are you seeking for (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Business details (<business_type>)" page
    Then "Robert" should see following options
      | options                              |
      | UK private or public limited company |
      | Other type of UK organisation        |
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
      | not imported    | UK business   |


  @allure.link:TT-2086
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to provide us with personal details
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
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
      | not imported    | UK business   |


  @allure.link:TT-2087
  @full
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to see the form summary before submitting it
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
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
      | Answers         |
      | Form            |
      | Save for later  |
      | Footer          |

    Examples:
      | imported or not | business_type |
      | not imported    | UK business   |


  @allure.link:TT-2088
  @dev-only
  @captcha
  @<business_type>
  Scenario Outline: A UK business which goods are "<imported or not>" from overseas should be able to submit the complete form
    Given "Robert" got to "ERP - Product search (<business_type>)" from "ERP - User type" via "UK business -> <imported or not>"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
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
      | not imported    | UK business   |


  @allure.link:TT-2116
  @save-for-later
  @restore-session
  @bug
  @allure.issue:TT-2098
  @fixed
  Scenario Outline: A UK business should be able to resume progress giving feedback from "<expected>" page
    Given "Robert" got to "<expected>" ERP page as "UK business"

    When "Robert" saves progress for later
    Then "Robert" should receive an email with a link to restore saved ERP session

    When "Robert" clears the cookies
    And "Robert" decides to restore saved ERP progress using the link he received

    Then "Robert" should be on the "ERP - <expected>" page
    And "Robert" should be able to resume giving feedback as "UK business" from "<expected>" page

    Examples: stages at which user can save progress
      | expected                                           |
      | Product detail (UK business)                       |
      | Sales volumes (UK business)                        |
      | Sales revenue (UK business)                        |
      | Are you aware of sales changes (UK business)       |
      | Are you aware of market size changes (UK business) |
      | Are you aware of other changes (UK business)       |
      | Market size (UK business)                          |
      | What outcome are you seeking for (UK business)     |
      | Business details (UK business)                     |
      | Personal details (UK business)                     |
      | Summary (UK business)                              |
