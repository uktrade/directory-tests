@case-studies
Feature: Domestic - Case Studies

  Background:
    Given basic authentication is done for "Domestic - Home" page

  @ED-2655
  @home-page
  Scenario Outline: Any Exporter should get to "<relevant>" case study from home page
    Given "Robert" visits the "Domestic - Home" page

    When "Robert" goes to the "<relevant>" Case Study

    Then "Robert" should see "<relevant>" case study
    And "Robert" should see the Share Widget

    Examples:
      | relevant |
      | First    |
      | Second   |
