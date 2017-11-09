@triage
Feature: Triage

  @ED-2520
  @first-time
  @regular
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


  @ED-2520
  @first-time
  @regular
  Scenario: Not incorporated Regular Exporter visiting the home page for the 1st time should be able to get to personalised page after going through triage process
    Given "Nadia" visits the "Home" page for the first time
    And "Nadia" decided to build her exporting journey

    When "Nadia" says what does she wants to export
    And "Nadia" says that she "has" exported before
    And "Nadia" says that exporting is "a regular" part of her business
    And "Nadia" says that her company "is not" incorporated
    And "Nadia" sees the summary page with answers to the questions she was asked
    And "Nadia" can see that she was classified as a "regular" exporter
    And "Nadia" decides to create her personalised journey page

    Then "Nadia" should be on the personalised "regular" exporter journey page


  @ED-2521
  @first-time
  @occasional
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


  @ED-2521
  @first-time
  @occasional
  Scenario Outline: Not incorporated Occasional Exporter visiting the home page for the 1st time should be able to get to personalised page after going through triage process
    Given "Inigo" visits the "home" page for the first time
    And "Inigo" decided to build his exporting journey

    When "Inigo" says what does she wants to export
    And "Inigo" says that she "has" exported before
    And "Inigo" says that exporting is "not a regular" part of her business
    And "Inigo" says that she "<online_action>" used online marketplaces
    And "Inigo" says that her company "is not" incorporated
    And "Inigo" sees the summary page with answers to the questions he was asked
    And "Inigo" can see that she was classified as a "occasional" exporter
    And "Inigo" decides to create her personalised journey page

    Then "Inigo" should be on the personalised "occasional" exporter journey page

    Examples:
      | online_action |
      | has           |
      | has never     |


  @ED-2522
  @first-time
  @new
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


  @ED-2522
  @first-time
  @new
  Scenario: Not incorporated New Exporter visiting the home page for the 1st time should be able to get to personalised page after going through triage process
    Given "Jonah" visits the "home" page for the first time
    And "Jonah" decided to build his exporting journey

    When "Jonah" says what does he wants to export
    And "Jonah" says that he "has never" exported before
    And "Jonah" says that his company "is not" incorporated
    And "Jonah" sees the summary page with answers to the questions he was asked
    And "Jonah" can see that he was classified as a "new" exporter
    And "Jonah" decides to create his personalised journey page

    Then "Jonah" should be on the personalised "new" exporter journey page


  @ED-2523
  @first-time
  @<specific>
  Scenario Outline: "<specific>" Exporter should be able to change their answers to at the end of triage
    Given "Robert" was classified as "<specific>" exporter in the triage process

    When "Robert" decides to change his answers

    Then "Robert" should be able to answer the triage questions again with his previous answers pre-populated

    Examples: classifications
      | specific   |
      | New        |
      | Occasional |
      | Regular    |
