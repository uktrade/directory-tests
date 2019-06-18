@isd
Feature: ISD - Landing

  Background:
    Given basic authentication is done for "Domestic - Home" page

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
