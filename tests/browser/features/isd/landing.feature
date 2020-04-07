@isd
@allure.suite:ISD
Feature: ISD - Landing

  Background:
    Given test authentication is done


  Scenario: Users should see all expected elements on "Investment Support Directory - Landing" page
    When "Robert" goes to the "ISD - Landing" page

    Then "Robert" should see following sections
      | Sections          |
      | Header            |
      | Search form       |
      | Breadcrumbs       |
      | Benefits          |
      | Search categories |
      | Error reporting   |
      | Footer            |

  @search
  Scenario: User comes through the content page - it means that the directory is pre-filtered for the matching content page (industry)
    Given "Robert" visits the "ISD - Landing" page

    When "Robert" searches for companies using "tax" keyword

    Then "Robert" should be on the "ISD - Search results" page
    And "Robert" should see following sections
      | Sections         |
      | Header           |
      | Breadcrumbs      |
      | Results summary  |
      | Search form      |
      | Filters          |
      | Search Results   |
      | Error reporting  |
      | Footer           |
