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
      | goods_or_services | has_or_has_not | expected                                             |
      | goods             | has            | Top 10, FAB section, SOO tile, ExOpps tile, Guidance |
      | goods             | has not        | Top 10, SOO tile, ExOpps tile, Guidance              |
      | services          | has            | FAB section, SOO tile, ExOpps tile, Guidance         |
      | services          | has not        | SOO tile, ExOpps tile, Guidance                      |


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
      | goods_or_services | used_or_not | has_or_has_not | expected                                                     |
      | goods             | used        | has            | Top 10, Article list, FAB section, SOO section, Case studies |
      | goods             | used        | has not        | Top 10, Article list, SOO section, Case studies              |
      | services          | never used  | has            | Article list, FAB section, Case studies                      |
      | services          | never used  | has not        | Article list, Case studies                                   |


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
      | goods_or_services | has_or_has_not | expected                                        |
      | goods             | has            | Top 10, Article list, FAB section, Case studies |
      | goods             | has not        | Top 10, Article list, Case studies              |
      | services          | has            | Article list, FAB section, Case studies         |
      | services          | has not        | Article list, Case studies                      |


  @wip
  @ED-2591
  @personalised-page
  Scenario: Any Exporter should be able to update preferences from personalised page
    Given "Robert" is on personalised page

    When "Robert" decides to update his triage preferences

    Then "Robert" should be redirected to the triage summary where he can change his answers


  @wip
  @ED-2592
  @personalised-page
  Scenario: Any Exporter should see the Banner & Top 10 table specific to the sector they selected in triage
    Given "Robert" has created the personalised journey page

    Then "Robert" should see the Banner & Top 10 table specific to the sector they selected in triage


  @wip
  @ED-2593
  @personalised-page
  Scenario Outline: Any Exporter should get to a relevant case study from Case Studies carousel on the personalised page
    Given "Robert" is interested in "<case_study_name>" case study

    When "Robert" goes to the relevant "<case_study_name>" link in the Case Studies carousel on the personalised page

    Then "Robert" should see "<case_study_name>" page with a Share widget

    Examples:
      | case_study_name   |
      | First case study  |
      | Second case study |
      | Third case study  |
