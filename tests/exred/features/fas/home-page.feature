@ED-3580
@fas-home-page
@no-sso-email-verification-required
Feature: FAS landing page


  @ED-4242
  Scenario: Buyers should be able to view "FAS landing" page
    Given "Robert" visits the "FAS landing" page

    Then "Robert" should see "Hero, Find UK Suppliers, Contact us, UK Industries, UK Services" sections on "FAS landing" page


  @ED-4245
  @search
  Scenario Outline: Buyers should be able to "Find UK suppliers" in "<specific>" industry from the "FAS landing" page using "<following>" keyword
    Given "Robert" visits the "FAS landing" page

    When "Robert" searches for companies using "<following>" keyword in "<specific>" sector on "FAS landing" page

    Then "Robert" should be on the "<expected>" page

    Examples:
      | following | specific       | expected                 |
      | no        | any            | FAS empty search results |
      | Food      | any            | FAS search results       |
      | no        | Mining         | FAS search results       |
      | Satellite | Aerospace      | FAS search results       |
      | WiFi      | Communications | FAS search results       |
      | Bridges   | Construction   | FAS search results       |


  @ED-4246
  @contact-us
  Scenario: Buyers should be able to get to the "Contact us" page from the "FAS landing" page
    Given "Robert" visits the "FAS landing" page

    When "Robert" decides to "contact us" via "FAS Landing" page

    Then "Robert" should be on the "FAS Contact us" page


  @ED-4247
  @contact-us
  Scenario: Buyers should be able to contact us (DIT) from the "FAS landing" page
    Given "Robert" visits the "FAS Landing" page
    And "Robert" decided to "contact us" via "FAS Landing" page

    When "Robert" fills out and submits the contact us form

    Then "Robert" should be on the "FAS Thank you for your message" page


  @ED-4248
  @industry-page
  Scenario Outline: Buyers should be able to find out more about "<specific>" industry from the "FAS landing" page
    Given "Robert" visits the "FAS landing" page

    When "Robert" decides to find out out more about "<specific>" industry

    Then "Robert" should be on the "FAS Industry" page
    And "Robert" should see content specific to "<specific>" industry page

    Examples:
      | specific          |
      | Agritech          |
      | Creative services |
      | Cyber security    |


  @ED-4249
  @industries-page
  Scenario: Buyers should be able to see more UK industries from the "FAS landing" page
    Given "Robert" visits the "FAS landing" page

    When "Robert" decides to see more UK industries from the FAS landing page

    Then "Robert" should be on the "FAS Industries" page


  @wip
  @company-profile
  Scenario Outline: Buyers should be able to look for more "Latest company profiles" from the "FAS landing" page using "<following>" keyword
    Given "Robert" visits the "FAS landing" page

    When "Robert" looks for UK suppliers using "Latest company profiles" section and "<following>" keyword

    Then "Robert" should see "FAS search" page

    Examples:
      | following |
      | SpaceX    |
      | WiFI      |
      | Bridges   |


  @wip
  @company-profile
  Scenario Outline: Buyers should be able to view the "<selected>" latest company profile from the "FAS landing" page
    Given "Robert" visits the "FAS landing" page

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
  Scenario: Buyers should be able to view all latest company profiles from the "FAS landing" page
    Given "Robert" visits the "FAS landing" page

    When "Robert" decides to view more latest company profiles

    Then "Robert" should see "FAS latest company profiles" page


  @wip
  @report-this-page
  Scenario: Buyers should be able to report a problem with the "FAS landing" page
    Given "Robert" visits the "FAS landing" page

    When "Robert" decides to report problem with the "FAS landing" page
    And "Robert" fills out and submits the "Help us improve great.gov.uk" form

    Then "Robert" should see "Thank you for your feedback" page


  @wip
  @marketing-content-page
  Scenario: Buyers should be able to view the Marketing Content from the "FAS landing" page
    Given "Robert" visits the "FAS landing" page

    When "Robert" decides to go to learn more about marketing on the "FAS landing" page

    Then "Robert" should see the "marketing content" page
