@international-page
@allure.suite:International
Feature: INTL - Landing page

  Background:
    Given basic authentication is done for "International - Landing" page

  @allure.link:ED-3114
  @dev-only
  Scenario: Visitors should see "Buy from the UK, Invest in the UK, Study in the UK, Visit the UK" sections on the International page
    Given "Robert" visits the "International - Landing" page

    Then "Robert" should see following sections
      | Sections              |
      | Header                |
      | Informative banner    |
      | Service cards         |
      | How DIT provides help |
      | Tariffs               |
      | Featured links        |
      | Error reporting       |
      | Study or visit the UK |
      | Footer                |


  @allure.link:ED-3136
  @dev-only
  @external-service
  @<expected_service>
  Scenario Outline: Visitors should be able to go to "<expected_service>" page from the International page
    Given "Robert" visits the "International - Landing" page

    When "Robert" decides to find out more about "<service>"

    Then "Robert" should be on the "<expected_service>" page

    Examples:
      | service          | expected_service          |
      | Expand to the UK | Invest - landing          |
      | Buy from the UK  | Find a Supplier - Landing |

    @wip
    Examples: ATM there are no links to these services
      | service          | expected_service       |
      | Study in the UK  | British Council - Home |
      | Visit the UK     | Visit Britain - Home   |


  @allure.link:ED-3149
  @dev-only
  @language-selector
  Scenario Outline: Visitors should be able to view International page in "<preferred_language>"
    Given "Robert" visits the "International - Landing" page

    When "Robert" decides to view the page in "<preferred_language>"

    Then "Robert" should be on the "International - Landing" page
    And "Robert" should see the page in "<preferred_language>"

    Examples: available languages
      | preferred_language |
      | English            |
      | Deutsch            |
      | Français           |
      | español            |
      | Português          |
      | 简体中文            |

    @wip
    Examples: Missing translations
      | preferred_language |
      | 日本語              |

  @bug
  @allure.issue:CMS-1263
  @fixme
    Examples: 500 ISE
      | preferred_language |
      | العربيّة            |


  @allure.link:ED-3083
  @dev-only
  @language-selector
  Scenario: Visitor should be able to open and close the language selector on "International - Landing" page
    Given "Robert" visits the "International - Landing" page

    When "Robert" opens up the language selector
    Then "Robert" should see the language selector

    When "Robert" closes the language selector


  @allure.link:ED-3083
  @dev-only
  @language-selector
  @accessibility
  Scenario: Keyboard users should be able to open and close the language selector using just the keyboard on "International - Landing" page
    Given "Robert" visits the "International - Landing" page

    When "Robert" opens up the language selector using his keyboard
    Then "Robert" should see the language selector

    When "Robert" closes the language selector using his keyboard


  @allure.link:ED-3149
  @dev-only
  Scenario: Visitors should be able to "get advice and services to help them export" from International page
    Given "Robert" visits the "International - Landing" page

    When "Robert" decides to find out more about "For UK Businesses"

    Then "Robert" should be on the "Domestic - Home" page
