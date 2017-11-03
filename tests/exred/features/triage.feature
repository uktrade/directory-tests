@triage
Feature: Triage

  @ED-2520
  @first-time
  Scenario Outline: Regular Exporter visiting the home page for the 1st time should be able to get to personalised page after going through triage process
    Given "Nadia" visits the "Home" page for the first time
    And "Nadia" decided to build her exporting journey

    When "Nadia" says what does she wants to export
    And "Nadia" says that she "has" exported before
    And "Nadia" says that exporting is "a regular" part of her business
    And "Nadia" says that her company "is" incorporated
    And "Nadia" "<company_name_action>" her company name
    And "Nadia" sees the summary page with answers to the questions she was asked
    And "Nadia" can see that she was classified as a "regular" exporter
    And "Nadia" decides to create her personalised journey page

    Then "Nadia" should be on the personalised "regular" exporter journey page

    Examples:
      | company_name_action  |
      | types in             |
      | does not provide     |
      | types in and selects |


  @wip
  @ED-2521
  @first-time
  Scenario Outline: Occasional Exporter visiting the home page for the 1st time should be able to get to personalised page after going through triage process
    Given "Inigo" visits the "home" page for the first time
    And "Inigo" decided to build his exporting journey

    When "Inigo" says what does she wants to export
    And "Inigo" says that she "has" exported before
    And "Inigo" says that exporting is "not a regular" part of her business
    And "Inigo" says that she "<online_action>" used online marketplaces
    And "Inigo" says that her company "is" incorporated
    And "Inigo" "<company_name_action>" his company name
    And "Inigo" sees the summary page with answers to the questions he was asked
    And "Inigo" can see that she was classified as a "occasional" exporter
    And "Inigo" decides to create her personalised journey page

    Then "Inigo" should be on the personalised "occasional" exporter journey page

    Examples:
      | online_action | company_name_action  |
      | has           | types in             |
      | has never     | types in             |
      | has           | does not provide     |
      | has never     | does not provide     |
      | has           | types in and selects |
      | has never     | types in and selects |


  @wip
  @ED-2522
  @first-time
  Scenario Outline: New Exporter visiting the home page for the 1st time should be able to get to personalised page after going through triage process
    Given "Jonah" visits the "home" page for the first time
    And "Jonah" decided to build his exporting journey

    When "Jonah" says what does he wants to export
    And "Jonah" says that he "has never" exported before
    And "Jonah" says that his company "is" incorporated
    And "Jonah" "<company_name_action>" his company name
    And "Jonah" sees the summary page with answers to the questions he was asked
    And "Jonah" can see that he was classified as a "new" exporter
    And "Jonah" decides to create his personalised journey page

    Then "Jonah" should be on the personalised "new" exporter journey page

    Examples:
      | company_name_action  |
      | types in             |
      | does not provide     |
      | types in and selects |


  @wip
  @ED-2523
  @first-time
  Scenario: Any Exporter should be able to change their answers to at the end of triage
    Given "Robert" visits the home page for the first time
    And "Robert" answered triage questions

    When "Robert" decides to change his answers

    Then "Robert" should be able to answer the triage questions again with his previous answers pre-populated


  @wip
  @ED-2524
  @sole-trader
  Scenario: Sole Trader visiting the home page for the 1st time should be able asked for Company name if he is not registered with companies house
    Given "Robert" is in triage
    And "Robert" said that his company "is not" incorporated

    Then "Robert" should not be asked for his Company name
    And "Robert" should be presented with the summary page with answers to the questions he asked


  @wip
  @ED-2525
  @sole-trader
  Scenario: Sole Trader visiting the home page for the 1st time should be able to get to personalised page after going through triage process
    Given "Robert" is in triage
    And "Robert" said that his company "is not" incorporated
    And "Robert" sees the summary page with answers to the questions he was asked
    And "Robert" decides to create his personalised journey page

    Then "Robert" should be on the personalised journey page


  @wip
  @ED-2526
  @classification
  Scenario Outline: Triaging should help to identify "new exporter"
    Given "Jonah" visits the "home" page for the first time
    And "Jonah" decided to build his exporting journey

    When "Jonah" says what does he wants to export
    And "Jonah" says that he "has never" exported before
    And "Jonah" says that his company "is" incorporated
    And "Jonah" "<company_name_action>" his company name


    Then "Nadia" should see the summary page with answers to the questions she was asked
    And "Nadia" should be classified as "new" exporter

    Examples:
      | company_name_action  |
      | types in             |
      | does not provide     |
      | types in and selects |


  @wip
  @ED-2527
  @first-time
  Scenario Outline: New Exporter visiting the home page for the 1st time should be able to get to personalised page after going through triage process
    Given "Jonah" visits the "home" page for the first time
    And "Jonah" decided to build his exporting journey

    When "Jonah" says what does he wants to export
    And "Jonah" says that he "has never" exported before
    And "Jonah" says that his company "is" incorporated
    And "Jonah" "<company_name_action>" his company name
    And "Jonah" sees the summary page with answers to the questions he was asked
    And "Jonah" can see that he was classified as a "new" exporter
    And "Jonah" decides to create his personalised journey page

    Then "Jonah" should be on the personalised "new" exporter journey page

    Examples:
      | company_name_action  |
      | types in             |
      | does not provide     |
      | types in and selects |


  @wip
  @ED-2528
  @classification
  Scenario Outline: Triaging should help to identify "occasional exporter"
    Given "Inigo" visits the "home" page for the first time
    And "Inigo" decided to build his exporting journey

    When "Inigo" says what does she wants to export
    And "Inigo" says that she "has" exported before
    And "Inigo" says that exporting is "not a regular" part of her business
    And "Inigo" says that she "<online_action>" used online marketplaces
    And "Inigo" says that her company "is" incorporated
    And "Inigo" "<company_name_action>" her company name


    Then "Inigo" should see the summary page with answers to the questions she was asked
    And "Inigo" should be classified as "occasional" exporter

    Examples:
      | online_action | company_name_action  |
      | has           | types in             |
      | has never     | types in             |
      | has           | does not provide     |
      | has never     | does not provide     |
      | has           | types in and selects |
      | has never     | types in and selects |
