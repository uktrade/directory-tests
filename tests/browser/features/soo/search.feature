Feature: Search for marketplace

  Background:
    Given basic authentication is done for "Selling Online Overseas - Home" page


  @XOT-631
  @XOT-689
  @exopps
  @dev-only
  @soo-long-domestic
  @account-support
  Scenario Outline: Visitors should be able to search for marketplaces to sell "<products>" in "<countries>"
    Given "Robert" visits the "Selling Online Overseas - <starting page>" page

    When "Robert" searches for marketplaces in "<country>" to sell "<products>"

    Then "Robert" should be on the "Selling Online Overseas - Search results" page
    And "Robert" should see marketplaces which operate globally or in "<country>"

    Examples: products and countries
      | starting page  | country   | products               |
      | Home           | Australia | Clothing & Accessories |
      | Search results | Poland    | Home & Garden          |


  @XOT-689
  @exopps
  @captcha
  @dev-only
  @soo-long-domestic
  @account-support
  Scenario Outline: Domestic "Selling Online Overseas" Enquirers should be able to view marketplace page
    Given "Robert" searches for marketplaces in "<country>" to sell "<products>"

    When "Robert" randomly selects a marketplace

    Then "Robert" should be on the "Selling Online Overseas - Marketplace" page

    Examples: products and countries
      | country   | products               |
      | Australia | Clothing & Accessories |
      | China     | Sporting Goods         |
