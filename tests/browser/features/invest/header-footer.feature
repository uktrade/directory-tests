@header-footer
Feature: Header-Footer


  @CMS-158
  @logo
  @header
  @footer
  Scenario Outline: Visitors should see correct UK Government logo, with Union Jack, in the page header and footer on "<selected>" page
    Given "Robert" visits the "<selected>" page

    Then "Robert" should be on the "<selected>" page
    And "Robert" should see correct UK Government logo in page "header"
    And "Robert" should see correct UK Government logo in page "footer"
    And "Robert" should see the correct favicon

    Examples:
      | selected                |
      | Invest - Home           |
      | Invest - Industries     |
      | Invest - UK Setup Guide |
      | Invest - Contact Us     |


  @CMS-158
  @header
  @footer
  @home-page
  @<specific>
  Scenario Outline: Visitors should be able to get to the "<specific>" page via "<section>" link
    Given "Robert" visits the "Invest - Home" page

    When "Robert" decides to use "<specific>" link from page "Invest - <section>"

    Then "Robert" should be on the "Invest - <specific>" page

    Examples:
      | specific       | section|
      | Home           | header |
      | Industries     | header |
      | UK Setup Guide | header |
      | Contact Us     | header |
      | Home           | footer |
      | Industries     | footer |
      | UK Setup Guide | footer |
      | Contact Us     | footer |


  @CMS-158
  @logo
  @header
  @footer
  Scenario Outline: Visitors should be able to get to the Invest home page from "<selected>" page by using UK Government logo in the page header
    Given "Robert" visits the "Invest - <selected>" page

    When "Robert" decides to click on the UK Government logo in the page "Invest - header"

    Then "Robert" should be on the "Invest - Home" page

    Examples:
      | selected                            |
      | Home                                |
      | Industries                          |
      | UK Setup Guide                      |
      | Contact Us                          |
      | Automotive - industry               |
      | Apply for a UK visa - guide         |

    @full
    Examples:
      | selected                            |
      | Capital Investment - industry       |
      | Creative industries - industry      |
      | Financial services - industry       |
      | Health and life sciences - industry |
      | Technology - industry               |
#      | Feedback                            | it's a separate service with different header & footer
