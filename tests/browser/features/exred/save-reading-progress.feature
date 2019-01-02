@decommissioned
@articles
@session
Feature: Save reading progress

  Background:
    Given hawk cookie is set on "Export Readiness - Home" page

  @bug
  @ED-2807
  @fixed
  @ED-2706
  @real-sso-email-verification
  @<group>
  @<location>
  Scenario Outline: Any Exporter should be able to register via link in "<element>" present on the "<group>" Article list page, in order to save their progress
    Given "Robert" went to randomly selected "<group>" Article category via "Export Readiness - <location>"
    And "Robert" read "<number>" of articles
    And "Robert" is on the "Export Readiness - Article list" page

    When "Robert" decides to register to save his reading progress using link visible in the "<element>"
    And "Robert" completes the registration and real email verification process
    Then "Robert" should see his reading progress same as before registration

    When "Robert" signs out and forgets the article reading history by clearing the cookies
    And "Robert" goes to the "Export Readiness - home" page
    And "Robert" goes back to the same "<group>" Article category via "Export Readiness - <location>"
    Then "Robert" should see that his reading progress is gone

    When "Robert" signs in using link visible in the "top bar"
    Then "Robert" should see his reading progress same as before registration

    Examples:
      | group            | location | number    | element      |
      | Export Readiness | header   | a sixth   | article list |
      | Export Readiness | home     | a quarter | top bar      |
      | Export Readiness | footer   | a third   | article list |
      | Advice           | header   | a fifth   | top bar      |
      | Advice           | home     | a quarter | article list |
      | Advice           | footer   | a third   | top bar      |


  @bug
  @ED-2807
  @fixed
  @ED-2769
  @real-sso-email-verification
  Scenario Outline: An Exporter should be able to register via link in "<element>" present on the "<group>" Article page in order to save their progress
    Given "Robert" went to randomly selected "<group>" Article category via "Export Readiness - <location>"
    And "Robert" read "<a number>" of articles and stays on the last read article page
    And "Robert" is on the "Export Readiness - Article" page

    When "Robert" decides to register to save his reading progress using link visible in the "<element>"
    And "Robert" completes the registration and real email verification process
    Then "Robert" should see his reading progress same as before registration

    When "Robert" signs out and forgets the article reading history by clearing the cookies
    And "Robert" goes to the "Export Readiness - Home" page
    And "Robert" goes back to the same "<group>" Article category via "Export Readiness - <location>"
    Then "Robert" should see that his reading progress is gone

    When "Robert" signs in using link visible in the "top bar"
    Then "Robert" should see his reading progress same as before registration

    Examples:
      | group            | location | a number  | element |
      | Export Readiness | header   | a sixth   | article |
      | Export Readiness | home     | a quarter | top bar |
      | Export Readiness | footer   | a third   | article |
      | Advice           | header   | a fifth   | top bar |
      | Advice           | home     | a quarter | article |
      | Advice           | footer   | a third   | top bar |


  @bug
  @ED-2807
  @fixed
  @ED-2770
  @fake-sso-email-verification
  Scenario Outline: An Exporter should be able to sing in from the Articles list page using "<element>" Sign-in link in order to save their reading progress for "<group>" articles
    Given "Robert" is a registered and verified user
    And "Robert" went to the "Export Readiness - Home" page
    And "Robert" went to randomly selected "<group>" Article category via "Export Readiness - <location>"
    And "Robert" read "<a number>" of articles
    And "Robert" is on the "Export Readiness - Article list" page

    When "Robert" signs in using link visible in the "<element>"

    Then "Robert" should be on the "Export Readiness - Article List" page
    And "Robert" should see his reading progress same as before signing in

    Examples:
      | group            | location | a number  | element      |
      | Export Readiness | header   | a sixth   | article list |
      | Export Readiness | home     | a quarter | top bar      |
      | Export Readiness | footer   | a third   | article list |
      | Advice           | header   | a fifth   | top bar      |
      | Advice           | home     | a quarter | article list |
      | Advice           | footer   | a third   | top bar      |


  @bug
  @ED-2807
  @fixed
  @ED-2771
  @fake-sso-email-verification
  Scenario Outline: An Exporter should be able to sing in from the Article page using "<element>" Sign-in link in order to save their reading progress for "<group>" articles
    Given "Robert" is a registered and verified user
    And "Robert" went to the "Export Readiness - Home" page
    And "Robert" went to randomly selected "<group>" Article category via "Export Readiness - <location>"
    And "Robert" read "<a number>" of articles and stays on the last read article page
    And "Robert" is on the "Export Readiness - Article" page

    When "Robert" signs in using link visible in the "<element>"

    Then "Robert" should be on the "Export Readiness - Article" page
    And "Robert" should see his reading progress same as before signing in

    Examples:
      | group            | location | a number  | element |
      | Export Readiness | header   | a sixth   | article |
      | Export Readiness | home     | a quarter | top bar |
      | Export Readiness | footer   | a third   | article |
      | Advice           | header   | a fifth   | top bar |
      | Advice           | home     | a quarter | article |
      | Advice           | footer   | a third   | top bar |


  @ED-2772
  @<group>
  @<location>
  Scenario Outline: A logged in Exporter should not see the "Register" and "Sign in" links on Article page
    Given "Robert" is a registered and verified user
    And "Robert" is signed in
    And "Robert" went to the "Export Readiness - Home" page
    And "Robert" went to randomly selected "<group>" Article category via "Export Readiness - <location>"

    When "Robert" opens any article on the list

    Then "Robert" should not see the link to register on the "Export Readiness - Article" page
    And "Robert" should not see the link to sign in on the "Export Readiness - Article" page

    Examples:
      | group            | location |
      | Export Readiness | header   |
      | Advice           | home     |


  @ED-2772
  @<relevant>
  @<location>
  Scenario Outline: A logged in Exporter should not see the "Register" and "Sign in" links on Article List page
    Given "Robert" is a registered and verified user
    And "Robert" is signed in
    And "Robert" went to the "Export Readiness - Home" page

    When "Robert" goes to the Export Readiness Articles for "<relevant>" Exporters via "Export Readiness - <location>"

    Then "Robert" should not see the link to register on the "Export Readiness - Article List" page
    And "Robert" should not see the link to sign in on the "Export Readiness - Article List" page

    Examples:
      | relevant | location |
      | New      | header   |
      | Regular  | home     |


  @ED-2773
  @<group>
  @<location>
  Scenario Outline: Reading progress for signed in Exporter should be updated with temporary information, cookie data merged with persistent storage - Exporters reads "<a number>" of "<group>" articles accessed via "<location>" link
    Given "Robert" is a registered and verified user
    And "Robert" is signed in
    And "Robert" went to the "Export Readiness - Home" page
    And "Robert" went to randomly selected "<group>" Article category via "Export Readiness - <location>"
    And "Robert" read "<a number>" of articles and stays on the last read article page

    When "Robert" signs out
    And "Robert" goes to the "Export Readiness - Home" page
    And "Robert" goes back to the same "<group>" Article category via "Export Readiness - <location>"
    And "Robert" shows all of the articles on the page whenever possible
    And "Robert" opens any Article but the last one
    And "Robert" decides to read through all remaining Articles from selected list
    And "Robert" signs in

    Then "Robert" should be on the "Export Readiness - Article" page
    And "Robert"'s current reading progress should be merged with the one from before signing out without any overwriting

    Examples:
      | group            | location | a number  |
      | Export Readiness | header   | a sixth   |
      | Export Readiness | home     | a quarter |
      | Export Readiness | footer   | a third   |
      | Advice           | header   | a fifth   |
      | Advice           | home     | a quarter |
      | Advice           | footer   | a third   |


  @bug
  @CMS-192
  @fixed
  @ED-2773
  @<group>
  @<location>
  Scenario Outline: Reading progress for signed in Exporter should be updated with temporary information, cookie data merged with persistent storage, even after clearing the cookies - Exporters reads "<a number>" of "<group>" articles accessed via "<location>" link
    Given "Robert" is a registered and verified user
    And "Robert" is signed in
    And "Robert" went to the "Export Readiness - Home" page
    And "Robert" went to randomly selected "<group>" Article category via "Export Readiness - <location>"
    And "Robert" read "<a number>" of articles and stays on the last read article page

    When "Robert" signs out and forgets the article reading history by clearing the cookies
    And "Robert" goes to the "Export Readiness - Home" page
    And "Robert" goes back to the same "<group>" Article category via "Export Readiness - <location>"
    And "Robert" shows all of the articles on the page whenever possible
    And "Robert" opens any Article but the last one
    And "Robert" decides to read through all remaining Articles from selected list
    And "Robert" signs in

    Then "Robert" should be on the "Export Readiness - Article" page
    And "Robert"'s current reading progress should be merged with the one from before signing out without any overwriting

    Examples:
      | group            | location | a number  |
      | Export Readiness | header   | a sixth   |
      | Export Readiness | home     | a quarter |
      | Export Readiness | footer   | a third   |
      | Advice           | header   | a fifth   |
      | Advice           | home     | a quarter |
      | Advice           | footer   | a third   |
