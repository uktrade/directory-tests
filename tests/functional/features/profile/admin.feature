@admin
@profile
Feature: Profile - Admin


  @captcha
  @dev-only
  @fake-sso-email-verification
  Scenario: Supplier should not be able to update business details using invalid values
    Given "Annette Geissinger" created an "unpublished unverified LTD, PLC or Royal Charter" profile for a random company "Company X"

    When "Annette Geissinger" goes to "Profile - Remove profile from account" page

    Then "Annette Geissinger" should see "You are the only administrator for this business profile" message
