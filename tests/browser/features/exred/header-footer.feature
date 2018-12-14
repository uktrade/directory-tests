Feature: Header-Footer

  Background:
    Given hawk cookie is set on "Export Readiness - Home" page

  @ED-3118
  @logo
  @header
  @footer
  Scenario Outline: Any Exporter should see correct DIT logo, one with the boat, in the page header and footer on "<selected>" page
    Given "Robert" visits the "<selected>" page

    Then "Robert" should see correct DIT logo in page header

    Examples:
      | selected                                        |
      | Export Readiness - Home                         |
      | Single Sign-On - Registration                   |
      | Single Sign-On - Sign in                        |
      | Single Sign-On - Profile about                  |
      | Export Readiness - Get finance                  |
      | Export Readiness - Interim export opportunities |
      | Export Readiness - Have you exported before     |
      | Find a Buyer - Home                             |
#      | Find a Supplier - Home                          |
#      | Events - Home                                   |


  @bug
  @ED-3116
  @fixed
  @logo
  @header
  @footer
  @ED-3118
  Scenario Outline: Any Exporter should see correct DIT logo, one with the boat, in the page header and footer on "<selected>" page
    Given "Robert" visits the "<selected>" page

    Then "Robert" should be on the "<selected>" page
    And "Robert" should see correct DIT logo in page header

    Examples:
      | selected                            |
      | Export Opportunities - Home         |
      | Selling Online Overseas - Home      |


  @ED-3587
  @logo
  @header
  @footer
  @ED-3118
  Scenario Outline: Any Exporter should be able to get to the Export Readiness Home page from "<selected>" page by using DIT logo in the page header and footer
    Given "Robert" visits the "<selected>" page

    When "Robert" decides to click on the DIT logo in the "header"

    Then "Robert" should be on the "Export Readiness - Home" page or on the International page

    Examples:
      | selected                                        |
      | Export Readiness - Home                         |
      | Single Sign-On - Registration                   |
      | Single Sign-On - Sign in                        |
      | Single Sign-On - Profile about                  |
      | Export Readiness - Get finance                  |
      | Export Readiness - Interim export opportunities |
      | Export Readiness - Have you exported before     |
      | Find a Buyer - Home                             |
      | Export Opportunities - Home                     |
