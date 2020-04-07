@allure.suite:International
Feature: International - About us

  Background:
    Given test authentication is done


  Scenario: Visitors should be able to see all expected sections on "International - About the UK" page
    Given "Robert" visits the "International - About us" page

    Then "Robert" should see following sections
      | Sections           |
      | Header             |
      | Hero               |
      | Breadcrumbs        |
      | About us subheader |
      | Teaser             |
      | How DIT helps      |
      | Error reporting    |
      | Footer             |
