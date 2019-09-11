@header-footer
Feature: INTL - Header-Footer

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
