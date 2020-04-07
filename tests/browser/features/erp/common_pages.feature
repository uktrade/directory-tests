@erp
@allure.suite:ERP
Feature: ERP - common pages


  Background:
    Given test authentication is done for "ERP"


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


  @wip
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


  @wip
  @stage-only
  @holding
  Scenario: Enquirers should be able to learn more about the service from external Gov.UK pages
    Given "Robert" visits the "ERP - Holding" page

    When "Robert" decides to use one of the "Gov.UK links"

    Then "Robert" should get to a working page


  @wip
  @allure.link:TT-2183
  @dev-only
  @summary
  Scenario Outline: "<specific_user_type>" should see correct data on "<summary>" page
    Given "Robert" got to "<summary>" ERP page as "<specific_user_type>"

    Then "Robert" should see correct data shown on the summary page

    Examples:
      | specific_user_type               | summary                      |
      | consumer group                   | Summary (UK consumer)        |
      | exporter from developing country | Summary (Developing country) |
      | individual consumer              | Summary (UK consumer)        |
      | UK business                      | Summary (UK business)        |
      | UK importer                      | Summary (UK importer)        |


  @allure.link:TT-2060
  @bug
  @allure.issue:TT-2294
  @fixed
  @search
  Scenario Outline: <user_type> should be able to search for affected goods by phrase "<phrase>" which can be a commodity code or part of its name
    Given "Robert" got to "ERP - Product search (<user_type>)" from "ERP - User type" via "<intermediate_steps>"

    When "Robert" searches using "<phrase>"

    Then "Robert" should see "<an expected number of>" product code(s) to select
    And "Robert" should see "<a number of>" product category(ies) to expand

    Examples:
      | user_type   | intermediate_steps          | phrase           | an expected number of | a number of |
      | UK importer | UK business -> imported     | food             | at least 1            | at least 1  |
      | UK business | UK business -> not imported | mineral products | at least 1            | at least 1  |
      | UK consumer | UK consumer                 | food             | at least 1            | at least 1  |

    Examples: specific product codes
      | user_type   | intermediate_steps          | phrase     | an expected number of | a number of |
      | UK importer | UK business -> imported     | 3904400091 | at least 1            | at least 1  |
      | UK business | UK business -> not imported | 2309904151 | at least 1            | at least 1  |
      | UK consumer | UK consumer                 | 3904400091 | at least 1            | at least 1  |

    Examples: parent product code category
      | user_type   | intermediate_steps          | phrase   | an expected number of | a number of |
      | UK importer | UK business -> imported     | 21069055 | no                    | at least 1  |
      | UK business | UK business -> not imported | 05100000 | no                    | at least 1  |
      | UK consumer | UK consumer                 | 21069055 | no                    | at least 1  |
