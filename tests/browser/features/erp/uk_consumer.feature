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
    Given "Robert" got from "ERP - User type" to "ERP - Product search (UK consumer)" via "UK consumer"

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
    Given "Robert" got from "ERP - User type" to "ERP - Product search (UK consumer)" via "UK consumer"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (UK consumer)" page

    When "Robert" decides to "change goods"
    Then "Robert" should be on the "ERP - Product search (UK consumer)" page

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (UK consumer)" page


  @save-for-later
  Scenario: A UK customer should be able to save their goods selection for later
    Given "Robert" got from "ERP - User type" to "ERP - Product search (UK consumer)" via "UK consumer"

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (UK consumer)" page

    When "Robert" saves progress for later
    Then "Robert" should receive "We’ve saved your progress until" confirmation email


  @changes
  Scenario: UK customers should be able to tell whether they're aware of price & choice changes since Brexit
    Given "Robert" got from "ERP - User type" to "ERP - Product search (UK consumer)" via "UK consumer"

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
    Given "Robert" got from "ERP - User type" to "ERP - Product search (UK consumer)" via "UK consumer"

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
    Given "Robert" got from "ERP - User type" to "ERP - Product search (UK consumer)" via "UK consumer"

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

  @wip
  @search
  @drill
  Scenario: A UK customer should be able to search for affected goods by commodity code or part of their name
    Given "Robert" got from "ERP - User type" to "ERP - Product search (UK consumer)" via "UK consumer"

  @wip
  @print
  Scenario: UK customers should be able to print a copy of their submitted form
    Given "Robert" got from "ERP - User type" to "ERP - Product search (UK consumer)" via "UK consumer"

  @wip
  @save-for-later
  Scenario: A UK customer should be able to save their progress for later at any point in time
    Given "Robert" got from "ERP - User type" to "ERP - Product search (UK consumer)" via "UK consumer"

  @wip
  @save-for-later
  Scenario: A UK customer should be able to restore their progress using link from the email
    Given "Robert" got from "ERP - User type" to "ERP - Product search (UK consumer)" via "UK consumer"
