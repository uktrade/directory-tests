@erp
Feature: ERP - common pages

  Scenario: Enquirers should be able to find out more about ERP service on its Landing page
    When "Robert" goes to the "ERP - Landing" page

    Then "Robert" should see following sections
      | Sections    |
      | Header      |
      | Beta bar    |
      | Breadcrumbs |
      | Description |
      | Footer      |


  Scenario: Enquirers should be able to find out more about ERP service on its Landing page
    Given "Robert" visits the "ERP - Landing" page

    When "Robert" decides to "start now"

    Then "Robert" should be on the "ERP - User type" page
    And "Robert" should see following sections
      | Sections |
      | Header   |
      | Beta bar |
      | Go back  |
      | Form     |
      | Footer   |


  Scenario: Enquirers should be able to choose appropriate type of business they represent on the "ERP - User type" page
    When "Robert" goes to the "ERP - User type" page

    Then "Robert" should see following options
      | options                          |
      | UK business                      |
      | UK consumer                      |
      | Exporter from developing country |
