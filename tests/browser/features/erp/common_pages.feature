@erp
Feature: ERP - common pages

  @dev-only
  Scenario: Enquirers should be able to find out more about ERP service on its Landing page
    When "Robert" goes to the "ERP - Landing" page

    Then "Robert" should be on the "ERP - User type" page
    And "Robert" should see following sections
      | Sections |
      | Header   |
      | Beta bar |
      | Form     |
      | Footer   |


  @dev-only
  Scenario: Enquirers should be able to choose appropriate type of business they represent on the "ERP - User type" page
    When "Robert" goes to the "ERP - User type" page

    Then "Robert" should see following options
      | options                          |
      | UK business                      |
      | UK consumer                      |
      | Exporter from developing country |


  @stage-only
  @holding
  Scenario: Enquirers should be greeted with a holding page when such feature is enabled
    Given "Robert" visits the "ERP - Landing" page

    Then "Robert" should be on the "ERP - Holding" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Holding message |
      | Footer          |


  @stage-only
  @holding
  Scenario: Enquirers should be able to learn more about the service from external Gov.UK pages
    Given "Robert" visits the "ERP - Holding" page

    When "Robert" decides to use one of the "Gov.UK links"

    Then "Robert" should get to a working page
