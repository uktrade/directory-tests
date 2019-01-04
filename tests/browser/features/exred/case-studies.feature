@case-studies
Feature: Case Studies

  Background:
    Given hawk cookie is set on "Export Readiness - Home" page

  @ED-2655
  @home-page
  Scenario Outline: Any Exporter should get to "<relevant>" case study from Case Studies carousel on the home page
    Given "Robert" visits the "Export Readiness - Home" page

    When "Robert" goes to the "<relevant>" Case Study via carousel

    Then "Robert" should see "<relevant>" case study
    And "Robert" should see the Share Widget

    Examples:
      | relevant |
      | First    |
      | Second   |
      | Third    |
