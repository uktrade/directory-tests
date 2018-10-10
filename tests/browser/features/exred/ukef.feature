@ukef
Feature: UK Export Finance page & contact-us form


  @TT-585
  Scenario: Any Exporter should see the all expected sections on the "UKEF Get Finance" page
    Given "Robert" visits the "Export Readiness - Get Finance" page

    Then "Robert" should see following sections
      | Sections              |
      | Breadcrumbs           |
      | Hero                  |
      | Check you eligibility |
      | Advantages            |
      | Video                 |
      | Contact us            |
      | Error Reporting       |


  @TT-585
  Scenario: Any Exporter should be able to watch promotional video on the "UKEF Get Finance" page
    Given "Robert" visits the "Export Readiness - Get Finance" page

    When "Robert" decides to watch "6" seconds of the promotional video

    Then "Robert" should be able to watch at least first "5" seconds of the promotional video


  @TT-585
  Scenario: Any Exporter should be able to watch promotional video on the "UKEF Get Finance" page
    Given "Robert" visits the "Export Readiness - Get Finance" page

    When "Robert" decides to "Read more about getting money to grow your business"

    Then "Robert" should see an ordered list of all Guidance Articles selected for "Finance" category
    Then "Robert" should be on the "Export Readiness - Finance - Guidance" page


  @TT-585
  Scenario: Any Exporter should see the all expected sections on the "UKEF Get Finance" page
    Given "Robert" visits the "Export Readiness - Get Finance" page

    When "Robert" decides to use "Export" breadcrumb on the "Export Readiness - Get Finance" page

    Then "Robert" should be on the "Export Readiness - Home" page
