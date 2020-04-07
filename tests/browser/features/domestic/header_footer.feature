@header
@footer
@allure.suite:Domestic
Feature: Domestic - Header-Footer

  Background:
    Given test authentication is done


  @bug
  @allure.issue:ED-3116
  @fixed
  @allure.link:ED-3118
  @logo
  Scenario Outline: Any Exporter should see correct EIG header logo & GREAT footer logo on "<selected>" page
    Given "Robert" visits the "<selected>" page

    Then "Robert" should see correct "EIG" logo
    And "Robert" should see correct "Great - footer" logo

    Examples:
      | selected                       |
      | Domestic - Get finance         |
      | Domestic - Home                |
      | Find a Buyer - Home            |
      | Selling Online Overseas - Home |
      | Profile - About                |
      | SSO - Registration             |
      | SSO - Sign in                  |


  @stage-only
  @allure.link:ED-3118
  @logo
  Scenario: Any Exporter should see correct EIG header logo & GREAT footer logo on "Export Opportunities - Home" page
    Given "Robert" visits the "Export Opportunities - Home" page

    Then "Robert" should see correct "EIG" logo
    And "Robert" should see correct "Great - footer" logo


  @bug
  @allure.issue:ED-3116
  @fixed
  @allure.link:ED-3118
  @events
  @logo
  Scenario: Any Exporter should see correct Business Is Great (BIG) header & footer logo on "Events - Home" page
    Given "Robert" visits the "Events - Home" page

    Then "Robert" should see correct "EVENTS Business Is Great - header" logo
    And "Robert" should see correct "EVENTS Business Is Great - footer" logo


  @allure.link:ED-3118
  @logo
  Scenario: Any Exporter should see correct GREAT header & footer logo on "Find a Supplier - Landing" page
    Given "Robert" visits the "Find a Supplier - Landing" page

    Then "Robert" should see correct "Great - header" logo
    And "Robert" should see correct "Great - footer" logo


  @allure.link:ED-3587
  @logo
  @allure.link:ED-3118
  Scenario Outline: Any Exporter should be able to get to the Domestic Home page from "<selected>" page by using DIT logo in the page header and footer
    Given "Robert" visits the "<selected>" page

    When "Robert" decides to click on "Invest in Great logo"

    Then "Robert" should be on the "Domestic - Home" page or be redirected to "International - Landing" page

    Examples:
      | selected                       |
      | Domestic - Home                |
      | Domestic - Get finance         |
      | SSO - Registration             |
      | SSO - Sign in                  |
      | Find a Buyer - Home            |
      | Selling Online Overseas - Home |
      | Profile - About                |


    @stage-only
    Examples:
      | selected                    |
      | Export Opportunities - Home |


  @allure.link:ED-3091
  @favicon
  Scenario Outline: Any user should see the correct favicon on "<specific>" page
    Given "Robert" visits the "<specific>" page

    Then "Robert" should see the correct favicon

    Examples: Domestic pages
      | specific                       |
      | Domestic - Home                |
      | Find a Buyer - Home            |
      | Find a Supplier - Landing      |
      | SSO - Registration             |
      | SSO - Sign in                  |
      | Profile - About                |
      | Selling Online Overseas - Home |

    @stage-only
    Examples: Export Opportunities
      | specific                       |
      | Export Opportunities - Home    |


  @mobile
  @skip-in-firefox
  Scenario Outline: Any mobile user should see mobile-friendly header on "<selected>" page
    Given "Robert" visits the "<selected>" page

    When "Robert" clicks the Menu button

    Then "Robert" should see the menu items

    Examples: Domestic pages
      | selected                       |
      | Domestic - Home                |
      | Find a Buyer - Home            |
      | Find a Supplier - Landing      |
      | SSO - Registration             |
      | SSO - Sign in                  |
      | Profile - About                |
      | Selling Online Overseas - Home |
