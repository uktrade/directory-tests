@advice
Feature: Advice articles

  Background:
    Given hawk cookie is set on "Export Readiness - Home" page

  @ED-2463
  @home-page
  @articles
  @<specific>
  Scenario Outline: Any Exporter should get to a "<specific>" article list from Advice section on the home page
    Given "Robert" visits the "Export Readiness - Home" page for the first time

    When "Robert" goes to the "<specific>" Advice articles via "Export Readiness - Home"

    Then "Robert" should see an ordered list of all Advice Articles selected for "<specific>" category
    And "Robert" should see on the Advice Articles page "Articles Read counter, Total number of Articles, Time to complete remaining chapters"
    And "Robert" should see a link to the "<next>" Advice category

    Examples: Advice categories
      | specific          | next              |
      | Market research   | Customer insight  |
      | Customer insight  | Finance           |

    @full
    Examples: Advice categories
      | specific          | next              |
      | Finance           | Business planning |
      | Business planning | Getting paid      |
      | Getting paid      | last              |


  @ED-2464
  @home-page
  @articles
  Scenario Outline: Any Exporter should see article read count for "<specific>" Advice category when accessed via home page
    Given "Robert" visits the "Export Readiness - Home" page for the first time

    When "Robert" goes to the "<specific>" Advice articles via "Export Readiness - Home"

    Then "Robert" should see an article read counter for the "<specific>" Advice category set to "0"
    And "Robert" should see total number of articles for the "<specific>" Advice category

    Examples:
      | specific          |
      | Market research   |
      | Customer insight  |
      | Finance           |
      | Business planning |
      | Getting paid      |


  @ED-2465
  @personalised-page
  @advice
  @articles
  @regular
  @optimize
  Scenario Outline: Regular Exporter should see article read count for each tile in the "<specific>" Advice section on the personalised page
    Given "Nadia" was classified as "regular" exporter in the triage process
    And "Nadia" decided to create her personalised journey page

    When "Nadia" goes to the "<specific>" Advice articles via "Export Readiness - Personalised Journey"

    Then "Nadia" should see an article read counter for the "<specific>" Advice category set to "0"
    And "Nadia" should see total number of articles for the "<specific>" Advice category

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
  Scenario Outline: Regular Exporter should see "<specific>" Advice Articles accessed via personalised journey page
    Given "Nadia" was classified as "regular" exporter in the triage process
    And "Nadia" decided to create her personalised journey page

    When "Nadia" goes to the "<specific>" Advice articles via "Export Readiness - Personalised Journey"

    Then "Nadia" should see an ordered list of all Advice Articles selected for "<specific>" category
    And "Nadia" should see on the Advice Articles page "Articles Read counter, Total number of Articles, Time to complete remaining chapters"
    And "Nadia" should see a link to the "<next>" Advice category

    Examples: Advice categories
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
  Scenario Outline: Advice Banner should be visible when on "<category>" Advice Article List accessed via "<location>"
    Given "Robert" accessed "<category>" advice articles using "Export Readiness - <location>"

    Then "Robert" should see the Advice Navigation Ribbon
    And "Robert" should see that the banner tile for "<category>" category is highlighted

    Examples: header menu
      | category                  | location |
      | Market research           | header   |
      | Customer insight          | header   |
      | Finance                   | header   |
      | Business planning         | header   |
      | Getting paid              | header   |
      | Operations and Compliance | header   |

    Examples: footer links
      | category                  | location |
      | Market research           | footer   |
      | Customer insight          | footer   |
      | Finance                   | footer   |
      | Business planning         | footer   |
      | Getting paid              | footer   |
      | Operations and Compliance | footer   |

    Examples: home page
      | category                  | location |
      | Market research           | home     |
      | Customer insight          | home     |
      | Finance                   | home     |
      | Business planning         | home     |
      | Getting paid              | home     |
      | Operations and Compliance | home     |
