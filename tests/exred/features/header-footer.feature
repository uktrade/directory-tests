Feature: Header-Footer


  @ED-3118
  @logo
  @header
  @footer
  Scenario Outline: Any Exporter should see correct DIT logo (with boat) in the page header and footer
    Given "Robert" visits the "<selected>" page

    Then "Robert" should be on the "<selected>" page
    And "Robert" should see correct DIT logo in page header

    Examples:
      | selected                            |
      | Home                                |
      | SSO registration                    |
      | SSO sign in                         |
      | SSO profile about                   |
      | Get finance                         |
      | Interim export opportunities        |
      | Triage - have you exported before   |
      | Find a Buyer                        |
#      | Find a Supplier                     |
#      | Events                              |


  @ED-3118
  @bug
  @ED-3116
  @fixme
  @logo
  @header
  @footer
  Scenario Outline: Any Exporter should see correct DIT logo (with boat) in the page header and footer
    Given "Robert" visits the "<selected>" page

    Then "Robert" should be on the "<selected>" page
    And "Robert" should see correct DIT logo in page header

    Examples:
      | selected                            |
      | Export Opportunities                |
      | Selling Online Overseas             |


  @ED-3091
  @favicon
  Scenario Outline: Any user should see the correct favicon on whichever page they're on
    Given "Robert" visits the "<specific>" page

    Then "Robert" should see the correct favicon

    Examples: Export Readiness pages
      | specific                            |
      | Home                                |
      | Triage - have you exported before   |
      | Interim export opportunities        |

    Examples: FABS pages
      | specific        |
      | Find a Buyer    |
      | Find a Supplier |

    Examples: SSO pages
      | specific          |
      | SSO Registration  |
      | SSO Sign in       |
      | SSO Profile about |

    Examples: SOO pages
      | specific                |
      | Selling Online Overseas |

    Examples: Export Opportunities
      | specific             |
      | Export Opportunities |


  @ED-3215
  @header
  @home-page
  @<specific>
  Scenario Outline: Any Exported should be able to get to the Domestic "<expected>" page via "<specific>" link in the "<selected section>"
    Given "Robert" visits the "Home" page for the first time

    When "Robert" goes to the "<specific>" page via "General" links in "<selected section>"

    Then "Robert" should be on the "<expected>" page

    Examples:
      | specific            | expected                   | selected section |
      | Home                | Home                       | header menu      |

    @bug
    @ED-3216
    @fixme
    Examples: failing examples
      | specific            | expected                   | selected section |
      | Your export journey | Create your export journey | header menu      |
      | Your export journey | Create your export journey | footer links     |


  @ED-3240
  @your-export-journey-link
  Scenario: Any user who visits the "Create your export journey" page for the first time, should be able to see all expected sections
    Given "Robert" visits the "Create your export journey" page for the first time

    Then "Robert" should see "Description, Start now, Save progress, Report this page" sections on "Create your export journey" page


  @ED-3261
  @bug
  @ED-3216
  @fixme
  @your-export-journey-link
  Scenario: Unauthenticated user should be prompted to sign in or to register on the "Create your export journey" page
    Given "Robert" visits the "Home" page for the first time

    When "Robert" decides to use "Your export journey" link in "header menu"

    Then "Robert" should be on the "Create your export journey" page
    And "Robert" should see "Save Progress" section on "Create your export journey" page


  @ED-3262
  @your-export-journey-link
  Scenario: Any user who visits the "Create your export journey" page for the first time, should be able to Start the journey (get to the first Triage question)
    Given "Robert" visits the "Create your export journey" page for the first time

    When "Robert" decides to use "Start now button" on "Create your export journey" page

    Then "Robert" should be on the "Triage - have you exported before" page


  @ED-3263
  @your-export-journey-link
  @session
  @fake-sso-email-verification
  Scenario: Any authenticated user should not be prompted to sign in or register on the "Create your export journey" page
    Given "Robert" is a registered and verified user
    And "Robert" is signed in
    And "Robert" went to the "Home" page

    When "Robert" goes to the "Create your export journey" page

    Then "Robert" should not see "Save Progress" section on "Create your export journey" page


  @ED-3283
  @your-export-journey-link
  @<specific>
  Scenario Outline: Any user who has created his/her "Personalised Journey page" should be able to return to it using "Your export journey" link
    Given "Robert" answered triage questions
    And "Robert" decided to create his personalised journey page
    And "Robert" is on the "Personalised Journey" page
    And "Robert" goes to the "<specific>" page

    When "Robert" decides to use "Your export journey" link in "header menu"

    Then "Robert" should be on the "Personalised Journey" page

    Examples:
      | specific                     |
      | Home                         |
      | Interim Export Opportunities |
      | Export Opportunities         |

    @bug
    @ED-3282
    @fixme
    Examples: header needs to be updated
      | specific                     |
      | Selling Online Overseas      |

    @bug
    @ED-3242
    @fixme
    Examples: header needs to be updated
      | specific                     |
      | Find a Buyer                 |


  @ED-3284
  @your-export-journey-link
  @<specific>
  Scenario Outline: Any user who has completed triage (without creating Personalised Journey page) should be redirected to "Create your export journey" page when using related header link
    Given "Robert" answered triage questions
    And "Robert" is on the "Triage - summary" page
    And "Robert" goes to the "<specific>" page

    When "Robert" decides to use "Your export journey" link in "header menu"

    Then "Robert" should be on the "Create your export journey" page

    Examples:
      | specific                     |
      | Home                         |
      | Interim Export Opportunities |
      | Export Opportunities         |

    @bug
    @ED-3282
    @fixme
    Examples: header needs to be updated
      | specific                     |
      | Selling Online Overseas      |

    @bug
    @ED-3242
    @fixme
    Examples: header needs to be updated
      | specific                     |
      | Find a Buyer                 |


  @ED-3285
  @your-export-journey-link
  Scenario Outline: "<relevant>" Exporter who has created his/her "Personalised Journey page" and hasn't signed-in should be asked to register or sign-in, in the Guidance section on the Personalised Journey page.
    Given "Robert" was classified as "<relevant>" exporter in the triage process

    When "Robert" decides to create his personalised journey page

    Then "Robert" should be on the "Personalised Journey" page
    And "Robert" should see "Save Progress" section on "Personalised Journey" page

    Examples:
      | relevant   |
      | New        |
      | Occasional |


  @bug
  @ED-3702
  @fixed
  @ED-3286
  @your-export-journey-link
  @fake-sso-email-verification
  Scenario: Any signed-in user who has created his/her "Personalised Journey page" should not be asked to register or sign-in, in the Guidance section on the Personalised Journey page.
    Given "Robert" is a registered and verified user
    And "Robert" is signed in
    And "Robert" answered triage questions

    When "Robert" decides to create his personalised journey page

    Then "Robert" should be on the "Personalised Journey" page
    And "Robert" should not see "Save Progress" section on "Personalised Journey" page


  @ED-3287
  @<group>
  @articles
  @your-export-journey-link
  Scenario Outline: Any user who has not signed-in should be asked to register or sign-in whilst being on the Article List page
    Given "Robert" is on the "<group>" Article List for randomly selected category

    Then "Robert" should see "Save Progress" section on "Article List" page

    Examples: article groups
      | group            |
      | Export Readiness |
      | Guidance         |


  @ED-3288
  @<group>
  @articles
  @your-export-journey-link
  Scenario Outline: Any user who has not signed-in should be asked to register or sign-in whilst being on the the Article page
    Given "Robert" is on the "<group>" Article List for randomly selected category
    And "Robert" shows all of the articles on the page whenever possible

    When "Robert" opens any article on the list

    Then "Robert" should see "Save Progress" section on "Article" page

    Examples: article groups
      | group            |
      | Export Readiness |
      | Guidance         |


  @ED-3289
  @<group>
  @articles
  @your-export-journey-link
  @fake-sso-email-verification
  Scenario Outline: Any user who signed in should not be told to Register or Sign-in whilst being on the Article List page
    Given "Robert" is a registered and verified user
    And "Robert" is signed in

    When "Robert" goes to randomly selected "<group>" Article category

    Then "Robert" should not see "Save Progress" section on "Article List" page

    Examples: article groups
      | group            |
      | Export Readiness |
      | Guidance         |


  @ED-3290
  @<group>
  @articles
  @your-export-journey-link
  @fake-sso-email-verification
  Scenario Outline: Any user who signed in should not be told to Register or Sign-in whilst being on the Article page
    Given "Robert" is a registered and verified user
    And "Robert" is signed in

    When "Robert" goes to randomly selected "<group>" Article category
    And "Robert" opens any article on the list

    Then "Robert" should not see "Save Progress" section on "Article" page

    Examples: article groups
      | group            |
      | Export Readiness |
      | Guidance         |
