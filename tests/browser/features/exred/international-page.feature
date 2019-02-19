@international-page
Feature: International Page

  Background:
    Given hawk cookie is set on "Export Readiness - Home" page

  @ED-3114
  Scenario: Visitors should see "Buy from the UK, Invest in the UK, Study in the UK, Visit the UK" sections on the International page
    Given "Robert" visits the "Export Readiness - International" page

    Then "Robert" should see following sections
      | Sections              |
      | Header bar            |
      | Header menu           |
      | Service Cards         |
      | Tariffs               |
      | News                  |
      | Study or visit the UK |
#      | Beta bar          |
#      | EU Exit updates   |  # EU Exit feature is turned off


  @ED-3136
  @external-service
  @<expected_service>
  Scenario Outline: Visitors should be able to go to "<expected_service>" page from the International page
    Given "Robert" visits the "Export Readiness - International" page

    When "Robert" goes to "<expected_service>" using "<section>" link on "Export Readiness - International"

    Then "Robert" should be on the "<expected_service>" page

    Examples:
      | expected_service       | section          |
      | Invest - Home          | Invest in the UK |
      | British Council - Home | Study in the UK  |
      | Visit Britain - Home   | Visit the UK     |
      | Find a Supplier - Home | Buy from the UK  |


  @ED-3083
  @language-selector
  Scenario: Visitor should be able to open and close the language selector on "Export Readiness - International" page
    Given "Robert" visits the "Export Readiness - International" page

    When "Robert" opens up the language selector
    Then "Robert" should see the language selector

    When "Robert" closes the language selector
    Then "Robert" should not see the language selector


  @ED-3083
  @language-selector
  @accessibility
  Scenario: Keyboard users should be able to open and close the language selector using just the keyboard on "Export Readiness - International" page
    Given "Robert" visits the "Export Readiness - International" page

    When "Robert" opens up the language selector using his keyboard
    Then "Robert" should see the language selector

    When "Robert" closes the language selector using his keyboard
    Then "Robert" should not see the language selector


  @ED-3083
  @language-selector
  @accessibility
  Scenario: Language selector should trap the keyboard in order to help Keyboard users to navigat on "Export Readiness - International" pagee
    Given "Robert" visits the "Export Readiness - International" page

    When "Robert" opens up the language selector using his keyboard
    And "Robert" uses his keyboard to navigate through all links visible on language selector

    Then "Robert"'s keyboard should be trapped to the language selector


  @ED-3149
  @language-selector
  Scenario Outline: Visitors should be able to view International page in "<preferred_language>"
    Given "Robert" visits the "Export Readiness - International" page

    When "Robert" decides to view the page in "<preferred_language>"

    Then "Robert" should be on the "Export Readiness - International" page
    And "Robert" should see the page in "<preferred_language>"

    Examples: available languages
      | preferred_language |
      | English            |
      | 简体中文            |
      | Deutsch            |
      | 日本語              |
      | Español            |
      | Português          |
      | العربيّة            |


  @ED-3149
  @language-selector
  Scenario: Visitors should be able to "get advice and services to help them export" from International page
    Given "Robert" visits the "Export Readiness - International" page

    When "Robert" decides to view the page in "English (UK)"

    Then "Robert" should be on the "Export Readiness - Home" page
