@isd
Feature: Investment Support Directory


  @search
  @no-sso-email-verification-required
  Scenario: Empty search query should return all published ISD companies
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" searches for ISD companies with empty search query

    Then "Annette Geissinger" should see that ISD search results are not filtered by any sector

