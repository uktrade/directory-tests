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

    Then "Robert" should be on the "Triage - 1st question" page


  @ED-2366
  @triage
  @bug
  @ED-
  @fixme
  Scenario: Any Exporter visiting the home page after triage should be able to get to personalised page
    Given "Robert" has answered triage questions
    And "Robert" goes to the "Home" page

    When "Robert" decides to continue in Exporting journey section

    Then "Robert" should be on the "Personalised Journey" page


  @wip
  @ED-2366
  @personas
  @articles
  Scenario Outline: Any Exporter should get to a relevant article list from Personas section on the homepage
    Given "Robert" classifies himself as "<exporter_status>" exporter

    When "Robert" goes to the relevant "<exporter_status>" exporter link in the Personas section on the homepage

    Then "Robert" should see an ordered list of "previous + next 5" articles selected for "<exporter_status>" exporter
    And "Robert" should see a Articles Read counter, Total number of Articles and Time to complete remaining chapters

    Examples:
      | exporter_status |
      | New             |
      | Occasional      |
      | Regular         |
