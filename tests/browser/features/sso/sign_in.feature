@sso
@allure.suite:SSO
Feature: SSO - Sign in

  Background:
    Given basic authentication is done for "SSO - Sign in" page
    And basic authentication is done for "SSO - Static assets" page

  @bug
  @allure.issue:TT-1778
  @fixed
  Scenario: Visitors should see all expected page elements on "SSO - Sign in"
    When "Robert" goes to the "SSO - Sign in" page

    Then "Robert" should see following sections
      | Sections                      |
      | Header                        |
      | SSO links - logged out        |
      | Breadcrumbs                   |
      | Form                          |
      | Create a great.gov.uk account |
      | Footer                        |


  @bug
  @allure.issue:TT-1778
  @fixed
  Scenario: Visitors should see all expected page elements on "SSO - Registration" page
    When "Robert" goes to the "SSO - Registration" page

    Then "Robert" should see following sections
      | Sections               |
      | Header                 |
      | SSO links - logged out |
      | Breadcrumbs            |
      | Form                   |
      | Footer                 |


  @bug
  @allure.issue:TT-1778
  @fixed
  Scenario: Visitors should see all expected page elements on "Profile - Sign in"
    Given basic authentication is done for "Profile - Create an account" page
    And basic authentication is done for "Profile - Static assets" page
    And "Robert" visits the "SSO - Sign in" page

    When "Robert" decides to "Create account"

    Then "Robert" should be on the "Profile - Create an account" page
    And "Robert" should see following sections
      | Sections               |
      | Header                 |
      | Breadcrumbs            |
      | Enrolment progress bar |
      | Footer                 |
