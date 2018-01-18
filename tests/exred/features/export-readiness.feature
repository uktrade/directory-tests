@articles
@personas
@export-readiness
Feature: Export Readiness


  @ED-2613
  @personas
  @articles
  @<relevant>
  Scenario Outline: "<relevant>" Exporter accessing Articles through the Export Readiness Article List should be able to navigate to the next article
    Given "Robert" accessed Export Readiness articles for "<relevant>" Exporters via "home page"
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

    When "Robert" goes to the Export Readiness Articles for "<relevant>" Exporters via "<location>"

    Then "Robert" should see an ordered list of all Export Readiness Articles selected for "<relevant>" Exporters
    And "Robert" should see on the Export Readiness Articles page "Articles Read counter, Total number of Articles, Time to complete remaining chapters"

    Examples:
      | relevant   | location      |
      | New        | header menu   |
      | Occasional | header menu   |
      | Regular    | header menu   |
      | New        | home page     |
      | Occasional | home page     |
      | Regular    | home page     |
      | New        | footer links  |
      | Occasional | footer links  |
      | Regular    | footer links  |
