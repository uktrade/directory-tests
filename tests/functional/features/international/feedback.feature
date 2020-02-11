@international
@allure.suite:International
Feature: Send feedback


  @bug
  @allure.issue:CMS-1850
  @fixme
  @allure.link:ED-2012
  @captcha
  @dev-only
  @feedback
  @no-sso-email-verification-required
  Scenario: Buyer should be able to send us a feedback from "Industries" page
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" sends a Trade Profiles feedback request from "International - Industries" FAS page

    Then "Annette Geissinger" should be told that the feedback request has been submitted
