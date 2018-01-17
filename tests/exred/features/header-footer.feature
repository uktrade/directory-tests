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
  @home-page
  @<specific-page>
  Scenario Outline: Any Exported should be able to get to the Domestic Home page via Home link in the header menu
    Given "Robert" visits the "Home" page

    When "Robert" goes to the "<specific>" page via "General" links in header menu

    Then "Robert" should be on the "<expected>" page

    Examples:
      | specific            | expected                   |
      | Home                | Home                       |

    @bug
    @ED-3216
    @fixme
    Examples:
      | specific            | expected                   |
      | Your export journey | Create your export journey |


  @wip
  @ED-2737
  @custom-link
  Scenario: Any user should be able to get to "your export journey" from the header
    Given "Robert" has not completed the triage questions
    And "Robert" is a registered user
    When "Robert" goes to his export journey via appropriate header link
    Then "Robert" should be on the "Start your export journey" page


  @wip
  @ED-2737
  @custom-link
  Scenario: Any user should be able to get to "your export journey" from the footer
    Given "Robert" has not completed the triage questions
    And "Robert" is a registered user
    When "Robert" goes to his export journey via appropriate header link
    Then "Robert" should be on the "Start your export journey" page


  @wip
  @ED-2737
  @custom-link
  Scenario: Any user  who has not completed triage should create their export journey from the "Your export journey" page
    Given "Robert" is on the "Your export journey" page and "Robert" has not completed triage before
    Then "Robert" should see the "Start your export journey" section


  @wip
  @ED-2737
  @custom-link
  Scenario: Any user who is not signed be prompted to sign in on the "start your journey" page
    Given "Robert" is not signed in
    When "Robert" visits the "Start your export journey" page
    Then "Robert" should be asked to sign in or register in the "your export journey" section


  @wip
  @ED-2737
  @custom-link
  Scenario: Any user who is not signed be prompted to sign in on the "home" page
    Given "Robert" is not signed in
    When "Robert" visits the "Start your export journey" page
    Then "Robert" should be asked to sign in or register in the  home page "create export journey" section


  @wip
  @ED-2737
  @custom-link
  Scenario: Any user who has completed triage should be able to get to the custom page from the header
    Given "Robert" has completed the triage questions
    When "Robert" goes to his export journey via appropriate header link
    Then "Robert" should be on the "Custom" page


  @wip
  @ED-2737
  @custom-link
  Scenario: Any user who hasn’t signed in should be asked to register or sign in, in the Guidance section of the custom page.
    Given "Robert" is not a registered user
    When "Robert" visits the "Custom" page
    Then "Robert" should see registration text in the "Guidance" section


  @wip
  @ED-2737
  @custom-link
  Scenario: Any user who signed in should not be asked to register or sign in in the Guidance section of the custom page.
    Given "Robert" is not a registered user
    When "Robert" visits the "Custom" page
    Then "Robert" should not see registration text in the "Guidance" section


  @wip
  @ED-2737
  @custom-link
  Scenario: Any user who hasn’t signed in should be asked to register in the article pages
    Given "Robert" is not a registered user
    When "Robert" visits any "Article" page
    Then "Robert" should see registration text


  @wip
  @ED-2737
  @custom-link
  Scenario: Any user who signed in should not be told to register in article pages
    Given "Robert" is a registered user
    When "Robert" visits any "Article" page
    Then "Robert" should not see registration text
