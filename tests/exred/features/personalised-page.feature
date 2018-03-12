@customised-page
Feature: Customised page


  @ED-2588
  @personalised-page
  @regular
  Scenario Outline: Regular Exporter which exports "<goods_or_services>" and "<has_or_has_not>" incorporated his company should see "<expected>" sections on personalised page
    Given "Nadia" exports "<goods_or_services>"
    And "Nadia" was classified as "Regular" Exporter which "<has_or_has_not>" incorporated the company

    When "Nadia" decides to create her personalised journey page

    Then "Nadia" should be on the Personalised Journey page for "regular" exporters
    And "Nadia" should see "<expected>" sections on "personalised journey" page

    Examples:
      | goods_or_services | has_or_has_not | expected                                     |
      | goods             | has            | FAB section, SOO tile, ExOpps tile, Guidance |
      | goods             | has not        | SOO tile, ExOpps tile, Guidance              |
      | services          | has            | FAB section, SOO tile, ExOpps tile, Guidance |
      | services          | has not        | SOO tile, ExOpps tile, Guidance              |


  @ED-2589
  @personalised-page
  @occasional
  Scenario Outline: Occasional Exporter which exports "<goods_or_services>", "<used_or_not>" online marketplaces and "<has_or_has_not>" incorporated his company should see "<expected>" sections on personalised page
    Given "Inigo" exports "<goods_or_services>"
    And "Inigo" "<used_or_not>" online marketplaces before
    And "Inigo" was classified as "Occasional" Exporter which "<has_or_has_not>" incorporated the company

    When "Inigo" decides to create her personalised journey page

    Then "Inigo" should be on the Personalised Journey page for "occasional" exporters
    And "Inigo" should see "<expected>" sections on "personalised journey" page

    Examples:
      | goods_or_services | used_or_not | has_or_has_not | expected                                             |
      | goods             | used        | has            | Article list, FAB section, SOO section, Case studies |
      | goods             | used        | has not        | Article list, SOO section, Case studies              |
      | services          | never used  | has            | Article list, FAB section, Case studies              |
      | services          | never used  | has not        | Article list, Case studies                           |


  @ED-2590
  @personalised-page
  @new
  Scenario Outline: New Exporter which exports "<goods_or_services>" and "<has_or_has_not>" incorporated his company should see "<expected>" sections on personalised page
    Given "Jonah" exports "<goods_or_services>"
    And "Jonah" was classified as "New" Exporter which "<has_or_has_not>" incorporated the company

    When "Jonah" decides to create his personalised journey page

    Then "Jonah" should be on the Personalised Journey page for "new" exporters
    And "Jonah" should see "<expected>" sections on "personalised journey" page

    Examples:
      | goods_or_services | has_or_has_not | expected                                |
      | goods             | has            | Article list, FAB section, Case studies |
      | goods             | has not        | Article list, Case studies              |
      | services          | has            | Article list, FAB section, Case studies |
      | services          | has not        | Article list, Case studies              |


  @ED-2465
  @personalised-page
  @articles
  @<relevant>
  @bug
  @ED-2508
  @fixed
  Scenario Outline: "<relevant>" Exporter should see Export Readiness Articles Read Counter on the personalised page
    Given "Nadia" classifies herself as "<relevant>" exporter

    When "Nadia" creates a personalised journey page for herself

    Then "Nadia" should see a Guidance Articles read counter for the "<relevant>" exporter

    Examples:
      | relevant   |
      | New        |
      | Occasional |


  @ED-2591
  @triage
  @change-answers
  @personalised-page
  Scenario Outline: "<relevant>" Exporter should be able to update preferences from personalised journey page
    Given "Robert" was classified as "<relevant>" exporter in the triage process
    And "Robert" decided to create her personalised journey page

    When "Robert" decides to update his triage preferences

    Then "Robert" should be on the "Triage - Summary" page
    And "Robert" should see an option to change his triage answers

    Examples:
      | relevant   |
      | New        |
      | Occasional |
      | Regular    |
