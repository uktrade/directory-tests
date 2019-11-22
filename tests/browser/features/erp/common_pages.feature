@erp
Feature: ERP - common pages


  Background:
    Given basic authentication is done for "ERP - Landing" page


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


  @wip
  @TT-2183
  @dev-only
  @summary
  Scenario Outline: Should see correct data on summary page
    Given "Robert" got to "<summary>" ERP page as "<specific_user_type>"

    Then "Robert" should see correct data shown on the summary page

    Examples:
      | specific_user_type               | summary                      |
      | consumer group                   | Summary (UK consumer)        |
      | exporter from developing country | Summary (Developing country) |
      | individual consumer              | Summary (UK consumer)        |
      | UK business                      | Summary (UK business)        |
      | UK importer                      | Summary (UK importer)        |
