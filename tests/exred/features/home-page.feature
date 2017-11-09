@home-page
Feature: Home Page


  @ED-2366
  @sections
  Scenario: Any Exporter should see the "Video, Exporting Journey, Personas, Guidance, Services, Case Studies" sections on the home page.
      Given "Robert" visits the "Home" page
      Then "Robert" should see the "Video, Exporting Journey, Personas, Guidance, Services, Case Studies" sections on Home page


  @ED-2366
  @triage
  Scenario: Any Exporter visiting the home page should be able to get to triage
    Given "Robert" visits the "Home" page for the first time

    When "Robert" decides to get started in Exporting journey section

    Then "Robert" should be on the "Triage - what do you want to export" page


  @ED-2366
  @triage
  Scenario: Any Exporter visiting the home page after triage should be able to get to personalised page
    Given "Robert" answered triage questions
    And "Robert" decided to create his personalised journey page
    And "Robert" goes to the "Home" page

    When "Robert" decides to continue in Exporting journey section

    Then "Robert" should be on the "Personalised Journey" page


  @ED-2366
  @personas
  @articles
  @<specific>
  Scenario Outline: "<specific>" Exporter should be able to get to a relevant Export Readiness Article List from Personas section on the home page
    Given "Robert" classifies himself as "<specific>" exporter

    When "Robert" goes to the Export Readiness Articles for "<specific>" Exporters via "home page"

    Then "Robert" should see an ordered list of all Export Readiness Articles selected for "<specific>" Exporters
    And "Robert" should see on the Export Readiness Articles page "Articles Read counter, Total number of Articles, Time to complete remaining chapters"

    Examples:
      | specific   |
      | New        |
      | Occasional |
      | Regular    |
