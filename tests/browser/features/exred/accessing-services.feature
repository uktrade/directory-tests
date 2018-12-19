@services
Feature: Accessing Services

  Background:
    Given hawk cookie is set on "Export Readiness - Home" page

  @ED-2659
  @home-page
  @accessing-services
  Scenario Outline: Any Exporter visiting the home page should be able to see links to selected Services in/on "<link_location>"
    Given "Robert" visits the "Export Readiness - Home" page

    Then "Robert" should see links to following Services "<services>" in "Export Readiness - <link_location>"

    Examples:
      | services                                                                         | link_location |
      | Find a buyer, Selling online overseas, Export opportunities, Get Finance, Events | header        |
      | Find a buyer, Selling online overseas, Export opportunities                      | home          |
      | Find a buyer, Selling online overseas, Export opportunities, Get Finance, Events | footer        |


  @ED-2660
  @home-page
  @accessing-services
  @interim-pages
  @<service>
  @external-service
  Scenario Outline: Any Exporter should be presented with interim pages leading to "<service>" Service page when accessed via "<link_location>"
    Given "Robert" visits the "Export Readiness - Home" page

    When "Robert" goes to "<service>" using "Services" links in "Export Readiness - <link_location>"

    Then "Robert" should be on the "Export Readiness - Interim <service>" page

    Examples:
      | service              | link_location |
      | Export Opportunities | header        |
      | Export Opportunities | home          |
      | Export Opportunities | footer        |


  @ED-2661
  @home-page
  @accessing-services
  @interim-pages
  @<service_name>
  @external-service
  Scenario Outline: Any Exporter should be able to get to the "<service>" Service page via interim page which was accessed via "<link_location>"
    Given "Robert" visits the "Export Readiness - Home" page

    When "Robert" goes to "<service>" using "Services" links in "Export Readiness - <link_location>"
    And "Robert" opens the link to "<service>" from interim page

    Then "Robert" should be on the "<service> - Home" page

    Examples:
      | service              | link_location |
      | Export Opportunities | header        |
      | Export Opportunities | home          |
      | Export Opportunities | footer        |


  @bug
  @ED-2702
  @fixed
  @ED-2661
  @home-page
  @accessing-services
  @<service_name>
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


  @bug
  @ED-2647
  @fixed
  @ED-2662
  @ED-2667
  @home-page
  @finance
  @accessing-services
  @interim-pages
  Scenario Outline: Any Exporter should see "Get finance" service page not as a Advice Article
    Given "Robert" visits the "Export Readiness - Home" page

    When "Robert" goes to "<service>" using "Services" links in "Export Readiness - <link_location>"

    Then "Robert" should be on the "Export Readiness - <service>" page
    And  "Robert" should not see following sections
      | sections                            |
      | Articles Read counter               |
      | Total number of Articles            |
      | Time to complete remaining chapters |
      | Tasks completed counter             |
      | Tasks Total number                  |

    Examples:
      | service     | link_location |
      | Get Finance | header        |
      | Get Finance | footer        |

