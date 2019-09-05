@header-footer
Feature: Header-Footer

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
      | selected                       | expected                                |
      | International - Landing        | International - Landing                 |
      | International - Contact Us     | International - Contact Us              |
      | International - UK Setup Guide | International - How to set up in the UK |


  @CMS-158
  @header
  @footer
  @home-page
  @<specific>
  Scenario Outline: Visitors should be able to get to the "<expected>" page via "<section>" link
    Given "Robert" visits the "Invest - Home" page

    When "Robert" decides to use "<specific>" link from page "Invest - <section>"

    Then "Robert" should be on the "<expected>" page

    Examples:
      | specific           | section | expected                       |
      | Invest             | header  | Invest - Home                  |
      | UK setup guide     | header  | International - UK setup guide |
      | Industries         | header  | International - Industries     |
      | Find a UK Supplier | header  | Find a Supplier - Landing         |


  @CMS-158
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

    @full
    Examples:
      | selected                            |
      | Capital Investment - industry       |
      | Health and life sciences - industry |
      | Technology - industry               |
#      | Feedback                            | it's a separate service with different header & footer

    @dev-only
    @full
    Examples:
      | selected                            |
      | Creative industries - industry      |
      | Financial services - industry       |

    @stage-only
    @full
    Examples:
      | selected                            |
      | Health and life sciences - industry |

    @uat-only
    @full
    Examples:
      | selected                            |
      | Financial services - industry       |
