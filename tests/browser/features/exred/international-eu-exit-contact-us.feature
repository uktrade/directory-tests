Feature: International Page - EU Exit - Contact us


  @TT-617
  @eu-exit
  @contact-us
  @international-page
  Scenario: International Visitors should be able to submit their questions regarding EU Exit
    Given "Robert" visits the "Export Readiness - International EU Exit - Contact Us" page

    Then "Robert" should see following sections
      | sections        |
      | header bar      |
      | header menu     |
      | heading         |
      | form            |
      | error reporting |
    And "Robert" should not see following section
      | section           |
      | language selector |


  @TT-617
  @eu-exit
  @contact-us
  @international-page
  Scenario: International Visitors should be able to submit their questions regarding EU Exit
    Given "Robert" visits the "Export Readiness - International EU Exit - Contact Us" page

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Export Readiness - International EU Exit - Thank you for contacting us" page
