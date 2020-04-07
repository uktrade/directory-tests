@search
@allure.suite:Domestic
Feature: Domestic - Great site search

  Background:
    Given test authentication is done


  @allure.link:XOT-760
  Scenario: Visitor should see empty search results if they don't specify search phrase
    Given "Robert" visits the "Domestic - Home" page

    When "Robert" decides to click on "search button"

    Then "Robert" should be on the "Domestic - Empty Search results" page


  @allure.link:XOT-760
  Scenario Outline: Visitor should see search results for "<phrase>"
    Given "Robert" visits the "Domestic - <specific>" page

    When "Robert" searches using "<phrase>"

    Then "Robert" should see search results page number "1" for "<phrase>"
#    And "Robert" should see search results in following order "Article, Service, Event, Opportunity"

    Examples: event, market, service and opportunity
      | specific        | phrase      |
      | Home            | Work        |
      | Advice landing  | Transport   |
      | Markets listing | Export      |


  @bug
  @allure.issue:XOT-840
  @fixed
  @allure.link:XOT-760
  Scenario Outline: Visitors should be able to find out more about the "<type of>" search results
    Given "Robert" searched using "<phrase>" on the "Domestic - <specific>" page

    When "Robert" decides to find out more about random "<type of>" result

    Then "Robert" should be on one of the "<expected>" pages

    Examples: event, market, service and opportunity
      | specific        | phrase | type of            | expected                                                                          |
      | Home            | Food   | Event              | Events - Event                                                                    |
      | Markets listing | Food   | Online marketplace | Selling Online Overseas - Marketplace, Domestic - Markets - guide, Events - event |

    @bug
    @allure.issue:XOT-1208
    @fixme
    Examples: event, market, service and opportunity
      | specific       | phrase         | type of            | expected                                                                                            |
      | Advice landing | export finance | Service            | Domestic - Get Finance, Export Opportunities - Home, Selling Online Overseas - Home, Events - event |
      | Advice landing | Transport      | Article            | Domestic - Advice article, Domestic - Markets                                                       |
      | Services       | Manufacture    | Export opportunity | Export Opportunities - Opportunity                                                                  |


  @allure.link:XOT-760
  Scenario Outline: Visitors should be able to navigate through search results pages for "<phrase>"
    Given "Robert" searched using "<phrase>" on the "Domestic - <specific>" page
    And "Robert" sees more than "1" search result page

    When "Robert" decides to use "Next" link
    Then "Robert" should see search results page number "2" for "<phrase>"

    When "Robert" decides to use "Previous" link
    Then "Robert" should see search results page number "1" for "<phrase>"

    Examples: event, market, service and opportunity
      | specific        | phrase      |
      | Home            | Work        |
      | Advice landing  | Transport   |
      | Markets listing | Water       |


  @allure.link:XOT-760
  Scenario Outline: Visitor should be able to clear the last search for "<first phrase>" and start new search for "<second phrase>"
    Given "Robert" searched using "<first phrase>" on the "Domestic - <specific>" page
    And "Robert" sees search results page number "1" for "<first phrase>"

    When "Robert" searches using "<second phrase>"

    Then "Robert" should see search results page number "1" for "<second phrase>"

    Examples: event, market, service and opportunity
      | specific        | first phrase | second phrase           |
      | Home            | Work         | Full work service       |
      | Advice landing  | Transport    | way                     |
      | Markets listing | Water        | Market selection clinic |
