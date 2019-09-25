@international
Feature: International - Industry pages


  @ED-2015
  @industries
  @no-sso-email-verification-required
  Scenario Outline: Buyers should be able to find out more about every promoted industry - visit "<selected>" page
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" goes to "<selected>" page

    Then "Annette Geissinger" should see "<selected>" page

    Examples:
      | selected                                                 |
      | International - Creative industries - Industry           |
      | International - Engineering and manufacturing - Industry |
      | International - Technology - Industry                    |
