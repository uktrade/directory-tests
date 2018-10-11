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
  Scenario: Any Exporter should be able to get to "Finance Guidance" page from the "UKEF Get Finance" page
    Given "Robert" visits the "Export Readiness - Get Finance" page

    When "Robert" decides to "Read more about getting money to grow your business"

    Then "Robert" should be on the "Export Readiness - Finance - Guidance" page


  @TT-585
  Scenario: Any Exporter should be able to navigate to "Export Readiness - Home" using breadcrumbs on the "UKEF Get Finance" page
    Given "Robert" visits the "Export Readiness - Get Finance" page

    When "Robert" decides to use "Export" breadcrumb on the "Export Readiness - Get Finance" page

    Then "Robert" should be on the "Export Readiness - Home" page


  @TT-585
  Scenario: Any Exporter should be able to get to the "Contact UKEF" form from "Export Readiness - Get Finance"
    Given "Robert" visits the "Export Readiness - Get Finance" page

    When "Robert" decides to "Check your eligibility"

    Then "Robert" should be on the "Export Readiness - What would you like to know more about? - UKEF Contact us" page
    And "Robert" should see following sections
      | Sections        |
      | Breadcrumbs     |
      | Form            |
      | Error Reporting |


  @TT-585
  @captcha
  @dev-only
  Scenario: Any Exporter should be able to contact UKEF team by submitting the "Check you eligibility" form
    Given "Robert" visits the "Export Readiness - What would you like to know more about? - UKEF Contact us" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Export Readiness - Your details - UKEF Contact us" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Export Readiness - Company details - UKEF Contact us" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Export Readiness - Tell us how we can help - UKEF Contact us" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Export Readiness - Thank you - UKEF Contact us" page


  @TT-585
  @captcha
  @dev-only
  Scenario: Any Exporter should not be able to submit "Check you eligibility" form without filling out all required fields
    Given "Robert" visits the "Export Readiness - What would you like to know more about? - UKEF Contact us" page
    When "Robert" submits the form
    Then "Robert" should be on the "Export Readiness - What would you like to know more about? - UKEF Contact us" page
    And "Robert" should see error message saying that mandatory fields are required

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Export Readiness - Your details - UKEF Contact us" page
    When "Robert" submits the form
    Then "Robert" should be on the "Export Readiness - Your details - UKEF Contact us" page
    And "Robert" should see error message saying that mandatory fields are required

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Export Readiness - Company details - UKEF Contact us" page
    When "Robert" submits the form
    Then "Robert" should be on the "Export Readiness - Company details - UKEF Contact us" page
    And "Robert" should see error message saying that mandatory fields are required

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Export Readiness - Tell us how we can help - UKEF Contact us" page
    When "Robert" submits the form
    Then "Robert" should be on the "Export Readiness - Tell us how we can help - UKEF Contact us" page
    And "Robert" should see error message saying that mandatory fields are required

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Export Readiness - Thank you - UKEF Contact us" page
