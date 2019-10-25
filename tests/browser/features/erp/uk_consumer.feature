@erp
@uk_consumer
@TT-2047
Feature: ERP - UK consumer


  Scenario: An enquirer representing a "UK consumer" should be able to tell which goods are affected
    Given "Robert" visits the "ERP - User type" page

    When "Robert" says that he represents a "UK consumer"

    Then "Robert" should be on the "ERP - Product search (UK consumer)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Hierarchy codes |
      | Footer          |


  @drill
  Scenario: A UK customer should be able to select goods affected by Brexit
    Given "Robert" got to "ERP - Product search (UK consumer)" from "ERP - User type" via "UK consumer"

    When "Robert" selects a random product code from the hierarchy of product codes

    Then "Robert" should be on the "ERP - Product detail (UK consumer)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Save for later  |
      | Footer          |


  @drill
  Scenario: A UK customer should be able to change the goods previously selected
    Given "Robert" got to "ERP - Product search (UK consumer)" from "ERP - User type" via "UK consumer"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (UK consumer)" page

    When "Robert" decides to "change goods"
    Then "Robert" should be on the "ERP - Product search (UK consumer)" page

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (UK consumer)" page


  @changes
  Scenario: UK customers should be able to tell whether they're aware of price & choice changes since Brexit
    Given "Robert" got to "ERP - Product search (UK consumer)" from "ERP - User type" via "UK consumer"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (UK consumer)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Are you aware of changes (UK consumer)" page
    Then "Robert" should see following options
      | options                     |
      | Aware of price changes      |
      | Not aware of price changes  |
      | Aware of choice changes     |
      | Not aware of choice changes |
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Save for later  |
      | Footer          |


  @changes
  Scenario: UK customers should be able to provide us with other information regarding price & choice changes since Brexit
    Given "Robert" got to "ERP - Product search (UK consumer)" from "ERP - User type" via "UK consumer"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (UK consumer)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Are you aware of changes (UK consumer)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Other information (UK customer)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Save for later  |
      | Footer          |


  @changes
  Scenario Outline: UK customers representing a "<specific group of consumers>" should be able to complete and submit their form
    Given "Robert" got to "ERP - Product search (UK consumer)" from "ERP - User type" via "UK consumer"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (UK consumer)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Are you aware of changes (UK consumer)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Other information (UK customer)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Consumer type (UK consumer)" page

    When "Robert" says that he represents a "<specific group of consumers>"
    Then "Robert" should be on the "ERP - <expected>" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Summary (UK consumer)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Finished (UK consumer)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Form submitted  |
      | Footer          |

    Examples: consumer type
      | specific group of consumers | expected                             |
      | consumer group              | Consumer group details (UK consumer) |
      | individual consumer         | Personal details (UK consumer)       |


  @TT-2060
  @search
  Scenario Outline: A UK customer should be able to search for affected goods by commodity code or part of their name
    Given "Robert" got to "ERP - Product search (UK consumer)" from "ERP - User type" via "UK consumer"

    When "Robert" searches using "<phrase>"

    Then "Robert" should see "<an expected number of>" product code(s) to select
    And "Robert" should see "<a number of>" product category(ies) to expand

    Examples: search phrases
      | phrase           | an expected number of | a number of |
      | food             | at least 1            | at least 1  |
      | mineral products | at least 1            | at least 1  |

    Examples: specific product codes
      | phrase     | an expected number of | a number of |
      | 3904400091 | at least 1            | at least 1  |
      | 2309904151 | at least 1            | at least 1  |

    Examples: parent product code category
      | phrase   | an expected number of | a number of |
      | 21069055 | no                    | at least 1  |
      | 05100000 | no                    | at least 1  |


  @TT-2054
  @print
  Scenario Outline: A "<uk consumer>" should be able to print a copy of their submitted form
    Given "Robert" submitted his ERP form as "<uk consumer>"

    Then "Robert" should be on the "ERP - Finished (UK consumer)" page
    And "Robert" should be able to print out a copy of submitted form

    Examples: types of UK consumers
      | uk consumer         |
      | individual consumer |
      | consumer group      |


  @TT-2056
  @save-for-later
  @restore-session
  Scenario Outline: A "<uk consumer>" should be able to get back to "<expected>" page using the link to restore their progress
    Given "Robert" got to "<expected>" ERP page as "<uk consumer>"

    When "Robert" saves progress for later
    Then "Robert" should receive an email with a link to restore saved ERP session

    When "Robert" clears the cookies
    And "Robert" decides to restore saved ERP progress using the link he received

    Then "Robert" should be on the "ERP - <expected>" page

    Examples: stages at which user can save progress
      | expected                               | uk consumer         |
      | Product detail (UK consumer)           | individual consumer |
      | Are you aware of changes (UK consumer) | individual consumer |
      | Other information (UK customer)        | individual consumer |
      | Consumer type (UK consumer)            | individual consumer |
      | Personal details (UK consumer)         | individual consumer |
      | Summary (UK consumer)                  | individual consumer |
      | Consumer type (UK consumer)            | consumer group      |
      | Consumer group details (UK consumer)   | consumer group      |
      | Summary (UK consumer)                  | consumer group      |
