@advice
Feature: Advice articles

  Background:
    Given basic authentication is done for "Domestic - Home" page

  @CMS-686
  @home-page
  @articles
  Scenario: Any Exporter should see all expected sections on "Domestic - Advice landing" page
    When "Robert" goes to the "Domestic - Advice landing" page

    Then  "Robert" should see following sections
      | sections                 |
      | Hero                     |
#      | Breadcrumbs              |  Breadcrumbs are not present on this page. See bug CMS-1698
      | Advice & Guidance tiles  |
      | Error reporting          |


  @CMS-686
  @home-page
  @articles
  Scenario: Any Exporter should be able to get to a list of Advice articles from the home page using link in "<specific>" section
    Given "Robert" visits the "Domestic - Advice landing" page

    When "Robert" opens any article on the list

    Then "Robert" should be on the "Domestic - Advice - article list" page
    And  "Robert" should see following sections
      | sections                 |
      | Hero                     |
      | Breadcrumbs              |
      | List of articles         |
      | Error reporting          |


  @CMS-686
  @home-page
  @articles
  Scenario Outline: Any Exporter should be able to get to "<advice>" Advice article
    Given "Robert" visits the "Domestic - <advice> - Article list" page

    When "Robert" opens any article on the list

    Then "Robert" should be on the "Domestic - Advice - Article" page
    And  "Robert" should see following sections
      | sections        |
      | Breadcrumbs     |
      | Share buttons   |
      | Article         |
      | Error reporting |

    Examples:
      | advice                                      |
      | Find an export market                       |

    @full
    Examples:
      | advice                                      |
      | Create an export plan                       |
      | Define route to market                      |
      | Get export finance                          |
      | Manage payment for export orders            |
      | Prepare to do business in a foreign country |
      | Manage legal and ethical compliance         |
      | Prepare for export procedures and logistics |


  @CMS-686
  @report
  Scenario: Any Exporter should be able to report a problem with Advice Article page
    Given "Robert" is on randomly selected Advice article page

    When "Robert" decides to report a problem with the page

    Then "Robert" should be on the "Domestic - Feedback - contact us" page


  @bug
  @CMS-1698
  @fixed
  @CMS-686
  @breadcrumbs
  Scenario Outline: Any Exporter should see be to use "<breadcrumb>" breadcrumb on "Advice article" page to get to "<target>" page
    Given "Robert" is on randomly selected Advice article page

    When "Robert" decides to open "<breadcrumb>"

    Then "Robert" should be on the "Domestic - <target>" page or on the International page

    Examples:
      | breadcrumb   | target                |
      | great.gov.uk | Home                  |
      | Advice       | Advice Landing        |
      | Article list | Advice - article list |


  @CMS-686
  @header
  @footer
  Scenario: Any Exporter visiting the home page should be able to see links to all Advice categories in "Domestic - <link_location>"
    Given "Robert" visits the "Domestic - Home" page

    Then "Robert" should see links to following "Advice" categories in "Domestic - home"
      | categories                                  |
      | Create an export plan                       |
      | Find an export market                       |
      | Define route to market                      |
      | Manage payment for export orders            |
      | Prepare to do business in a foreign country |
      | Manage legal and ethical compliance         |
      | Prepare for export procedures and logistics |
      | Get export finance                          |
