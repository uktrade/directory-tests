@case-studies
Feature: Case Studies


  @ED-2655
  @home-page
  Scenario Outline: Any Exporter should get to "<relevant>" case study from Case Studies carousel on the home page
    Given "Robert" visits the "Home" page

    When "Robert" goes to the "<relevant>" Case Study via carousel

    Then "Robert" should see "<relevant>" case study
    And "Robert" should see the Share Widget

    Examples:
      | relevant |
      | First    |
      | Second   |
      | Third    |


  @ED-2593
  @personalised-page
  @case-studies
  Scenario Outline: "<relevant>" Exporter should get to a "<selected>" case study from Case Studies carousel on the personalised journey page
    Given "Robert" was classified as "<relevant>" exporter in the triage process
    And "Robert" decided to create his personalised journey page

    When "Robert" goes to the "<selected>" Case Study via carousel

    Then "Robert" should see "<selected>" case study
    And "Robert" should see the Share Widget

    Examples:
      | relevant   | selected |
      | New        | First    |
      | Occasional | Second   |


  @ED-2593
  @personalised-page
  @case-studies
  Scenario Outline: "<relevant>" Exporter should not see Case Studies carousel on the personalised journey page
    Given "Robert" was classified as "<relevant>" exporter in the triage process

    When "Robert" decides to create her personalised journey page

    Then "Robert" should be on the Personalised Journey page for "<relevant>" exporters
    And "Robert" should not see "case studies" sections on "personalised journey" page

    Examples:
      | relevant |
      | Regular  |
