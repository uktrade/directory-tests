@articles
@feedback
Feature: Feedback (tell us why)

  Background:
    Given hawk cookie is set on "Export Readiness - Home" page

  @ED-2639
  Scenario Outline: Any Exporter should be able to tell us that they "<found_or_not>" the "<group>" article useful
    Given "Robert" is on the "<group>" Article List for randomly selected category
    And "Robert" opened any Article

    When "Robert" decides to tell us that he "<found_or_not>" this article useful

    Then feedback widget should disappear
    And "Robert" should be thanked for his feedback

    Examples: article groups
      | group            | found_or_not  |
      | Export Readiness | found         |
      | Advice           | haven't found |


  @ED-2639
  @<relevant>
  Scenario Outline: "<relevant>" Exporters should be able to tell us that they "<found_or_not>" the article relevant to them useful
    Given "Robert" was classified as "<relevant>" exporter in the triage process
    And "Robert" decided to create her personalised journey page
    And "Robert" shows all of the articles on the page whenever possible
    And "Robert" opened any Article

    When "Robert" decides to tell us that he "<found_or_not>" this article useful

    Then feedback widget should disappear
    And "Robert" should be thanked for his feedback

    Examples:
      | relevant   | found_or_not  |
      | New        | found         |
      | Occasional | haven't found |


  @ED-2639
  @<relevant>
  Scenario Outline: "<relevant>" Exporters should be able to tell us that they "<found_or_not>" the article useful
    Given "Robert" was classified as "<relevant>" exporter in the triage process
    And "Robert" decided to create her personalised journey page
    And "Robert" went to randomly selected Advice Articles category
    And "Robert" opened any Article

    When "Robert" decides to tell us that he "<found_or_not>" this article useful

    Then feedback widget should disappear
    And "Robert" should be thanked for his feedback

    Examples:
      | relevant | found_or_not  |
      | Regular  | found         |
      | Regular  | haven't found |
