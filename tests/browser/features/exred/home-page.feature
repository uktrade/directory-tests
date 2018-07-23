@home-page
Feature: Home Page


  @ED-2366
  @sections
  Scenario: Any Exporter should see the "Beta, Hero, Exporting Journey, Export Readiness, Guidance, Services, Case Studies, Business is Great, Error Reporting" sections on the home page.
      Given "Robert" visits the "Export Readiness - Home" page
      Then "Robert" should see following sections
        | Sections          |
        | Beta              |
        | Hero              |
        | Exporting Journey |
        | Export Readiness  |
        | Guidance          |
        | Services          |
        | Case Studies      |
        | Business is Great |
        | Error Reporting   |


  @new-triage
  @ED-2366
  @triage
  Scenario: Any Exporter visiting the home page should be able to get to triage
    Given "Robert" visits the "Export Readiness - Home" page for the first time

    When "Robert" decides to get started in Exporting journey section

    Then "Robert" should be on the "Export Readiness - Have you exported before" page


  @ED-2366
  @triage
  Scenario: Any Exporter visiting the home page after triage should be able to get to personalised page
    Given "Robert" answered triage questions
    And "Robert" decided to create his personalised journey page
    And "Robert" is on the "Export Readiness - Personalised Journey" page
    And "Robert" goes to the "Export Readiness - Home" page

    When "Robert" decides to continue in Exporting journey section

    Then "Robert" should be on the "Export Readiness - Personalised Journey" page


  @ED-2366
  @personas
  @articles
  @<specific>
  Scenario Outline: "<specific>" Exporter should be able to get to a relevant Export Readiness Article List from Export Readiness section on the home page
    Given "Robert" classifies himself as "<specific>" exporter

    When "Robert" goes to the Export Readiness Articles for "<specific>" Exporters via "Export Readiness - Home"
    And "Robert" shows all of the articles on the page whenever possible

    Then "Robert" should see an ordered list of all Export Readiness Articles selected for "<specific>" Exporters
    And "Robert" should see on the Export Readiness Articles page "Articles Read counter, Total number of Articles, Time to complete remaining chapters"

    Examples:
      | specific   |
      | New        |
      | Occasional |
      | Regular    |


  @ED-3014
  @video
  Scenario: Any Exporter should be able to play promotional video on the Home page
    Given "Robert" visits the "Export Readiness - Home" page

    When "Robert" decides to watch "6" seconds of the promotional video

    Then "Robert" should be able to watch at least first "5" seconds of the promotional video


  @ED-3014
  @video
  Scenario: Any Exporter should be able to close the window with promotional video on the Home page
    Given "Robert" visits the "Export Readiness - Home" page

    When "Robert" decides to watch "6" seconds of the promotional video
    And "Robert" closes the window with promotional video

    Then "Robert" should not see the window with promotional video


  @ED-3083
  @language-selector
  Scenario: Visitor should be able to open and close the language selector
    Given "Robert" visits the "Export Readiness - Home" page

    When "Robert" opens up the language selector
    Then "Robert" should see the language selector

    When "Robert" closes the language selector
    Then "Robert" should not see the language selector


  @ED-3083
  @language-selector
  @accessibility
  Scenario: Keyboard users should be able to open and close the language selector using just the keyboard
    Given "Robert" visits the "Export Readiness - Home" page

    When "Robert" opens up the language selector using his keyboard
    Then "Robert" should see the language selector

    When "Robert" closes the language selector using his keyboard
    Then "Robert" should not see the language selector


  @ED-3083
  @language-selector
  @accessibility
  Scenario: Language selector should trap the keyboard in order to help Keyboard users to navigate
    Given "Robert" visits the "Export Readiness - Home" page

    When "Robert" opens up the language selector using his keyboard
    And "Robert" uses his keyboard to navigate through all links visible on language selector

    Then "Robert"'s keyboard should be trapped to the language selector


  @ED-3083
  @language-selector
  Scenario Outline: Visitors should be able to view go to International page after changing language to "<preferred_language>" on the Domestic Home Page
    Given "Robert" visits the "Export Readiness - Home" page

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