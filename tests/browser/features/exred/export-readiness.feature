@articles
@personas
@export-readiness
Feature: Export Readiness

  Background:
    Given hawk cookie is set on "Export Readiness - Home" page

  @ED-2613
  @personas
  @articles
  @<relevant>
  Scenario Outline: "<relevant>" Exporter accessing Articles through the Export Readiness Article List should be able to navigate to the next article
    Given "Robert" accessed Export Readiness articles for "<relevant>" Exporters via "Export Readiness - Home"
    And "Robert" shows all of the articles on the page whenever possible
    And "Robert" opened any Article but the last one

    When "Robert" decides to read through all remaining Articles from selected list

    Then "Robert" should be able to navigate to the next article from the List following the Article Order

    Examples:
      | relevant   |
      | New        |
      | Occasional |
      | Regular    |


  @ED-2628
  @articles
  @<relevant>
  @<location>
  Scenario Outline: "<relevant>" Exporter should see a list of relevant Export Readiness Articles when accessed via "<location>"
    Given "Robert" classifies himself as "<relevant>" exporter

    When "Robert" goes to the Export Readiness Articles for "<relevant>" Exporters via "Export Readiness - <location>"
    And "Robert" shows all of the articles on the page whenever possible

    Then "Robert" should see an ordered list of all Export Readiness Articles selected for "<relevant>" Exporters
    And "Robert" should see on the Export Readiness Articles page "Articles Read counter, Total number of Articles, Time to complete remaining chapters"

    Examples:
      | relevant   | location |
      | New        | Header   |
      | Occasional | Home     |
      | Regular    | Footer   |

    @full
    Examples:
      | relevant   | location |
      | Occasional | Header   |
      | Regular    | Header   |
      | New        | Home     |
      | Regular    | Home     |
      | New        | Footer   |
      | Occasional | Footer   |
