@fas
Feature: Contact a Supplier


  @ED-2011
  @contact
  @captcha
  @dev-only
  @fake-sso-email-verification
  Scenario: Buyers should be able to contact selected Supplier via FAS
    Given "Annette Geissinger" is a buyer
    And "Peter Alder" is an unauthenticated supplier
    And "Peter Alder" created a "published LTD, PLC or Royal Charter" profile for a random company "Y"
    And "Annette Geissinger" has found a company "Y" on Find a Supplier site

    When "Annette Geissinger" sends a message to company "Y"

    Then "Annette Geissinger" should be told that the message has been sent to company "Y"
    And "Peter Alder" should receive an email message from "Annette Geissinger"
