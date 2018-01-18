@articles
@session
Feature: Save reading progress

  @bug
  @ED-2807
  @fixed
  @ED-2706
  @real-sso-email-verification
  @<group>
  @<location>
  Scenario Outline: Any Exporter should be able to register via link in "<element>" present on the "<group>" Article list page, in order to save their progress
    Given "Robert" went to randomly selected "<group>" Article category via "<location>"
    And "Robert" read "<number>" of articles
    And "Robert" is on the "Article list" page

    When "Robert" decides to register to save his reading progress using link visible in the "<element>"
    And "Robert" completes the registration and real email verification process
    Then "Robert" should see his reading progress same as before registration

    When "Robert" signs out and forgets the article reading history by clearing the cookies
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
  @fixed
  @ED-2769
  @real-sso-email-verification
  Scenario Outline: An Exporter should be able to register via link in "<element>" present on the "<group>" Article page in order to save their progress
    Given "Robert" went to randomly selected "<group>" Article category via "<location>"
    And "Robert" read "<a number>" of articles and stays on the last read article page
    And "Robert" is on the "Article" page

    When "Robert" decides to register to save his reading progress using link visible in the "<element>"
    And "Robert" completes the registration and real email verification process
    Then "Robert" should see his reading progress same as before registration

    When "Robert" signs out and forgets the article reading history by clearing the cookies
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
  @fixed
  @ED-2770
  @fake-sso-email-verification
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
  @fixed
  @ED-2771
  @fake-sso-email-verification
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


  @ED-2772
  @<group>
  @<location>
  Scenario Outline: A logged in Exporter should not see the "Register" and "Sign in" links on Article page
    Given "Robert" is a registered and verified user
    And "Robert" is signed in
    And "Robert" went to the "Home" page
    And "Robert" went to randomly selected "<group>" Article category via "<location>"

    When "Robert" opens any article on the list

    Then "Robert" should not see the link to register on the "Article" page
    And "Robert" should not see the link to sign in on the "Article" page

    Examples:
      | group            | location    |
      | Export Readiness | header menu |
      | Guidance         | home page   |


  @ED-2772
  @<relevant>
  @<location>
  Scenario Outline: A logged in Exporter should not see the "Register" and "Sign in" links on Article List page
    Given "Robert" is a registered and verified user
    And "Robert" is signed in
    And "Robert" went to the "Home" page

    When "Robert" goes to the Export Readiness Articles for "<relevant>" Exporters via "<location>"

    Then "Robert" should not see the link to register on the "Article List" page
    And "Robert" should not see the link to sign in on the "Article List" page

    Examples:
      | relevant | location    |
      | New      | header menu |
      | Regular  | home page   |


  @ED-2773
  @<group>
  @<location>
  Scenario Outline: A signed in Exporter's progress should be updated with temporary information (cookie data merged with persistent storage)
    Given "Robert" is a registered and verified user
    And "Robert" is signed in
    And "Robert" went to the "Home" page
    And "Robert" went to randomly selected "<group>" Article category via "<location>"
    And "Robert" read "<a number>" of articles and stays on the last read article page

    When "Robert" signs out
    And "Robert" goes to the "Home" page
    And "Robert" goes back to the same "<group>" Article category via "<location>"
    And "Robert" opens any Article but the last one
    And "Robert" decides to read through all remaining Articles from selected list
    And "Robert" signs in

    Then "Robert" should be on the "Article" page
    And "Robert"'s current reading progress should be merged with the one from before signing out without any overwriting

    Examples:
      | group            | location     | a number  |
      | Export Readiness | header menu  | a sixth   |
      | Export Readiness | home page    | a quarter |
      | Export Readiness | footer links | a third   |
      | Guidance         | header menu  | a fifth   |
      | Guidance         | home page    | a quarter |
      | Guidance         | footer links | a third   |


  @ED-2773
  @<group>
  @<location>
  Scenario Outline: A signed in Exporter's progress should be updated with temporary information (cookie data merged with persistent storage)
    Given "Robert" is a registered and verified user
    And "Robert" is signed in
    And "Robert" went to the "Home" page
    And "Robert" went to randomly selected "<group>" Article category via "<location>"
    And "Robert" read "<a number>" of articles and stays on the last read article page

    When "Robert" signs out and forgets the article reading history by clearing the cookies
    And "Robert" goes to the "Home" page
    And "Robert" goes back to the same "<group>" Article category via "<location>"
    And "Robert" shows all of the articles on the page
    And "Robert" opens any Article but the last one
    And "Robert" decides to read through all remaining Articles from selected list
    And "Robert" signs in

    Then "Robert" should be on the "Article" page
    And "Robert"'s current reading progress should be merged with the one from before signing out without any overwriting

    Examples:
      | group            | location     | a number  |
      | Export Readiness | header menu  | a sixth   |
      | Export Readiness | home page    | a quarter |
      | Export Readiness | footer links | a third   |
      | Guidance         | header menu  | a fifth   |
      | Guidance         | home page    | a quarter |
      | Guidance         | footer links | a third   |
