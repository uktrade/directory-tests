@articles
Feature: Articles


  @ED-2606
  @guidance
  @articles
  @<category>
  Scenario Outline: Any Exporter accessing "<category>" Articles through the Guidance Article List should be able to navigate to the next article
    Given "Robert" accessed "<category>" guidance articles using "home page"
    And "Robert" opened first Article from the list

    When "Robert" decides to read through all Articles from selected list

    Then "Robert" should be able to navigate to the next article from the List following the Article Order

    Examples: home page
      | category                  |
      | Market research           |
      | Customer insight          |
      | Finance                   |
      | Business planning         |
      | Getting paid              |
      | Operations and Compliance |


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


  @ED-2605
  @progress
  @<group>
  Scenario Outline: Any Exporter should see his reading progress through the "<group>" articles list
    Given "Robert" is on the "<group>" Article List for randomly selected category

    When "Robert" opens any article on the list
    And "Robert" goes back to the Article List page

    Then "Robert" should see this article as read
    And "Robert" should see that Article Read Counter increased by "1"
    And "Robert" should see that Time to Complete remaining chapters decreased or remained unchanged for short articles

    Examples: article groups
      | group            |
      | Export Readiness |
      | Guidance         |


  @ED-2616
  @guidance
  @articles
  @<category>
  Scenario Outline: Any Exporter accessing the last Article from the Guidance Article "<category>" List should be able to navigate to the "<next>" Articles
    Given "Robert" accessed "<category>" guidance articles using "home page"
    And "Robert" opened any Article but the last one

    When "Robert" decides to read through all remaining Articles from selected list

    Then "Robert" should see a link to the fist article from the "<next>" category

    Examples:
      | category                  | next                      |
      | Market research           | Customer insight          |
      | Customer insight          | Finance                   |
      | Finance                   | Business planning         |
      | Business planning         | Getting paid              |
      | Getting paid              | Operations and Compliance |


  @ED-2616
  @guidance
  @articles
  @<category>
  Scenario Outline: Any Exporter accessing the last Article from the last Guidance Article category "<category>" should not see link to the next article
    Given "Robert" accessed "<category>" guidance articles using "home page"
    And "Robert" opened any Article but the last one

    When "Robert" decides to read through all remaining Articles from selected list

    Then "Robert" should not see the link to the next Article
    And "Robert" should not see the Personas End Page

    Examples:
      | category                  |
      | Operations and Compliance |


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


  @ED-2632
  @articles
  @<relevant>
  Scenario Outline: An Exporter classified as "<relevant>" in the Triage process should see a list of relevant articles on the personalised journey page
    Given "Robert" was classified as "<relevant>" exporter in the triage process

    When "Robert" decides to create his personalised journey page

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
    And "Robert" should see "Guidance" section on "personalised journey" page


  @ED-2638
  @triage
  @articles
  @<relevant>
  Scenario Outline: "<relevant>" Exporter accessing Guidance Articles through the Personalised Page should be able to navigate to the next article
    Given "Robert" was classified as "<relevant>" exporter in the triage process
    And "Robert" decided to create her personalised journey page

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
  Scenario Outline: Regular Exporter accessing "<specific>" Guidance Articles through the Personalised Page should be able to navigate to the next article
    Given "Robert" was classified as "regular" exporter in the triage process
    And "Robert" decided to create her personalised journey page

    When "Robert" goes to the "<specific>" Guidance Articles via "personalised journey"
    And "Robert" opens any Article but the last one
    And "Robert" decides to read through all remaining Articles from selected list

    Then "Robert" should be able to navigate to the next article from the List following the Article Order

    Examples:
      | specific          |
      | Market research   |
      | Customer insight  |
      | Finance           |
      | Business planning |
      | Getting paid      |


  @ED-2654
  @counters
  @<group>
  @<location>
  Scenario Outline: Article Indicators should be updated accordingly after opening "<group>" Article via "<location>"
    Given "Robert" went to randomly selected "<group>" Article category via "<location>"

    When "Robert" opens any article on the list

    Then "Robert" should see that Total number of Articles did not change
    And "Robert" should see that Article Read Counter increased by "1"
    And "Robert" should see that Time to Complete remaining chapters decreased or remained unchanged for short articles

    Examples:
      | group            | location     |
      | Export Readiness | header menu  |
      | Export Readiness | home page    |
      | Export Readiness | footer links |
      | Guidance         | header menu  |
      | Guidance         | home page    |
      | Guidance         | footer links |


  @ED-2654
  @counters
  @<relevant>
  Scenario Outline: Article Indicators should be updated accordingly after opening Export Readiness Article relevant to "<relevant>" Exporters
    Given "Robert" was classified as "<relevant>" exporter in the triage process
    And "Robert" decided to create her personalised journey page

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
      | relevant | group    | location             |
      | Regular  | Guidance | personalised journey |


  @ED-2640
  @sharing
  @<group>
  @<social_media>
  Scenario Outline: Any Exporter should be able to share the article via "<social_media>"
    Given "Robert" is on the "<group>" Article List for randomly selected category
    And "Robert" opened any Article

    When "Robert" decides to share the article via "<social_media>"

    Then "Robert" should be taken to a new tab with the "<social_media>" share page opened
    And "Robert" should that "<social_media>" share page has been pre-populated with message and the link to the article

    Examples:
      | group            | social_media |
      | Export Readiness | Facebook     |
      | Guidance         | Twitter      |
      | Export Readiness | LinkedIn     |


  @ED-2640
  @sharing
  @<group>
  @<social_media>
  Scenario Outline: Any Exporter should be able to share the article via "<social_media>"
    Given "Robert" is on the "<group>" Article List for randomly selected category
    And "Robert" opened any Article

    When "Robert" decides to share the article via "<social_media>"

    Then "Robert" should see that the share via email link will pre-populate the message subject and body with Article title and URL

    Examples:
      | group            | social_media |
      | Guidance         | email        |


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
