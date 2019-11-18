@home-page
Feature: Domestic - Home Page

  Background:
    Given basic authentication is done for "Domestic - Home" page

  @ED-2366
  @sections
  Scenario: Any Exporter should see the "Beta bar, Hero, EU Exit enquiries banner, Advice, Services, Case Studies, Business is Great, Error Reporting" sections on the home page
      Given "Robert" visits the "Domestic - Home" page
      Then "Robert" should see following sections
        | Sections                         |
        | Header                           |
        | SSO links - logged out           |
        | Hero                             |
        | Prepare your business for Brexit |
        | Find new markets                 |
        | Export goods from the UK         |
        | What's new                       |
        | Error Reporting                  |
        | Footer                           |


  @ED-3014
  @video
  Scenario: Any Exporter should be able to play promotional video on the Home page
    Given "Robert" visits the "Domestic - Home" page

    When "Robert" decides to watch "6" seconds of the promotional video

    Then "Robert" should be able to watch at least first "5" seconds of the promotional video


  @ED-3014
  @video
  Scenario: Any Exporter should be able to close the window with promotional video on the Home page
    Given "Robert" visits the "Domestic - Home" page

    When "Robert" decides to watch "6" seconds of the promotional video
    And "Robert" closes the window with promotional video

    Then "Robert" should not see the window with promotional video


  @XOT-1215
  @maddb
  @sections
  Scenario: Any Exporter should be able to get to the "Market Access Database" using link on the home page
    Given "Robert" visits the "Domestic - Home" page

    When "Robert" decides to find out more about "exporting goods from the UK"

    Then "Robert" should be on the "Market Access Database - Landing" page
