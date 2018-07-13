@header-footer
Feature: Header-Footer


  @CMS-158
  @logo
  @header
  @footer
  Scenario Outline: Visitors should see correct UK Government logo (with Union Jack) in the page header and footer on "<selected>" page
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
  Scenario Outline: Visitors should be able to get to the "<specific>" page via "<menu>" link
    Given "Robert" visits the "Invest - Home" page

    When "Robert" decides to use "<menu>" link to the "<specific>" page

    Then "Robert" should be on the "<specific>" page

    Examples:
      | menu   | specific                |
      | header | Invest - Home           |
      | header | Invest - Industries     |
      | header | Invest - UK Setup Guide |
      | header | Invest - Contact Us     |
      | footer | Invest - Home           |
      | footer | Invest - Industries     |
      | footer | Invest - UK Setup Guide |
      | footer | Invest - Contact Us     |


  @wip
  @CMS-158
  @logo
  @header
  @footer
  Scenario Outline: Visitors should be able to get to the Home (Invest) page from "<selected>" page by using UK Government logo in the page header
    Given "Robert" visits the "<selected>" page

    When "Robert" decides to click on the UK Government logo in the page "header"

    Then "Robert" should be on the "Invest Home" page

    Examples:
      | selected                          |
      | Home                              |
      | Industries                        |
      | UK Setup Guide                    |
      | Contact Us                        |
      | Feedback                          |
      | Invest - Automotive               |
      | Invest - Capital Investment       |
      | Invest - Creative industries      |
      | Invest - Financial services       |
      | Invest - Health and life sciences |
      | Invest - Technology               |
