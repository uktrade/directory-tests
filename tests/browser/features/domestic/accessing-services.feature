@services
Feature: Accessing Services

  Background:
    Given basic authentication is done for "Export Readiness - Home" page

  @ED-2659
  @home-page
  @accessing-services
  Scenario: Any Exporter visiting the Services page should be able to see links to all relevant Services
    When "Robert" goes to the "Export Readiness - Services" page

    Then "Robert" should see following sections
      | sections               |
      | Header                 |
      | SSO links - logged out |
      | Breadcrumbs            |
      | Services               |
      | Error reporting        |
      | Footer                 |


  @bug
  @ED-2702
  @fixed
  @ED-2661
  @home-page
  @accessing-services
  @<service>
  @external-service
  Scenario Outline: Any Exporter should be able to get to the "<specific>" Service page from "Export Readiness - Services" page
    Given "Robert" visits the "Export Readiness - Services" page

    When "Robert" decides to find out more about "<service>"

    Then "Robert" should be on the "<specific>" page

    Examples:
      | service                   | specific                       |
      | Create a business profile | Find a Buyer - Home            |
      | Find online marketplaces  | Selling online overseas - Home |
      | Find export opportunities | Export Opportunities - Home    |
      | UK Export Finance         | Export Readiness - Get Finance |
      | Find events and visits    | Events - Home                  |
      | Get an EORI number        | EORI - Home                    |
