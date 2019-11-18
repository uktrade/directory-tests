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


  @XOT-1216
  @govuk
  @sections
  Scenario: Any Exporter should be able to find out more about "preparing business for Brexit"
    Given "Robert" visits the "Domestic - Home" page

    When "Robert" decides to find out more about "preparing business for Brexit"

    Then "Robert" should be on the "GOV.UK - Prepare your business or organisation for Brexit" page


  @XOT-1216
  @govuk
  @sections
  Scenario: Any Exporter should be able to find out more how to "prepare business for Brexit" by going to one of the "brexit related" pages on GOV.UK
    Given "Robert" visits the "Domestic - Home" page

    When "Robert" decides to use one of the "brexit related links to GOV.UK"

    Then "Robert" should be on the "GOV.UK - Brexit related article" page


  @XOT-1217
  @markets
  @sections
  Scenario Outline: Any Exporter should be able to get to the export markets listing using "<export market guides>" link on Home page
    Given "Robert" visits the "Domestic - Home" page

    When "Robert" decides to "<export market guides>"

    Then "Robert" should be on the "Domestic - markets listing" page

    Examples:
      | export market guides      |
      | view export market guides |
      | view all market guides    |


  @XOT-1217
  @markets
  @sections
  Scenario: Exporters should be able to quickly filter export markets by one of the preselected sectors
    Given "Robert" visits the "Domestic - Home" page

    When "Robert" decides to use one of the "sector selector quick links"

    Then "Robert" should be on the "Domestic - filtered markets listing" page


  @XOT-1217
  @markets
  @sections
  Scenario: Exporters should be able to filter export markets by the sector their business is in
    Given "Robert" visits the "Domestic - Home" page

    When "Robert" decides to find new markets for his business

    Then "Robert" should be on the "Domestic - filtered markets listing" page


  @XOT-1218
  @markets
  @sections
  Scenario: Any Exporter should be able to learn what's new on our site
    Given "Robert" visits the "Domestic - Home" page

    When "Robert" decides to use one of the "what's new links"

    Then "Robert" should get to a working page
