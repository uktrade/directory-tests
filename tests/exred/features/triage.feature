@triage
Feature: Triage

  @new-triage
  @ED-2520
  @first-time
  @regular
  Scenario Outline: Regular Exporter visiting the home page for the 1st time should be able to get to personalised page after going through triage process
    Given "Nadia" visits the "Home" page for the first time
    And "Nadia" decided to build her exporting journey

    When "Nadia" says that she "has" exported before
    And "Nadia" says that exporting is "a regular" part of her business
    And "Nadia" says what she wants to export "<goods_or_services>"
    And "Nadia" says that her company "is" incorporated
    And "Nadia" "<company_name_action>" her company name
    And "Nadia" sees the summary page with answers to the questions she was asked
    And "Nadia" can see that she was classified as a "regular" exporter
    And "Nadia" decides to create her personalised journey page

    Then "Nadia" should be on the Personalised Journey page for "regular" exporters

    Examples:
      | company_name_action  | goods_or_services  |
      | types in             | goods              |
      | does not provide     | services           |
      | types in and selects | goods              |
      | types in             | goods and services |


  @new-triage
  @ED-2520
  @first-time
  @regular
  Scenario Outline: Not incorporated Regular Exporter visiting the home page for the 1st time should be able to get to personalised page after going through triage process
    Given "Nadia" visits the "Home" page for the first time
    And "Nadia" decided to build her exporting journey

    When "Nadia" says that she "has" exported before
    And "Nadia" says that exporting is "a regular" part of her business
    And "Nadia" says what she wants to export "<goods_or_services>"
    And "Nadia" says that her company "is not" incorporated
    And "Nadia" sees the summary page with answers to the questions she was asked
    And "Nadia" can see that she was classified as a "regular" exporter
    And "Nadia" decides to create her personalised journey page

    Then "Nadia" should be on the Personalised Journey page for "regular" exporters

    Examples:
      | goods_or_services  |
      | goods              |
      | services           |
      | goods and services |


  @new-triage
  @ED-2521
  @first-time
  @occasional
  Scenario Outline: Occasional Exporter which "<online_action>" used online marketplaces and visiting the home page for the 1st time should be able to get to personalised page after going through triage process
    Given "Inigo" visits the "home" page for the first time
    And "Inigo" decided to build his exporting journey

    When "Inigo" says that she "has" exported before
    And "Inigo" says that exporting is "not a regular" part of her business
    And "Inigo" says that she "<online_action>" used online marketplaces
    And "Inigo" says what she wants to export "<goods_or_services>"
    And "Inigo" says that her company "is" incorporated
    And "Inigo" "<company_name_action>" his company name
    And "Inigo" sees the summary page with answers to the questions he was asked
    And "Inigo" can see that she was classified as a "occasional" exporter
    And "Inigo" decides to create her personalised journey page

    Then "Inigo" should be on the Personalised Journey page for "occasional" exporters

    Examples:
      | online_action | company_name_action  | goods_or_services  |
      | has           | types in             | goods              |
      | has never     | types in             | services           |
      | has           | does not provide     | goods              |
      | has never     | does not provide     | services           |
      | has           | types in and selects | goods              |
      | has never     | types in and selects | services           |
      | has           | types in             | goods and services |


  @new-triage
  @ED-2521
  @first-time
  @occasional
  Scenario Outline: Not incorporated Occasional Exporter which "<online_action>" used online marketplaces and visiting the home page for the 1st time should be able to get to personalised page after going through triage process
    Given "Inigo" visits the "home" page for the first time
    And "Inigo" decided to build his exporting journey

    When "Inigo" says that she "has" exported before
    And "Inigo" says that exporting is "not a regular" part of her business
    And "Inigo" says that she "<online_action>" used online marketplaces
    And "Inigo" says what she wants to export "<goods_or_services>"
    And "Inigo" says that her company "is not" incorporated
    And "Inigo" sees the summary page with answers to the questions he was asked
    And "Inigo" can see that she was classified as a "occasional" exporter
    And "Inigo" decides to create her personalised journey page

    Then "Inigo" should be on the Personalised Journey page for "occasional" exporters

    Examples:
      | online_action | goods_or_services  |
      | has           | goods              |
      | has never     | services           |
      | has           | goods and services |


  @new-triage
  @ED-2522
  @first-time
  @new
  Scenario Outline: New Exporter visiting the home page for the 1st time should be able to get to personalised page after going through triage process
    Given "Jonah" visits the "home" page for the first time
    And "Jonah" decided to build his exporting journey

    When "Jonah" says that he "has never" exported before
    And "Inigo" says what she wants to export "<goods_or_services>"
    And "Jonah" says that his company "is" incorporated
    And "Jonah" "<company_name_action>" his company name
    And "Jonah" sees the summary page with answers to the questions he was asked
    And "Jonah" can see that he was classified as a "new" exporter
    And "Jonah" decides to create his personalised journey page

    Then "Jonah" should be on the Personalised Journey page for "new" exporters

    Examples:
      | company_name_action  | goods_or_services  |
      | types in             | goods              |
      | does not provide     | services           |
      | types in and selects | goods              |
      | types in and selects | goods and services |


  @new-triage
  @ED-2522
  @first-time
  @new
  Scenario Outline: Not incorporated New Exporter visiting the home page for the 1st time should be able to get to personalised page after going through triage process
    Given "Jonah" visits the "home" page for the first time
    And "Jonah" decided to build his exporting journey

    When "Jonah" says that he "has never" exported before
    And "Jonah" says what he wants to export "<goods_or_services>"
    And "Jonah" says that his company "is not" incorporated
    And "Jonah" sees the summary page with answers to the questions he was asked
    And "Jonah" can see that he was classified as a "new" exporter
    And "Jonah" decides to create his personalised journey page

    Then "Jonah" should be on the Personalised Journey page for "new" exporters

    Examples:
      | goods_or_services  |
      | goods              |
      | services           |
      | goods and services |


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
