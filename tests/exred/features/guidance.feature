@guidance
Feature: Guidance articles

  @ED-2463
  @home-page
  @articles
  @<specific>
  Scenario Outline: Any Exporter should get to a "<specific>" article list from Guidance section on the home page
    Given "Robert" visits the "Home" page for the first time

    When "Robert" goes to the "<specific>" Guidance articles via "home page"

    Then "Robert" should see an ordered list of all articles selected for "<specific>" category
    And "Robert" should see on the Guidance Articles page "Articles Read counter, Total number of Articles, Time to complete remaining chapters"
    And "Robert" should see a link to the "<next>" Guidance category

    Examples: Guidance categories
      | specific          | next              |
      | Market research   | Customer insight  |
      | Customer insight  | Finance           |
      | Finance           | Business planning |
      | Business planning | Getting paid      |
      | Getting paid      | last              |


  @ED-2464
  @home-page
  @articles
  Scenario Outline: Any Exporter should see article read count for "<specific>" Guidance category when accessed via home page
    Given "Robert" visits the "Home" page for the first time

    When "Robert" goes to the "<specific>" Guidance articles via "home page"

    Then "Robert" should see an article read counter for the "<specific>" Guidance category set to "0"
    And "Robert" should see total number of articles for the "<specific>" Guidance category

    Examples:
      | specific          |
      | Market research   |
      | Customer insight  |
      | Finance           |
      | Business planning |
      | Getting paid      |


  @ED-2465
  @personalised-page
  @articles
  @<relevant>
  @bug
  @ED-2508
  @fixme
  Scenario Outline: "<relevant>" Exporter should see Guidance Articles Read Counter on the personalised page
    Given "Nadia" classifies herself as "<relevant>" exporter

    When "Nadia" creates a personalised journey page for herself

    Then "Nadia" should see a Guidance Articles read counter for the "<relevant>" exporter

    Examples:
      | relevant   |
      | New        |
      | Occasional |


  @ED-2465
  @personalised-page
  @guidance
  @articles
  @regular
  @optimize
  Scenario Outline: Regular Exporter should see article read count for each tile in the Guidance section on the personalised page
    Given "Nadia" was classified as "regular" exporter in the triage process

    When "Nadia" goes to the "<specific>" Guidance articles via "personalised journey"

    Then "Nadia" should see an article read counter for the "<specific>" Guidance category set to "0"
    And "Nadia" should see total number of articles for the "<specific>" Guidance category

    Examples:
      | specific          |
      | Market research   |
      | Customer insight  |
      | Finance           |
      | Business planning |
      | Getting paid      |


  @ED-2466
  @personalised-page
  @articles
  @regular
  @optimize
  @<specific>
  Scenario Outline: Regular Exporter should see "<specific>" Guidance Articles accessed via personalised journey page
    Given "Nadia" was classified as "regular" exporter in the triage process

    When "Nadia" goes to the "<specific>" Guidance articles via "personalised journey"

    Then "Nadia" should see an ordered list of all articles selected for "<specific>" category
    And "Nadia" should see on the Guidance Articles page "Articles Read counter, Total number of Articles, Time to complete remaining chapters"
    And "Nadia" should see a link to the "<next>" Guidance category

    Examples: Guidance categories
      | specific          | next              |
      | Market research   | Customer insight  |
      | Customer insight  | Finance           |
      | Finance           | Business planning |
      | Business planning | Getting paid      |
      | Getting paid      | last              |


  @ED-2467
  @banner
  @<category>
  @<location>
  Scenario Outline: Guidance Banner should be visible when on "<category>" Guidance Article List accessed via "<location>"
    Given "Robert" accessed "<category>" guidance articles using "<location>"

    Then "Robert" should see the Guidance Navigation Ribbon
    And "Robert" should see that the banner tile for "<category>" category is highlighted

    Examples: header menu
      | category                  | location    |
      | Market research           | header menu |
      | Customer insight          | header menu |
      | Finance                   | header menu |
      | Business planning         | header menu |
      | Getting paid              | header menu |
      | Operations and Compliance | header menu |

    Examples: footer links
      | category                  | location     |
      | Market research           | footer links |
      | Customer insight          | footer links |
      | Finance                   | footer links |
      | Business planning         | footer links |
      | Getting paid              | footer links |
      | Operations and Compliance | footer links |

    Examples: home page
      | category                  | location  |
      | Market research           | home page |
      | Customer insight          | home page |
      | Finance                   | home page |
      | Business planning         | home page |
      | Getting paid              | home page |
      | Operations and Compliance | home page |
