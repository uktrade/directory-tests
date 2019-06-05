@isd
Feature: ISD - Search

  Background:
    Given basic authentication is done for "Find a Supplier - Home" page

  @search
  Scenario: User comes through the content page - it means that the directory is pre-filtered for the matching content page (industry)
    Given "Robert" visits the "Find a Supplier - ISD" page

    When "Robert" searches for companies using "tax" keyword

    Then "Robert" should be on the "Find a Supplier - ISD - Search results" page
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
