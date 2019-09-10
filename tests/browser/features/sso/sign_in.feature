@sso
Feature: SSO - Sign in

  @bug
  @TT-1778
  Scenario: Visitors should see all expected page elements on "Single Sign-On - Sign in"
    When "Robert" goes to the "Single Sign-On - Sign in" page

    Then "Robert" should see following sections
      | Sections                      |
      | Header                        |
      | SSO links - logged out        |
      | Breadcrumbs                   |
      | Login form                    |
      | Create a great.gov.uk account |
#      See TT-1778 there's a problem with lazy loading and Firefox
#      | Footer                        |


  @bug
  @TT-1778
  Scenario: Visitors should see all expected page elements on "Single Sign-On - Registration" page
    When "Robert" goes to the "Single Sign-On - Registration" page

    Then "Robert" should see following sections
      | Sections               |
      | Header                 |
      | SSO links - logged out |
      | Breadcrumbs            |
      | Form                   |
#      See TT-1778 there's a problem with lazy loading and Firefox
#      | Footer                        |


  @bug
  @TT-1778
  Scenario: Visitors should see all expected page elements on "Profile - Sign in"
    Given "Robert" visits the "Single Sign-On - Sign in" page

    When "Robert" decides to "Create account"

    Then "Robert" should be on the "Profile - Create an account" page
    And "Robert" should see following sections
      | Sections               |
      | Header                 |
      | Breadcrumbs            |
      | Enrolment progress bar |
#      See TT-1778 there's a problem with lazy loading and Firefox
#      | Footer                        |
