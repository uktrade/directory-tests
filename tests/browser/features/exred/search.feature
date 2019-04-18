Feature: Great site search

  @XOT-760
  Scenario: Visitor should see empty search results if they don't specify search phrase
    Given "Robert" visits the "Export Readiness - Home" page

    When "Robert" decides to "search button"

    Then "Robert" should be on the "Export Readiness - Empty Search results" page


  @XOT-760
  Scenario Outline: Visitor should see search results
    Given "Robert" visits the "Export Readiness - <specific>" page

    When "Robert" searches using "<phrase>"

    Then "Robert" should see search results page number "1" for "<phrase>"
#    And "Robert" should see search results in following order "Article, Service, Event, Opportunity"

    Examples: event, market, service and opportunity
      | specific | phrase            |
      | Home     | Food              |
      | Advice   | Transport         |
      | Markets  | Steel             |
      | Services | Manufacture       |


  @wip
  @bug
  @XOT-840
  @XOT-760
  Scenario Outline: Visitors should be able to find out more about the "<type of>" search results
    Given "Robert" searched using "<phrase>" on the "Export Readiness - <specific>" page

    When "Robert" decides to find out more about random "<type of>" result

    Then "Robert" should be on one of the "<expected>" pages

    Examples: event, market, service and opportunity
      | specific | phrase         | type of     | expected                           |
      | Home     | Food           | Event       | Events - Event                     |
      | Advice   | Transport      | Article     | Export Readiness - Advice          |
      | Advice   | export finance | Service     | Export Readiness - Get Finance     |
      | Markets  | Food           | Market      | Something                          |
      | Services | Manufacture    | Opportunity | Export Opportunities - Opportunity |


  @XOT-760
  Scenario Outline: Visitors should be able to navigate through search results pages
    Given "Robert" searched using "<phrase>" on the "Export Readiness - <specific>" page
    And "Robert" sees more than "1" search result page

    When "Robert" decides to go to the "Next" page
    Then "Robert" should see search results page number "2" for "<phrase>"

    When "Robert" decides to go to the "Previous" page
    Then "Robert" should see search results page number "1" for "<phrase>"

    Examples: event, market, service and opportunity
      | specific | phrase            |
      | Home     | Food              |
      | Advice   | Transport         |
      | Markets  | Steel             |
      | Services | Manufacture       |


  @XOT-760
  Scenario Outline: Visitor should be able to clear the last search and start new search
    Given "Robert" searched using "<first phrase>" on the "Export Readiness - <specific>" page
    And "Robert" sees search results page number "1" for "<first phrase>"

    When "Robert" searches using "<second phrase>"

    Then "Robert" should see search results page number "1" for "<second phrase>"

    Examples: event, market, service and opportunity
      | specific | first phrase      | second phrase           |
      | Home     | Food              | Full food service       |
      | Advice   | Transport         | Passenger transport     |
      | Markets  | Steel             | Market selection clinic |
      | Services | Manufacture       | Motor vehicles          |