#      | Selling Online Overseas - Home                  | There's no SOO DEV env


  @ED-3091
  @favicon
  Scenario Outline: Any user should see the correct favicon on "<specific>" page
    Given "Robert" visits the "<specific>" page

    Then "Robert" should see the correct favicon

    Examples: Export Readiness pages
      | specific                                        |
      | Export Readiness - Home                         |
      | Export Readiness - Have you exported before     |
      | Export Readiness - Interim export opportunities |

    Examples: FABS pages
      | specific               |
      | Find a Buyer - Home    |
      | Find a Supplier - Home |

    Examples: SSO pages
      | specific                       |
      | Single Sign-On - Registration  |
      | Single Sign-On - Sign in       |
      | Single Sign-On - Profile about |

    Examples: SOO pages
      | specific                       |
      | Selling Online Overseas - Home |

    Examples: Export Opportunities
      | specific                    |
      | Export Opportunities - Home |


  @bug
  @ED-3216
  @fixed
  @ED-3215
  @header
  @home-page
  @<specific>
  Scenario Outline: Any Exported should be able to get to the Domestic "<expected>" page via "<specific>" link in the "<selected section>"
    Given "Robert" visits the "Export Readiness - Home" page for the first time

    When "Robert" goes to the "<specific>" page via "General" links in "Export Readiness - <selected section>"

    Then "Robert" should be on the "<expected>" page or on the International page

    Examples:
      | specific            | expected                                      | selected section |
      | Home                | Export Readiness - Home                       | header           |
      | Your export journey | Export Readiness - Create your export journey | header           |
      | Your export journey | Export Readiness - Create your export journey | footer           |


  @ED-3240
  @your-export-journey-link
  Scenario: Any user who visits the "Create your export journey" page for the first time, should be able to see all expected sections
    Given "Robert" visits the "Export Readiness - Create your export journey" page for the first time

    Then "Robert" should see following sections
      | Sections         |
      | Description      |
      | Start now        |
      | Save progress    |
      | Report this page |


  @ED-3261
  @bug
  @ED-3216
  @fixed
  @your-export-journey-link
  Scenario: Unauthenticated user should be prompted to sign in or to register on the "Create your export journey" page
    Given "Robert" visits the "Export Readiness - Home" page for the first time

    When "Robert" decides to use "Your export journey" link in "Export Readiness - Header"

    Then "Robert" should be on the "Export Readiness - Create your export journey" page
    And "Robert" should see following sections
      | Sections      |
      | Save progress |


  @ED-3262
  @your-export-journey-link
  Scenario: Any user who visits the "Create your export journey" page for the first time, should be able to start the Triage
    Given "Robert" visits the "Export Readiness - Create your export journey" page for the first time

    When "Robert" decides to use "Start now" button

    Then "Robert" should be on the "Export Readiness - have you exported before" page


  @ED-3263
  @your-export-journey-link
  @session
  @fake-sso-email-verification
  Scenario: Any authenticated user should not be prompted to sign in or register on the "Create your export journey" page
    Given "Robert" is a registered and verified user
    And "Robert" is signed in
    And "Robert" went to the "Export Readiness - Home" page

    When "Robert" goes to the "Export Readiness - Create your export journey" page

    Then "Robert" should not see following section
      | section       |
      | Save Progress |


  @ED-3283
  @your-export-journey-link
  @<specific>
  Scenario Outline: Any user who has created his/her "Personalised Journey page" should be able to return to it using "Your export journey" link on "<specific>" page
    Given "Robert" answered triage questions
    And "Robert" decided to create his personalised journey page
    And "Robert" is on the "Export Readiness - Personalised Journey" page
    And "Robert" goes to the "<specific>" page

    When "Robert" decides to use "Your export journey" link in "Export Readiness - Header"

    Then "Robert" should be on the "Export Readiness - Personalised Journey" page

    Examples:
      | specific                                        |
      | Export Readiness - Home                         |
      | Export Readiness - Interim Export Opportunities |
      | Find a Buyer - Home                             |

    @bug
    @fixme
    Examples: invalid link to "Your export journey" on ExOpps site
      | specific                                        |
      | Export Opportunities - Home                     |

    @bug
    @ED-3282
    @fixme
    Examples: header needs to be updated
      | specific                       |
      | Selling Online Overseas - Home |


  @ED-3284
  @your-export-journey-link
  @<specific>
  Scenario Outline: Any user who has completed triage, without creating Personalised Journey page, should be redirected to "Create your export journey" page when using related header link
    Given "Robert" answered triage questions
    And "Robert" is on the "Export Readiness - Triage summary" page
    And "Robert" goes to the "<specific>" page

    When "Robert" decides to use "Your export journey" link in "Export Readiness - Header"

    Then "Robert" should be on the "Export Readiness - Create your export journey" page

    Examples:
      | specific                                        |
      | Export Readiness - Home                         |
      | Export Readiness - Interim Export Opportunities |
      | Find a Buyer - Home                             |

    @bug
    @fixme
    Examples: invalid link to "Your export journey" on ExOpps site
      | specific                                        |
      | Export Opportunities - Home                     |

    @bug
    @ED-3282
    @fixme
    Examples: header needs to be updated
      | specific                       |
      | Selling Online Overseas - Home |


  @ED-3285
  @your-export-journey-link
  Scenario Outline: "<relevant>" Exporters who have created their "Personalised Journey page" and have not signed-in should be asked to register or sign-in, in the Guidance section on the Personalised Journey page
    Given "Robert" was classified as "<relevant>" exporter in the triage process

    When "Robert" decides to create his personalised journey page

    Then "Robert" should be on the "Export Readiness - Personalised Journey" page
    And "Robert" should see following sections
      | Sections      |
      | Save progress |

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
  Scenario: Any signed-in user who has created his/her "Personalised Journey page" should not be asked to register or sign-in, in the Guidance section on the Personalised Journey page
    Given "Robert" is a registered and verified user
    And "Robert" is signed in
    And "Robert" answered triage questions

    When "Robert" decides to create his personalised journey page

    Then "Robert" should be on the "Export Readiness - Personalised Journey" page
    Then "Robert" should not see following section
      | section       |
      | Save Progress |


  @ED-3287
  @<group>
  @articles
  @your-export-journey-link
  Scenario Outline: Any user who has not signed-in should be asked to register or sign-in whilst being on the Article List page
    Given "Robert" is on the "<group>" Article List for randomly selected category

    Then "Robert" should see following section
      | Section       |
      | Save progress |

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

    Then "Robert" should see following section
      | Section       |
      | Save progress |

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

    Then "Robert" should not see following section
      | Section       |
      | Save progress |

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

    Then "Robert" should not see following section
      | Section       |
      | Save progress |

    Examples: article groups
      | group            |
      | Export Readiness |
      | Guidance         |
