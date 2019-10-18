@header-footer
Feature: INTL - Header-Footer

  Background:
    Given basic authentication is done for "International - Landing" page

  @CMS-158
  @logo
  @header
  @footer
  Scenario Outline: Visitors should see "Great" logo in the page header and footer on "<selected>" page
    Given "Robert" visits the "<selected>" page

    Then "Robert" should be on the "<expected>" page
    And "Robert" should see correct "<header>" logo
    And "Robert" should see correct "Great - footer" logo
    And "Robert" should see the correct favicon

    Examples:
      | selected                   | expected                   | header         |
      | International - Landing    | International - Landing    | Great - header |
      | International - Contact Us | International - Contact Us | EIG            |
