@allure.link:ED-3190
@industries-page
@no-sso-email-verification-required
@allure.suite:International
Feature: INTL - Industries page

  Background:
    Given test authentication is done


  @allure.link:ED-4253
  Scenario: Buyers should be able to view "International - Industries" page
    Given "Annette Geissinger" visits the "International - Industries" page

    Then "Annette Geissinger" should see following sections
      | Sections         |
      | Header           |
      | Hero             |
      | Breadcrumbs      |
      | Industries       |
      | Error reporting  |
      | Footer           |


  @allure.link:ED-4255
  @breadcrumbs
  Scenario: Buyers should be able to go back to the "International - Landing" page via breadcrumbs on the "International - Industries" page
    Given "Robert" visits the "International - Industries" page

    When "Robert" decides to click on "great.gov.uk international"

    Then "Robert" should be on the "International - Landing" page


  @allure.link:ED-4258
  @report-this-page
  Scenario: Buyers should be able to report a problem with the "International - Industries" page
    Given test authentication is done
    Given "Robert" visits the "International - Industries" page

    When "Robert" decides to "report a problem with the page"

    Then "Robert" should be on the "Domestic - Feedback" page
