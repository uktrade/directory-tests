@decommissioned
@articles
Feature: Articles

  Background:
    Given hawk cookie is set on "Export Readiness - Home" page

  @ED-2606
  @advice
  @articles
  @<category>
  Scenario Outline: Any Exporter accessing "<category>" Articles through the Advice Article List should be able to navigate to the next article
    Given "Robert" accessed "<category>" advice articles using "Export Readiness - Home"
    And "Robert" opened first Article from the list

    When "Robert" decides to read through all Articles from selected list

    Then "Robert" should be able to navigate to the next article from the List following the Article Order

    Examples: Advice Articles
      | category                  |
      | Market research           |
      | Customer insight          |
      | Finance                   |

    @full
    Examples: Advice Articles
      | category                  |
      | Business planning         |
      | Getting paid              |
      | Operations and Compliance |


  @ED-2605
  @progress
  @<group>
  Scenario Outline: Any Exporter should see his reading progress through the "<group>" articles list
    Given "Robert" is on the "<group>" Article List for randomly selected category
    And "Robert" shows all of the articles on the page whenever possible

    When "Robert" opens any article on the list
    And "Robert" goes back to the Article List page
    And "Robert" shows all of the articles on the page whenever possible

    Then "Robert" should see this article as read
    And "Robert" should see that Article Read Counter increased by "1"
    And "Robert" should see that Time to Complete remaining chapters decreased or remained unchanged for short articles

    Examples: article groups
      | group            |
      | Export Readiness |
      | Advice           |


  @ED-2616
  @advice
  @articles
  @<category>
  Scenario Outline: Any Exporter accessing the last Article from the Advice Article "<category>" List should be able to navigate to the "<next>" Articles
    Given "Robert" accessed "<category>" advice articles using "Export Readiness - Home"
    And "Robert" opened any Article but the last one

    When "Robert" decides to read through all remaining Articles from selected list

    Then "Robert" should see a link to the fist article from the "<next>" category

    Examples:
      | category          | next                      |
      | Market research   | Customer insight          |
      | Customer insight  | Finance                   |
      | Finance           | Business planning         |

    @full
    Examples:
      | category          | next                      |
      | Business planning | Getting paid              |
      | Getting paid      | Operations and Compliance |


  @ED-2616
  @advice
  @articles
  @<category>
  Scenario Outline: Any Exporter accessing the last Article from the last Advice Article category "<category>" should not see link to the next article
    Given "Robert" accessed "<category>" advice articles using "Export Readiness - Home"
    And "Robert" opened any Article but the last one

    When "Robert" decides to read through all remaining Articles from selected list

    Then "Robert" should not see the link to the next Article
    And "Robert" should not see the Personas End Page

    Examples:
      | category                  |
      | Operations and Compliance |


  @ED-2632
  @articles
  @<relevant>
  Scenario Outline: An Exporter classified as "<relevant>" in the Triage process should see a list of relevant articles on the personalised journey page
    Given "Robert" was classified as "<relevant>" exporter in the triage process

    When "Robert" decides to create his personalised journey page
    And "Robert" shows all of the articles on the page whenever possible

    Then "Robert" should see an ordered list of all Export Readiness Articles selected for "<relevant>" Exporters
    And "Robert" should see on the Export Readiness Articles page "Articles Read counter, Total number of Articles, Time to complete remaining chapters"

    Examples:
      | relevant   |
      | New        |
      | Occasional |


  @ED-2632
  @articles
  @regular
  Scenario: An Exporter classified as "Regular" in the Triage process should see a list of relevant articles on the personalised journey page
    Given "Robert" was classified as "Regular" exporter in the triage process

    When "Robert" decides to create his personalised journey page

    Then "Robert" should be on the Personalised Journey page for "regular" exporters
    And "Robert" should see following sections
      | Sections |
      | Advice   |


  @ED-2638
  @triage
  @articles
  @<relevant>
  Scenario Outline: "<relevant>" Exporter accessing Advice Articles through the Personalised Page should be able to navigate to the next article
    Given "Robert" was classified as "<relevant>" exporter in the triage process
    And "Robert" decided to create her personalised journey page
    And "Robert" shows all of the articles on the page whenever possible

    When "Robert" opens any Article but the last one
    And "Robert" decides to read through all remaining Articles from selected list

    Then "Robert" should be able to navigate to the next article from the List following the Article Order

    Examples:
      | relevant   |
      | New        |
      | Occasional |


  @ED-2638
  @triage
  @articles
  @regular
  Scenario Outline: Regular Exporter accessing "<specific>" Advice Articles through the Personalised Page should be able to navigate to the next article
    Given "Robert" was classified as "regular" exporter in the triage process
    And "Robert" decided to create her personalised journey page

    When "Robert" goes to the "<specific>" Advice Articles via "Export Readiness - Personalised Journey"
    And "Robert" opens any Article but the last one
    And "Robert" decides to read through all remaining Articles from selected list

    Then "Robert" should be able to navigate to the next article from the List following the Article Order

    Examples:
      | specific          |
      | Market research   |
      | Customer insight  |

    @full
    Examples:
      | specific          |
      | Finance           |
      | Business planning |
      | Getting paid      |


  @ED-2654
  @counters
  @<group>
  @<location>
  Scenario Outline: Article Indicators should be updated accordingly after opening "<group>" Article via "<location>"
    Given "Robert" went to randomly selected "<group>" Article category via "Export Readiness - <location>"
    And "Robert" shows all of the articles on the page whenever possible

    When "Robert" opens any article on the list

    Then "Robert" should see that Total number of Articles did not change
    And "Robert" should see that Article Read Counter increased by "1"
    And "Robert" should see that Time to Complete remaining chapters decreased or remained unchanged for short articles

    Examples:
      | group            | location |
      | Export Readiness | header   |
      | Export Readiness | home     |
      | Export Readiness | footer   |
      | Advice           | header   |
      | Advice           | home     |
      | Advice           | footer   |


  @ED-2654
  @counters
  @<relevant>
  Scenario Outline: Article Indicators should be updated accordingly after opening Export Readiness Article relevant to "<relevant>" Exporters
    Given "Robert" was classified as "<relevant>" exporter in the triage process
    And "Robert" decided to create her personalised journey page
    And "Robert" shows all of the articles on the page whenever possible

    When "Robert" opens any article on the list

    Then "Robert" should see that Total Number of Articles did not change
    And "Robert" should see that Article Read Counter increased by "1"
    And "Robert" should see that Time to Complete remaining chapters decreased or remained unchanged for short articles

    Examples:
      | relevant   |
      | New        |
      | Occasional |


  @ED-2654
  @counters
  @<group>
  @<relevant>
  @<location>
  Scenario Outline: Article Indicators should be updated accordingly after opening "<group>" Article relevant to "<relevant>" Exporters
    Given "Robert" was classified as "<relevant>" exporter in the triage process
    And "Robert" decided to create her personalised journey page
    And "Robert" went to randomly selected "<group>" Article category via "<location>"

    When "Robert" opens any article on the list

    Then "Robert" should see that Total number of Articles did not change
    And "Robert" should see that Article Read Counter increased by "1"
    And "Robert" should see that Time to Complete remaining chapters decreased or remained unchanged for short articles

    Examples:
      | relevant | group  | location                                |
      | Regular  | Advice | Export Readiness - Personalised Journey |


  @wip
  @ED-2775
  @out-of-scope
  @triage
  @articles
  Scenario Outline: Any Exporter that reads through all the Articles specific to his Persona should be presented with a dedicated Persona End Page
    Given "Robert" was classified as "<specific>" exporter in the triage process
    And "Robert" opens any Article from the Personalised Page which is not the last one
    And "Robert" navigates through Articles

    When "Robert" reaches the last Article from the List of Articles for "<specific>" Persona

    Then "Robert" should see the End Page for "<specific>" Persona
    And "Robert" should not see the link to the next Article

    Examples:
      | specific   |
      | New        |
      | Occasional |
      | Regular    |
