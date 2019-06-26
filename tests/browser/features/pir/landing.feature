@pir
@no-sso-email-verification-required
Feature: PIR - Landing page

  Background:
    Given basic authentication is done for "Domestic - Home" page

  Scenario: Buyers should be able to view "PIR - Landing" page
    Given "Robert" visits the "PIR - Landing" page

    Then "Robert" should see following sections
      | Sections     |
      | Header       |
      | Hero         |
      | Contact form |
      | Footer       |
