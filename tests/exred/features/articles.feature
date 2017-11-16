@articles
Feature: Articles


  @ED-2606
  @guidance
  @articles
  Scenario Outline: Any Exporter accessing Articles through the Guidance Article List should be able to navigate to the next article
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


  @wip
  @ED-2605
  Scenario: Any Exporter should see his progress through the articles list
    Given "Robert" is on the Article List page

    When "Robert" views any article on the list
    And "Robert" goes back to the Article List page

    Then "Robert" should see this article as read (ticked)
    And Chapters read counter should increase by 1
    And Time to complete remaining chapters should decrease


  @ED-2616
  @guidance
  @articles
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
  Scenario Outline: Any Exporter accessing the last Article from the last Guidance Article category "<category>" should not see link to the next article
    Given "Robert" accessed "<category>" guidance articles using "home page"
    And "Robert" opened any Article but the last one

    When "Robert" decides to read through all remaining Articles from selected list

    Then "Robert" should not see the link to the next Article
    And "Robert" should not see the Personas End Page

    Examples:
      | category                  |
      | Operations and Compliance |


  @wip
  @articles
  Scenario Outline: Any Exporter should see relevant article list from "<link_location>"
    Given "Robert" classifies himself as "<specific>" exporter

    When "Robert" goes to the relevant "<specific>" exporter link from "<link_location>"

    Then "Robert" should see an ordered list of first 5 articles selected for "<exporter_status>" exporter
    And "Robert" should see a Articles Read counter, Total number of Articles, Time to complete remaining chapters, Tasks completed counter and task Total number

    Examples:
      | specific   | link_location |
      | New        | header menu   |
      | Occasional | header menu   |
      | Regular    | header menu   |
      | New        | page body     |
      | Occasional | page body     |
      | Regular    | page body     |
      | New        | footer links  |
      | Occasional | footer links  |
      | Regular    | footer links  |


  @wip
  @articles
  Scenario Outline:  A triaged Exporter should see relevant article list on the customised page
    Given "Robert" was classified as "<relevant>" exporter in the triage process

    When "Robert" goes to the personalised page

    Then "Robert" should see an ordered list of "first 5" articles selected for "<exporter_status>" exporter
    And "Robert" should see a Articles Read counter, Total number of Articles, Time to complete remaining chapters, Tasks completed counter and task Total number

    Examples:
      | relevant   |
      | New        |
      | Occasional |
      | Regular    |


  @wip
  @articles
  Scenario Outline: Any Exporter should be able to get to the relevant article list using link from "<link_location>"
    Given "Robert" classifies himself as "<exporter_status>" exporter
    And "Robert" is on the Articles list page

    When "Robert" decides to show more articles

    Then "Robert" should see an ordered list of "previous + next 5" articles selected for "<exporter_status>" exporter
    And "Robert" should see a Articles Read counter, Total number of Articles, Time to complete remaining chapters, Tasks completed counter and task Total number

    Examples:
      | exporter_status | link_location |
      | New             | header menu   |
      | Occasional      | header menu   |
      | Regular         | header menu   |
      | New             | page body     |
      | Occasional      | page body     |
      | Regular         | page body     |
      | New             | footer links  |
      | Occasional      | footer links  |
      | Regular         | footer links  |


  @wip
  @articles
  Scenario Outline: A triaged Exporter should be able to show more relevant articles on the customised page
    Given "Robert" was classified as "<relevant>" exporter in the triage process
    And "Robert" is on the "Personalised Journey" page

    When "Robert" decides to show more articles

    Then "Robert" should see an ordered list of "previous + next 5" articles selected for "<exporter_status>" exporter
    And "Robert" should see a Articles Read counter, Total number of Articles, Time to complete remaining chapters, Tasks completed counter and task Total number

    Examples:
      | relevant   |
      | New        |
      | Occasional |
      | Regular    |


  @wip
  Scenario: An Exporter should be able to register from the Articles list page in order to save their progress
    Given "Robert" is on the Article List page
    And "Robert" read some of the articles

    When "Robert" decides to "register"
    And "Robert" completes registration and email verification process
    And "Robert" signs in

    Then "Robert"'s current progress should be saved


  @wip
  Scenario: An Exporter should be able to sing in from the Articles list page in order to save their progress
    Given "Robert" is on the Article List page
    And "Robert" read some of the articles

    When "Robert" decides to "sign in"
    And "Robert" signs in

    Then "Robert"'s current progress should be saved


  @wip
  Scenario: An Exporter should be able to register from the specific Article page in order to save their progress
    Given "Robert" read some of the articles
    And "Robert" is on the specific Article page

    When "Robert" decides to "register"
    And "Robert" completes registration and email verification process
    And "Robert" signs in

    Then "Robert"'s current progress should be saved


  @wip
  Scenario: A logged in Exporter should not see the register link on Article page
    Given "Robert" is signed in
    And "Robert" is on the specific Article page

    Then "Robert"'s should not see the link to register


  @wip
  Scenario: A logged in Exporter should not see the register link on Article List page
    Given "Robert" is signed in
    And "Robert" is on the specific Article List page

    Then "Robert"'s should not see the link to register


  @wip
  Scenario: An Exporter should be able to sign in from the specific Article page in order to save their progress
    Given "Robert" read some of the articles
    And "Robert" is on the specific Article page

    When "Robert" decides to "sign in"
    And "Robert" signs in

    Then "Robert"'s current progress should be saved


  @wip
  Scenario: A signed in Exporter's progress should be updated with temporary information (cookie data merged with persistent storage)
    Given "Robert" is signed in
    And "Robert" reads some articles
    And "Robert" completes some tasks
    And "Robert"'s current progress is saved

    When "Robert" decides to "sign out"
    And "Robert" reads some more articles
    And "Robert" completes some more tasks
    And "Robert" decides to "sign in"

    Then "Robert"'s current progress should be updated without overwriting (merged / accumulated)


  @wip
  Scenario Outline: Article read counter on the specific Article page and Articles list page should be the same
    Given "Robert" accessed the article list from "<link_location>"

    When "Robert" views any article on that list

    Then "Robert" should see the same "Articles Read counter, Total number of Articles, Time to complete remaining chapters" as on the Articles list page

    Examples:
      | link_location             |
      | header menu               |
      | home page body            |
      | personalised journey page |
      | footer links              |


  @wip
  Scenario: Any Exporter should see his task completion progress on the articles list page
    Given "Robert" is on the Article page

    When "Robert" marks any task as completed
    And "Robert" goes back to the Article List page

    Then "Robert" should see the tasks completed counter increased by 1


  @wip
  Scenario: Any Exporter should see his task completion progress on the article page
    Given "Robert" is on the Article page
    And "Robert" marks any task as completed
    And "Robert" went back to the Article List page

    When "Robert" views the same article

    Then "Robert" should see the tasks he already marked as completed


  @articles
  @wip
  Scenario Outline: Any Exporter should be able to tell us whether they found the article useful or not
    Given "Robert" is on the Article page

    When "Robert" decides to tell us that he "<article_feedback_action>" this article useful

    Then "Robert" feedback widget should disappear
    And "Robert" should thanked for his feeback

    Examples:
      | article_feedback_action |
      | found                   |
      | did not find            |
  @wip
  @triage
  @articles
  Scenario Outline: Any Exporter accessing Articles through the Triage should be able to navigate to the next article for his Persona
    Given "Robert" was classified as "<specific>" exporter in the triage process

    When "Robert" opens any Article from the Personalised Page which is not the last one

    Then "Robert" should be able to navigate to the next article from the List following the Article Order for "<exporting_status>" Persona
    And "Robert" should not see any Articles that are not relevant to his "<exporting_status>" Persona

    Examples:
      | specific   |
      | New        |
      | Occasional |


  @wip
  @triage
  @articles
  Scenario Outline: Any Exporter that reads through all the Articles specific to his Persona should be presented with a dedicated Persona End Page
    Given "Robert" was classified as "<specific>" exporter in the triage process
    And "Robert" opens any Article from the Personalised Page which is not the last one
    And "Robert" navigates through Articles

    When "Robert" reaches the last Article from the List of Articles for "<exporting_status>" Persona

    Then "Robert" should see the End Page for "<exporting_status>" Persona
    And "Robert" should not see the link to the next Article

    Examples:
      | specific   |
      | New        |
      | Occasional |


  @wip
  Scenario Outline: Any Exporter should be able to share the article via Facebook, Twitter, Linked and email on the article page
    Given "Robert" is on the Article page
    And "Robert" decides to share the article via "<sharing_option>"

    Then "Robert" should be taken to a new tab with the "<sharing_option>" opened and pre-populated message with the link to the article

    Examples:
      | sharing_option |
      | Facebook       |
      | Twitter        |
      | Linked         |
      | email          |
