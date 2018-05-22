@ED-3580
@fas-home-page
@no-sso-email-verification-required
Feature: FAS home page


  @ED-4242
  Scenario: Buyers should be able to view "FAS landing" page
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" goes to "FAS landing" page

    Then "Annette Geissinger" should see following sections
      | expected sections       |
      | Hero                    |
      | Find UK Suppliers       |
      | Contact us              |
      | UK Industries           |
      | UK Services             |


  @wip
  @search
  Scenario Outline: Buyers should be able to "Find UK suppliers" in "<specific>" industry from the "FAS home" page using "<following>" keyword
    Given "Robert" is a buyer
    And "Robert" visits the "FAS home" page

    When "Robert" looks for UK suppliers in "<specific>" industry using "Find UK Suppliers" section and "<following>" keyword

    Then "Robert" should see "FAS search" page

    Examples:
      | specific       | following |
      | Aerospace      | SpaceX    |
      | Communications | WiFI      |
      | Construction   | Bridges   |


  @wip
  @contact-us
  Scenario: Buyers should be able to get to the "Contact us" page from the "FAS home" page
    Given "Robert" is a buyer
    And "Robert" visits the "FAS home" page

    When "Robert" decides to contact us from "FAS home" page

    Then "Robert" should see "Contact us" page


  @wip
  @contact-us
  Scenario: Buyers should be able to contact us (DIT) from the "FAS home" page
    Given "Robert" is a buyer
    And "Robert" visits the "FAS home" page
    And "Robert" decides to contact us from "FAS home" page

    When "Robert" fills out and submits the contact us form

    Then "Robert" should see "Thank you for contacting us" page


  @wip
  @industry-page
  Scenario Outline: Buyers should be able to find out more about "<specific>" industry from the "FAS home" page
    Given "Robert" is a buyer
    And "Robert" visits the "FAS home" page

    When "Rober" decides to find out out more about "<specific>" industry

    Then "Robert" should see "<specific> Industry" page

    Examples:
      | specific          |
      | Agritech          |
      | Creative services |
      | Cyber security    |
#      | Food and drink    |
#      | Global sports     |
#      | Healthcare        |


  @wip
  @industries-page
  Scenario: Buyers should be able to see more UK industries from the "FAS home" page
    Given "Robert" is a buyer
    And "Robert" visits the "FAS home" page

    When "Robert" decides to see more more UK industries from the FAS home page

    Then "Robert" should see "FAS Industries" page


  @wip
  @company-profile
  Scenario Outline: Buyers should be able to look for more "Latest company profiles" from the "FAS home" page using "<following>" keyword
    Given "Robert" is a buyer
    And "Robert" visits the "FAS home" page

    When "Robert" looks for UK suppliers using "Latest company profiles" section and "<following>" keyword

    Then "Robert" should see "FAS search" page

    Examples:
      | following |
      | SpaceX    |
      | WiFI      |
      | Bridges   |


  @wip
  @company-profile
  Scenario Outline: Buyers should be able to view the "<selected>" latest company profile from the "FAS home" page
    Given "Robert" is a buyer
    And "Robert" visits the "FAS home" page

    When "Robert" decides to view the "<selected>" latest company profile

    Then "Robert" should see "FAS company profile" page

    Examples:
      | selected |
      | first    |
      | second   |
      | third    |
      | fourth   |


  @wip
  @report-this-page
  Scenario: Buyers should be able to view all latest company profiles from the "FAS home" page
    Given "Robert" is a buyer
    And "Robert" visits the "FAS home" page

    When "Robert" decides to view more latest company profiles

    Then "Robert" should see "FAS latest company profiles" page


  @wip
  @report-this-page
  Scenario: Buyers should be able to report a problem with the "FAS home" page
    Given "Robert" is a buyer
    And "Robert" visits the "FAS home" page

    When "Robert" decides to report problem with the "FAS home" page
    And "Robert" fills out and submits the "Help us improve great.gov.uk" form

    Then "Robert" should see "Thank you for your feedback" page


  @wip
  @marketing-content-page
  Scenario: Buyers should be able to view the Marketing Content from the "FAS home" page
    Given "Robert" is a buyer
    And "Robert" visits the "FAS home" page

    When "Robert" decides to go to learn more about marketing on the "FAS home" page

    Then "Robert" should see the "marketing content" page
