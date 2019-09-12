@header-footer
Feature: Invest - Header-Footer

  Background:
    Given basic authentication is done for "International - Landing" page

  @CMS-158
  @logo
  @header
  @footer
  Scenario Outline: Visitors should see correct UK Government logo, with Union Jack, in the page header and footer on "<selected>" page
    Given "Robert" visits the "<selected>" page

    Then "Robert" should be on the "<expected>" page
    And "Robert" should see correct UK Government logo in page "header"
    And "Robert" should see correct UK Government logo in page "footer"
    And "Robert" should see the correct favicon

    Examples:
      | selected                | expected                                |
      | Invest - Home           | Invest - Home                           |
      | Invest - Contact Us     | Invest - Contact Us                     |


  @stage-only
  @CMS-158
  @logo
  @header
  @footer
  Scenario Outline: Visitors should see correct UK Government logo, with Union Jack, in the page header and footer on "<selected>" page
    Given "Robert" visits the "<selected>" page

    Then "Robert" should be on the "<expected>" page
    And "Robert" should see correct "Great - header" logo
    And "Robert" should see correct "Great - footer" logo
    And "Robert" should see the correct favicon

    Examples:
      | selected                                         | expected                                         |
      | Invest - High productivity food production - HPO | Invest - High productivity food production - HPO |
      | Invest - Lightweight structures - HPO            | Invest - Lightweight structures - HPO            |
      | Invest - Rail infrastructure - HPO               | Invest - Rail infrastructure - HPO               |


  @CMS-158
  @header
  @footer
  @home-page
  @<specific>
  Scenario Outline: Visitors should be able to get to the "<specific>" page via "<section>" link
    Given "Robert" visits the "Invest - Home" page

    When "Robert" decides to use "<specific>" link from page "Invest - <section>"

    Then "Robert" should be on the "<expected>" page

    Examples:
      | specific           | section | expected                       |
      | Invest             | header  | Invest - Home                  |
      | Industries         | header  | International - Industries     |
      | UK setup guide     | header  | International - UK setup guide |
      | Find a UK Supplier | header  | Find a Supplier - Landing      |


  @CMS-158a
  @logo
  @header
  @footer
  Scenario Outline: Visitors should be able to get to the Invest home page from "<selected>" page by using UK Government logo in the page header
    Given "Robert" visits the "Invest - <selected>" page

    When "Robert" decides to click on "Invest in Great logo"

    Then "Robert" should be on the "International - Landing" page

    Examples:
      | selected                            |
      | Home                                |
      | UK Setup Guide                      |
      | Contact Us                          |

    @dev-only
    Examples: UK setup guides
      | selected                                          |
      | Access finance in the UK - guide                  |
      | DIT's guide to UK Capital Gains Tax - guide       |
      | DIT's guide to UK Corporation Tax - guide         |
      | DIT's Guide to UK Venture Capital Schemes - guide |
      | Establish a UK business base - guide              |
      | Register a company in the UK - guide              |
      | UK Income Tax - guide                             |
      | UK infrastructure - guide                         |
      | UK talent and labour - guide                      |
      | UK tax and incentives - guide                     |

    @stage-only
    Examples: Legacy UK setup guides
      | selected                                         |
      | Access finance in the UK (Staging) - guide       |
      | Open a UK business bank account (Staging) - guide|
      | UK tax and incentives (Staging) - guide          |

    @uat-only
    Examples: UK setup guides
      | selected                                          |
      | Access finance in the UK - guide                  |
      | DIT's guide to UK Capital Gains Tax - guide       |
      | DIT's guide to UK Corporation Tax - guide         |
      | DIT's Guide to UK Venture Capital Schemes - guide |
      | Establish a UK business base - guide              |
      | Register a company in the UK - guide              |
      | UK Income Tax - guide                             |
      | UK infrastructure - guide                         |
      | UK talent and labour - guide                      |
      | UK tax and incentives - guide                     |