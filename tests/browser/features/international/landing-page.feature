@international-page
Feature: International Page

  Background:
    Given basic authentication is done for "Export Readiness - Home" page

  @ED-3114
  @dev-only
  Scenario: Visitors should see "Buy from the UK, Invest in the UK, Study in the UK, Visit the UK" sections on the International page
    Given "Robert" visits the "International - Landing" page

    Then "Robert" should see following sections
      | Sections              |
      | Header                |
      | Service Cards         |
      | Error reporting       |
      | Footer                |
#      | Beta bar              |
#      | EU Exit updates       |
#      | News                  |
#      | Tariffs               |
#      | Study or visit the UK |


  @ED-3136
  @dev-only
  @external-service
  @<expected_service>
  Scenario Outline: Visitors should be able to go to "<expected_service>" page from the International page
    Given "Robert" visits the "International - Landing" page

    When "Robert" decides to find out more about "<service>"

    Then "Robert" should be on the "<expected_service>" page

    Examples:
      | service            | expected_service       |
      | Expand to the UK   | Invest - Home          |
      | Find a UK supplier | Find a Supplier - Home |

    @wip
    Examples: ATM there are no links to these services
      | service          | expected_service       |
      | Study in the UK  | British Council - Home |
      | Visit the UK     | Visit Britain - Home   |


  @ED-3149
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
      | 日本語              |

  @wip
    Examples: Missing translations
      | preferred_language |
      | 简体中文            |
      | Français           |
      | español            |
      | Português          |

  @bug
  @CMS-1263
  @fixme
    Examples: 500 ISE
      | preferred_language |
      | العربيّة            |


  @ED-3083
  @dev-only
  @language-selector
  Scenario: Visitor should be able to open and close the language selector on "International - Landing" page
    Given "Robert" visits the "International - Landing" page

    When "Robert" opens up the language selector
    Then "Robert" should see the language selector

    When "Robert" closes the language selector


  @ED-3083
  @dev-only
  @language-selector
  @accessibility
  Scenario: Keyboard users should be able to open and close the language selector using just the keyboard on "International - Landing" page
    Given "Robert" visits the "International - Landing" page

    When "Robert" opens up the language selector using his keyboard
    Then "Robert" should see the language selector

    When "Robert" closes the language selector using his keyboard


  @ED-3083
  @dev-only
  @language-selector
  @accessibility
  Scenario: Language selector should trap the keyboard in order to help Keyboard users to navigate on "International - Landing" pagee
    Given "Robert" visits the "International - Landing" page

    When "Robert" opens up the language selector using his keyboard
    And "Robert" uses his keyboard to navigate through all links visible on language selector

    Then "Robert"'s keyboard should be trapped to the language selector


  @ED-3149
  @wip
  @ED-3149
  @language-selector
  Scenario: Visitors should be able to "get advice and services to help them export" from International page
    Given "Robert" visits the "International - Landing" page

    When "Robert" decides to view the page in "English (UK)"

    Then "Robert" should be on the "Export Readiness - Home" page
