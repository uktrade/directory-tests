Feature: Promoted industries

  @ED-2013
  @industries
  Scenario: Buyers should be able to view page with promoted Industries
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" visits "Industries" page on FAS

    Then "Annette Geissinger" should see sections with selected industries
      | industry       |
      | Health         |
      | Tech           |
      | Creative       |
      | Food and drink |


  @ED-2015
  @industries
  Scenario Outline: Buyers should be able to find out more about every promoted industry - visit "<selected>" page
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" visits "<selected>" page on FAS

    Then "Annette Geissinger" should be presented with "<selected>" FAS page

    Examples:
      | selected                        |
      | Health Industry                 |
      | Tech Industry                   |
      | Creative Industry               |
      | Food and drink Industry         |
      | Health Industry Summary         |
      | Tech Industry Summary           |
      | Creative Industry Summary       |
      | Food and drink Industry Summary |
