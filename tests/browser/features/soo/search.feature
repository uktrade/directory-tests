@allure.suite:SOO
Feature: SOO - Search for marketplace

  Background:
    Given test authentication is done


  @allure.link:XOT-631
  @allure.link:XOT-689
  @exopps
  @soo-long-domestic
  @account-support
  @read-only
  Scenario Outline: Visitors should be able to search for marketplaces to sell "<products>" in "<country>"
    Given "Robert" visits the "Selling Online Overseas - <starting page>" page

    When "Robert" searches for marketplaces in "<country>" to sell "<products>"

    Then "Robert" should be on the "Selling Online Overseas - Search results" page
    And "Robert" should see marketplaces which operate globally or in "<country>"

    Examples: products and countries
      | starting page  | country   | products                 |
      | Home           | Australia | Clothing and accessories |
      | Search results | Poland    | Home and lifestyle       |


  @allure.link:XOT-689
  @exopps
  @soo-long-domestic
  @account-support
  @read-only
  Scenario Outline: Domestic "Selling Online Overseas" Enquirers should be able to view marketplace page
    Given "Robert" searches for marketplaces in "<country>" to sell "<products>"

    When "Robert" randomly selects a marketplace

    Then "Robert" should be on the "Selling Online Overseas - Marketplace" page
    Then "Robert" should see following sections
      | Sections            |
      | Header              |
      | Breadcrumbs         |
      | Logo                |
      | Apply now - sidebar |
      | Market details      |
      | Back                |
      | Error reporting     |
#      See TT-1778 there's a problem with lazy loading and Firefox
#      | Footer              |

    Examples: products and countries
      | country   | products                 |
      | Australia | Clothing and accessories |
      | China     | Sports and leisure       |
