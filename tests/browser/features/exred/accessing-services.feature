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
      | sections        |
      | Breadcrumbs     |
      | Services        |
      | Error reporting |


  @bug
  @ED-2647
  @fixed
  @ED-2662
  @ED-2667
  @home-page
  @finance
  @accessing-services
  @<service>
  Scenario: Any Exporter should see "Get finance" service page not as a Advice Article
    Given "Robert" visits the "Export Readiness - Services" page

    When "Robert" decides to find out more about "UK Export Finance"

    Then "Robert" should be on the "Export Readiness - Get Finance" page
    And  "Robert" should not see following sections
      | sections                            |
      | Articles Read counter               |
      | Total number of Articles            |
      | Time to complete remaining chapters |
      | Tasks completed counter             |
      | Tasks Total number                  |


  @bug
  @ED-2702
  @fixed
  @ED-2661
  @home-page
  @accessing-services
  @<service>
  @external-service
  Scenario Outline: Any Exporter should be able to get to the "<service>" Service page using "<link_location>"
    Given "Robert" visits the "Export Readiness - Home" page

    When "Robert" goes to "<service>" using "Services" links in "Export Readiness - <link_location>"

    Then "Robert" should be on the "<service> - Home" page

    Examples:
      | service                 | link_location |
      | Find a Buyer            | header        |
      | Find a Buyer            | home          |
      | Find a Buyer            | footer        |
      | Selling online overseas | header        |
      | Selling online overseas | home          |
      | Selling online overseas | footer        |
      | Events                  | header        |
      | Events                  | footer        |
