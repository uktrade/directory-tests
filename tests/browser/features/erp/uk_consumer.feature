@dev-only
@erp
@uk_consumer
@allure.link:TT-2047
@allure.suite:ERP
Feature: ERP - UK consumer


  Background:
    Given test authentication is done for "ERP"


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
  @full
  Scenario: A UK consumer should be able to select goods affected by Brexit
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
  Scenario: A UK consumer should be able to change the goods previously selected
    Given "Robert" got to "ERP - Product search (UK consumer)" from "ERP - User type" via "UK consumer"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (UK consumer)" page

    When "Robert" decides to "change goods"
    Then "Robert" should be on the "ERP - Product search (UK consumer)" page

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (UK consumer)" page


  @changes
  @full
  Scenario: UK consumers should be able to tell whether they're aware of price & choice changes since Brexit
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
  @full
  Scenario: UK consumers should be able to provide us with other information regarding price & choice changes since Brexit
    Given "Robert" got to "ERP - Product search (UK consumer)" from "ERP - User type" via "UK consumer"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (UK consumer)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Are you aware of changes (UK consumer)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Other information (UK consumer)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Save for later  |
      | Footer          |


  @changes
  @dev-only
  @captcha
  Scenario Outline: UK consumers representing a "<specific group of consumers>" should be able to complete and submit their form
    Given "Robert" got to "ERP - Product search (UK consumer)" from "ERP - User type" via "UK consumer"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (UK consumer)" page

    When "Robert" decides to "continue"
    Then "Robert" should be on the "ERP - Are you aware of changes (UK consumer)" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Other information (UK consumer)" page

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


  @allure.link:TT-2060
  @search
  Scenario Outline: A UK consumer should be able to search for affected goods by "<phrase>" which can be a commodity code or part of their name
    Given "Robert" got to "ERP - Product search (UK consumer)" from "ERP - User type" via "UK consumer"

    When "Robert" searches using "<phrase>"
    And "Robert" selects a random product "code" from search results

    Then "Robert" should be on the "ERP - Product detail (UK consumer)" page

    Examples: search phrases
      | phrase           |
      | food             |
      | mineral products |

    Examples: specific product codes
      | phrase     |
      | 3904400091 |
      | 2309904151 |
      | 9305200010 |


  @allure.link:TT-2060
  @search
  Scenario Outline: A UK consumer should be able to see product code details after looking for it using a "<phrase>" which is their commodity code
    Given "Robert" got to "ERP - Product search (UK consumer)" from "ERP - User type" via "UK consumer"

    When "Robert" searches using "<phrase>"
    And "Robert" selects a random product "category" from search results
    Then "Robert" should be on the "ERP - Product search (UK consumer)" page

    When "Robert" selects a random product code from an expanded hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (UK consumer)" page

    Examples: parent product code category
      | phrase     |
      | 21069055   |
      | 05100000   |
      | 9305200000 |
      | 988        |
      | 9880000000 |
      | 67         |
      | 6700000000 |


  @allure.link:TT-2054
  @print
  Scenario Outline: A "<uk consumer>" should be able to print a copy of their submitted form
    Given "Robert" submitted his ERP form as "<uk consumer>"

    Then "Robert" should be on the "ERP - Finished (UK consumer)" page
    And "Robert" should be able to print out a copy of submitted form

    Examples: types of UK consumers
      | uk consumer         |
      | individual consumer |
      | consumer group      |


  @allure.link:TT-2056
  @save-for-later
  @restore-session
  @bug
  @allure.issue:TT-2098
  @fixed
  Scenario Outline: A "<uk consumer>" should be able to resume progress giving feedback from "<expected>" page
    Given "Robert" got to "<expected>" ERP page as "<uk consumer>"

    When "Robert" saves progress for later
    Then "Robert" should receive an email with a link to restore saved ERP session

    When "Robert" clears the cookies
    And "Robert" decides to restore saved ERP progress using the link he received

    Then "Robert" should be on the "ERP - <expected>" page
    And "Robert" should be able to resume giving feedback as "<uk consumer>" from "<expected>" page

    Examples: stages at which user can save progress
      | expected                               | uk consumer         |
      | Product detail (UK consumer)           | individual consumer |
      | Are you aware of changes (UK consumer) | individual consumer |
      | Other information (UK consumer)        | individual consumer |
      | Consumer type (UK consumer)            | individual consumer |
      | Summary (UK consumer)                  | individual consumer |
      | Consumer type (UK consumer)            | consumer group      |
      | Summary (UK consumer)                  | consumer group      |
      | Consumer group details (UK consumer)   | consumer group      |
      | Personal details (UK consumer)         | individual consumer |
