@erp
@uk_consumer
Feature: ERP - An exporter from developing country


  @TT-2121
  Scenario: An enquirer representing an "exporter from developing country" should be able to tell which country they are from
    Given "Robert" visits the "ERP - User type" page

    When "Robert" says that he represents an "exporter from developing country"

    Then "Robert" should be on the "ERP - Select country (Developing country)" page
    And "Robert" should see following sections
      | Sections |
      | Header   |
      | Beta bar |
      | Go back  |
      | Form     |
      | Footer   |


  @TT-2122
  @<business_type>
  Scenario Outline: An exporter from developing country should see a list of product codes which might be affected by Brexit
    Given "Robert" got to "ERP - Select country (<business_type>)" from "ERP - User type" via "exporter from developing country"

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Product search (<business_type>)" page
    And "Robert" should see following sections
      | Sections       |
      | Save for later |

    Examples: business type
      | business_type      |
      | Developing country |


  @TT-2123
  @<business_type>
  Scenario Outline: An exporter from developing country should should be able to select goods affected by Brexit
    Given "Robert" got to "ERP - Select country (<business_type>)" from "ERP - User type" via "exporter from developing country"

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Product search (<business_type>)" page

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    Examples: business type
      | business_type      |
      | Developing country |


  @TT-2124
  @<business_type>
  Scenario Outline: An exporter from developing country should should be able to change the goods previously selected
    Given "Robert" got to "ERP - Select country (<business_type>)" from "ERP - User type" via "exporter from developing country"

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Product search (<business_type>)" page

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "change goods"
    Then "Robert" should be on the "ERP - Product search (<business_type>)" page

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    Examples: business type
      | business_type      |
      | Developing country |


  @TT-2125
  @<business_type>
  Scenario Outline: An exporter from developing country should should be able to specify what were UK sales volumes for these goods before Brexit
    Given "Robert" got to "ERP - Select country (<business_type>)" from "ERP - User type" via "exporter from developing country"

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Product search (<business_type>)" page

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Sales volumes (<business_type>)" page

    Examples: business type
      | business_type      |
      | Developing country |


  @TT-2126
  @<business_type>
  Scenario Outline: An exporter from developing country should should be able to specify what were UK export volumes before Brexit
    Given "Robert" got to "ERP - Select country (<business_type>)" from "ERP - User type" via "exporter from developing country"

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Product search (<business_type>)" page

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Sales volumes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales revenue (<business_type>)" page

    Examples: business type
      | business_type      |
      | Developing country |


  @TT-2127
  @<business_type>
  Scenario Outline: An exporter from developing country should should be able to to tell us if they're aware of sales changes
    Given "Robert" got to "ERP - Select country (<business_type>)" from "ERP - User type" via "exporter from developing country"

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Product search (<business_type>)" page

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Sales volumes (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Sales revenue (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Are you aware of sales changes (<business_type>)" page

    Examples: business type
      | business_type      |
      | Developing country |


  @TT-2128
  @<business_type>
  Scenario Outline: An exporter from developing country should should be able to tell us if they're aware of market size changes
    Given "Robert" got to "ERP - Select country (<business_type>)" from "ERP - User type" via "exporter from developing country"

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Product search (<business_type>)" page

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

    Examples: business type
      | business_type      |
      | Developing country |


  @TT-2129
  @<business_type>
  Scenario Outline: An exporter from developing country should should be able to tell us if they're aware of other changes
    Given "Robert" got to "ERP - Select country (<business_type>)" from "ERP - User type" via "exporter from developing country"

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Product search (<business_type>)" page

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

    Examples: business type
      | business_type      |
      | Developing country |


  @TT-2130
  @<business_type>
  Scenario Outline: An exporter from developing country should should be able to tell us what outcome (in terms of tariffs and quotas) they are seeking for affected goods
    Given "Robert" got to "ERP - Select country (<business_type>)" from "ERP - User type" via "exporter from developing country"

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Product search (<business_type>)" page

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
    Then "Robert" should be on the "ERP - What outcome are you seeking for (<business_type>)" page

    Examples: business type
      | business_type      |
      | Developing country |


  @TT-2131
  @<business_type>
  Scenario Outline: An exporter from developing country should should be able to provide us with business details
    Given "Robert" got to "ERP - Select country (<business_type>)" from "ERP - User type" via "exporter from developing country"

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Product search (<business_type>)" page

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
    Then "Robert" should be on the "ERP - What outcome are you seeking for (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Business details (<business_type>)" page

    Examples: business type
      | business_type      |
      | Developing country |


  @TT-2132
  @<business_type>
  Scenario Outline: An exporter from developing country should should be able to provide us with personal details
    Given "Robert" got to "ERP - Select country (<business_type>)" from "ERP - User type" via "exporter from developing country"

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Product search (<business_type>)" page

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
    Then "Robert" should be on the "ERP - What outcome are you seeking for (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Business details (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Personal details (<business_type>)" page

    Examples: business type
      | business_type      |
      | Developing country |


  @TT-2133
  @<business_type>
  Scenario Outline: An exporter from developing country should should be able to see the form summary before submitting it
    Given "Robert" got to "ERP - Select country (<business_type>)" from "ERP - User type" via "exporter from developing country"

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Product search (<business_type>)" page

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
    Then "Robert" should be on the "ERP - What outcome are you seeking for (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Business details (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Personal details (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Summary (<business_type>)" page

    Examples: business type
      | business_type      |
      | Developing country |


  @TT-2134
  @<business_type>
  Scenario Outline: An exporter from developing country should should be able to submit the complete form
    Given "Robert" got to "ERP - Select country (<business_type>)" from "ERP - User type" via "exporter from developing country"

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Product search (<business_type>)" page

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
    Then "Robert" should be on the "ERP - What outcome are you seeking for (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Business details (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Personal details (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Summary (<business_type>)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Finished (<business_type>)" page

    Examples: business type
      | business_type      |
      | Developing country |


  @TT-2135
  @save-for-later
  @restore-session
  Scenario Outline: An exporter from developing country should be able to get back to "<expected>" page using the link to restore their progress
    Given "Robert" got to "<expected>" ERP page as "exporter from developing country"

    When "Robert" saves progress for later
    Then "Robert" should receive an email with a link to restore saved ERP session

    When "Robert" clears the cookies
    And "Robert" decides to restore saved ERP progress using the link he received

    Then "Robert" should be on the "ERP - <expected>" page

    Examples: stages at which user can save progress
      | expected                                                  |
      | Product search (Developing country)                       |
      | Product detail (Developing country)                       |
      | Sales volumes (Developing country)                        |
      | Sales revenue (Developing country)                        |
      | Are you aware of sales changes (Developing country)       |
      | Are you aware of market size changes (Developing country) |
      | Are you aware of other changes (Developing country)       |
      | What outcome are you seeking for (Developing country)     |
      | Business details (Developing country)                     |
      | Personal details (Developing country)                     |

    @bug
    @TT-2098
    @fixme
    Examples: stages at which user can save progress
      | expected                                                  |
      | Summary (Developing country)                              |
