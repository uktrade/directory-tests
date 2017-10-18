@home-page
Feature: Home Page


  @ED-2366
  @sections
  Scenario: Any Exporter should see the "Video, Exporting Journey, Personas, Guidance, Services, Case Studies" sections on the home page.
      Given "Robert" visits the "Home" page
      Then "Robert" should see the "Video, Exporting Journey, Personas, Guidance, Services, Case Studies" sections


  @ED-2366
  @triage
  Scenario: Any Exporter visiting the home page should be able to get to triage
    Given "Robert" visits the "Home" page for the first time

    When "Robert" decides to get started in Exporting journey section

    Then "Robert" should be on the "Triage - 1st question" page
