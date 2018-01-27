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
      | Triage - what do you want to export |
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
      | Triage - what do you want to export |
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

    Then "Robert" should be on the "Triage - what do you want to export" page


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
  @your-export-journey-link
  Scenario: Any user who signed in should not be asked to register or sign in in the Guidance section of the custom page.
    Given "Robert" is not a registered user
    When "Robert" visits the "Custom" page
    Then "Robert" should not see registration text in the "Guidance" section


  @wip
  @ED-2737
  @your-export-journey-link
  Scenario: Any user who hasn’t signed in should be asked to register in the article pages
    Given "Robert" is not a registered user
    When "Robert" visits any "Article" page
    Then "Robert" should see registration text


  @wip
  @ED-2737
  @your-export-journey-link
  Scenario: Any user who signed in should not be told to register in article pages
    Given "Robert" is a registered user
    When "Robert" visits any "Article" page
    Then "Robert" should not see registration text
