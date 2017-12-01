@services
Feature: Accessing Services


  @ED-2659
  @home-page
  @accessing-services
  Scenario Outline: Any Exporter visiting the home page should be able to see links to selected Services in/on "<link_location>"
    Given "Robert" visits the "Home" page

    Then "Robert" should see links to following Services "<services>" in "<link_location>"

    Examples:
      | services                                                                         | link_location |
      | Find a buyer, Export opportunities, Selling online overseas, Get Finance, Events | header menu   |
      | Find a buyer, Export opportunities, Selling online overseas                      | home page     |
      | Find a buyer, Export opportunities, Selling online overseas, Get Finance, Events | footer links  |


  @ED-2660
  @home-page
  @accessing-services
  @interim-pages
  @<service>
  Scenario Outline: Any Exporter should be presented with interim pages leading to "<service>" Service page when accessed via "<link_location>"
    Given "Robert" visits the "Home" page

    When "Robert" goes to "<service>" using "Services" links in "<link_location>"

    Then "Robert" should be on the "Interim <service>" page

    Examples:
      | service              | link_location |
      | Export Opportunities | header menu   |
      | Export Opportunities | home page     |
      | Export Opportunities | footer links  |


  @wip
  @out-of-scope
  @ED-2660
  @home-page
  @accessing-services
  @interim-pages
  @<service>
  Scenario Outline: Any Exporter should be presented with an interim page leading to "<service>" Service page which was accessed via "<link_location>"
    Given "Robert" visits the "Home" page

    When "Robert" goes to "<service>" using "Services" links in "<link_location>"

    Then "Robert" should be on the "Interim <service>" page

    Examples:
      | service                 | link_location |
      | Find a Buyer            | header menu   |
      | Find a Buyer            | home page     |
      | Find a Buyer            | footer links  |
      | Selling online overseas | header menu   |
      | Selling online overseas | home page     |
      | Selling online overseas | footer links  |


  @ED-2661
  @home-page
  @accessing-services
  @interim-pages
  @<service_name>
  Scenario Outline: Any Exporter should be able to get to the "<service>" Service page via interim page which was accessed via "<link_location>"
    Given "Robert" visits the "Home" page

    When "Robert" goes to "<service>" using "Services" links in "<link_location>"
    And "Robert" opens the link to "<service>" from interim page

    Then "Robert" should be on the "<service>" page

    Examples:
      | service                 | link_location |
      | Export Opportunities    | header menu   |
      | Export Opportunities    | home page     |
      | Export Opportunities    | footer links  |


  @bug
  @ED-2702
  @fixed
  @ED-2661
  @home-page
  @accessing-services
  @<service_name>
  Scenario Outline: Any Exporter should be able to get to the "<service>" Service page using "<link_location>"
    Given "Robert" visits the "Home" page

    When "Robert" goes to "<service>" using "Services" links in "<link_location>"

    Then "Robert" should be on the "<service>" page

    Examples:
      | service                 | link_location |
      | Find a Buyer            | header menu   |
      | Find a Buyer            | home page     |
      | Find a Buyer            | footer links  |
      | Selling online overseas | header menu   |
      | Selling online overseas | home page     |
      | Selling online overseas | footer links  |
      | Events                  | header menu   |
      | Events                  | footer links  |



  @bug
  @ED-2647
  @fixed
  @ED-2662
  @ED-2667
  @home-page
  @finance
  @accessing-services
  @interim-pages
  Scenario Outline: Any Exporter should see "Get finance" service page not as a Guidance Article
    Given "Robert" visits the "Home" page

    When "Robert" goes to "<service>" using "Services" links in "<link_location>"

    Then "Robert" should be on the "<service>" page
    And  "Robert" should not see "Articles Read counter, Total number of Articles, Time to complete remaining chapters, Tasks completed counter, Tasks Total number"

    Examples:
      | service      | link_location |
      | Get Finance  | header menu   |
      | Get Finance  | footer links  |


  @wip
  @out-of-scope
  @ED-2663
  @personalised-page
  @accessing-services
  @interim-pages
  Scenario: Any Exporter who finished triage should be presented with interim page leading to the actual service page
    Given "Robert" is on the personalised journey page

    When "Robert" opens any visible service link

    Then "Robert" should be presented with Interim page


  @wip
  @out-of-scope
  @ED-2664
  @personalised-page
  @accessing-services
  @interim-pages
  Scenario: Any Exporter who finished triage should be able to get to the actual Service page
    Given "Robert" is on the personalised journey page

    When "Robert" opens any visible service link
    And "Robert" opens the link to the service from interim page

    Then "Robert" should be redirect to the actual service page


  @wip
  @out-of-scope
  @ED-2665
  @personalised-page
  @accessing-services
  @interim-pages
  Scenario: Users that opted-out from showing interim pages should be taken directly to the service page
    Given "Robert" has decided not to have interim pages shown in the past
    And "Robert" is on the personalised journey page

    When "Robert" opens any visible service link

    Then "Robert" should be redirect to the actual service page


  @wip
  @out-of-scope
  @ED-2666
  @home-page
  @accessing-services
  @interim-pages
  Scenario Outline: Any Exporter that opted-out from showing interim pages should be redirected to the Services directly without seeing interim pages
    Given "Robert" has decided not to have interim pages shown in the past

    When "Robert" opens the link to "<service_name>" from "<link_location>"

    Then "Robert" should be redirected to "<service_name>" page

    Examples:
      | service_name            | link_location |
      | Find a Buyer            | header menu   |
      | Find a Buyer            | home page     |
      | Find a Buyer            | footer links  |
      | Export Opportunities    | header menu   |
      | Export Opportunities    | home page     |
      | Export Opportunities    | footer links  |
      | Selling online overseas | header menu   |
      | Selling online overseas | home page     |
      | Selling online overseas | footer links  |
