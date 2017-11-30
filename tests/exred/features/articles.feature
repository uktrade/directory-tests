@articles
Feature: Articles


  @ED-2606
  @guidance
  @articles
  @<category>
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
  Scenario Outline: Any Exporter should see his progress through the articles list
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
    When "Robert" opens any Article but the last one
    And "Robert" decides to read through all remaining Articles from selected list

    Then "Robert" should be able to navigate to the next article from the List following the Article Order

    Examples:
      | specific          |
      | Market research   |
      | Customer insight  |
      | Finance           |
      | Business planning |
      | Getting paid      |


  @ED-2639
  @feedback
  Scenario Outline: Any Exporter should be able to tell us that they "<found_or_not>" the "<group>" article useful
    Given "Robert" is on the "<group>" Article List for randomly selected category
    And "Robert" opened any Article

    When "Robert" decides to tell us that he "<found_or_not>" this article useful

    Then feedback widget should disappear
    And "Robert" should be thanked for his feedback

    Examples: article groups
      | group            | found_or_not  |
      | Export Readiness | found         |
      | Guidance         | haven't found |


  @ED-2639
  @feedback
  @<relevant>
  Scenario Outline: "<relevant>" Exporters should be able to tell us that they "<found_or_not>" the article relevant to them useful
    Given "Robert" was classified as "<relevant>" exporter in the triage process
    And "Robert" decided to create her personalised journey page
    And "Robert" opened any Article

    When "Robert" decides to tell us that he "<found_or_not>" this article useful

    Then feedback widget should disappear
    And "Robert" should be thanked for his feedback

    Examples:
      | relevant   | found_or_not  |
      | New        | found         |
      | Occasional | haven't found |


  @ED-2639
  @feedback
  @<relevant>
  Scenario Outline: "<relevant>" Exporters should be able to tell us that they "<found_or_not>" the "<group>" article useful
    Given "Robert" was classified as "<relevant>" exporter in the triage process
    And "Robert" decided to create her personalised journey page
    And "Robert" went to randomly selected Guidance Articles category
    And "Robert" opened any Article

    When "Robert" decides to tell us that he "<found_or_not>" this article useful

    Then feedback widget should disappear
    And "Robert" should be thanked for his feedback

    Examples:
      | relevant | found_or_not  |
      | Regular  | found         |
      | Regular  | haven't found |



  @ED-2654
  @counters
  @<group>
  @<location>
  Scenario Outline: Article Indicators should be updated accordingly after opening "<group>" Article
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


  @bug
  @ED-2807
  @fixme
  @ED-2706
  @session
  @register
  @real-sso-email-verification
  @<group>
  @<location>
  Scenario Outline: Any Exporter should be able to register from the "<group>" Articles list page in order to save their progress
    Given "Robert" went to randomly selected "<group>" Article category via "<location>"
    And "Robert" read "<number>" of articles
    And "Robert" is on the "Article list" page

    When "Robert" decides to register to save his reading progress using link visible in the "<element>"
    And "Robert" completes the registration and real email verification process
    Then "Robert" should see his reading progress same as before registration

    When "Robert" logs out and forgets the article reading history by clearing the cookies
    And "Robert" goes to the "home" page
    And "Robert" goes back to the same "<group>" Article category via "<location>"
    Then "Robert" should see that his reading progress is gone

    When "Robert" signs in using link visible in the "top bar"
    Then "Robert" should see his reading progress same as before registration

    Examples:
      | group            | location     | number    | element      |
      | Export Readiness | header menu  | a sixth   | article list |
      | Export Readiness | home page    | a quarter | top bar      |
      | Export Readiness | footer links | a third   | article list |
      | Guidance         | header menu  | a fifth   | top bar      |
      | Guidance         | home page    | a quarter | article list |
      | Guidance         | footer links | a third   | top bar      |


  @bug
  @ED-2807
  @fixme
  @ED-2769
  @session
  @register
  @real-sso-email-verification
  Scenario Outline: An Exporter should be able to register from the Article page in order to save their progress
    Given "Robert" went to randomly selected "<group>" Article category via "<location>"
    And "Robert" read "<a number>" of articles and stays on the last read article page
    And "Robert" is on the "Article" page

    When "Robert" decides to register to save his reading progress using link visible in the "<element>"
    And "Robert" completes the registration and real email verification process
    Then "Robert" should see his reading progress same as before registration

    When "Robert" logs out and forgets the article reading history by clearing the cookies
    And "Robert" goes to the "home" page
    And "Robert" goes back to the same "<group>" Article category via "<location>"
    Then "Robert" should see that his reading progress is gone

    When "Robert" signs in using link visible in the "top bar"
    Then "Robert" should see his reading progress same as before registration

    Examples:
      | group            | location     | a number  | element |
      | Export Readiness | header menu  | a sixth   | article |
      | Export Readiness | home page    | a quarter | top bar |
      | Export Readiness | footer links | a third   | article |
      | Guidance         | header menu  | a fifth   | top bar |
      | Guidance         | home page    | a quarter | article |
      | Guidance         | footer links | a third   | top bar |


  @bug
  @ED-2807
  @fixme
  @ED-2770
  @session
  Scenario Outline: An Exporter should be able to sing in from the Articles list page using "<element>" Sign-in link in order to save their reading progress for "<group>" articles
    Given "Robert" is a registered and verified user
    And "Robert" went to the "Home" page
    And "Robert" went to randomly selected "<group>" Article category via "<location>"
    And "Robert" read "<a number>" of articles
    And "Robert" is on the "Article list" page

    When "Robert" signs in using link visible in the "<element>"

    Then "Robert" should be on the "Article List" page
    And "Robert" should see his reading progress same as before signing in

    Examples:
      | group            | location     | a number  | element      |
      | Export Readiness | header menu  | a sixth   | article list |
      | Export Readiness | home page    | a quarter | top bar      |
      | Export Readiness | footer links | a third   | article list |
      | Guidance         | header menu  | a fifth   | top bar      |
      | Guidance         | home page    | a quarter | article list |
      | Guidance         | footer links | a third   | top bar      |


  @bug
  @ED-2807
  @fixme
  @ED-2771
  @session
  Scenario Outline: An Exporter should be able to sing in from the Article page using "<element>" Sign-in link in order to save their reading progress for "<group>" articles
    Given "Robert" is a registered and verified user
    And "Robert" went to the "Home" page
    And "Robert" went to randomly selected "<group>" Article category via "<location>"
    And "Robert" read "<a number>" of articles and stays on the last read article page
    And "Robert" is on the "Article" page

    When "Robert" signs in using link visible in the "<element>"

    Then "Robert" should be on the "Article" page
    And "Robert" should see his reading progress same as before signing in

    Examples:
      | group            | location     | a number  | element |
      | Export Readiness | header menu  | a sixth   | article |
      | Export Readiness | home page    | a quarter | top bar |
      | Export Readiness | footer links | a third   | article |
      | Guidance         | header menu  | a fifth   | top bar |
      | Guidance         | home page    | a quarter | article |
      | Guidance         | footer links | a third   | top bar |


  @wip
  @ED-2772
  @session
  Scenario: A logged in Exporter should not see the "Register" and "Sign in" links on Article page
    Given "Robert" is signed in
    And "Robert" is on the specific Article page

    Then "Robert"'s should not see the link to register
    And "Robert"'s should not see the link to sign in


  @wip
  @ED-2772
  @session
  Scenario: A logged in Exporter should not see the "Register" and "Sign in" links on Article List page
    Given "Robert" is signed in
    And "Robert" is on the specific Article List page

    Then "Robert"'s should not see the link to register
    And "Robert"'s should not see the link to sign in


  @wip
  @ED-2773
  @session
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
  @ED-2640
  @sharing
  Scenario Outline: Any Exporter should be able to share the article via Facebook, Twitter, Linked and email on the article page
    Given "Robert" is on the "<group>" Article List for randomly selected category
    And "Robert" opened any Article

    When "Robert" decides to share the article via "<social_media>"

    Then "Robert" should be taken to a new tab with the "<sharing_option>" opened and pre-populated message with the link to the article

    Examples:
      | group            | sharing_option |
      | Export Readiness | Facebook       |
      | Guidance         | Twitter        |
      | Export Readiness | LinkedIn       |
      | Guidance         | email          |


  @wip
  @ED-2774
  @out-of-scope
  @tasks
  Scenario: Any Exporter should see his task completion progress on the articles list page
    Given "Robert" is on the Article page

    When "Robert" marks any task as completed
    And "Robert" goes back to the Article List page

    Then "Robert" should see the tasks completed counter increased by 1


  @wip
  @ED-2774
  @out-of-scope
  @tasks
  Scenario: Any Exporter should see his task completion progress on the article page
    Given "Robert" is on the Article page
    And "Robert" marks any task as completed
    And "Robert" went back to the Article List page

    When "Robert" views the same article

    Then "Robert" should see the tasks he already marked as completed


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
