@advice
Feature: Advice articles

  Background:
    Given hawk cookie is set on "Export Readiness - Home" page

  @CMS-686
  @home-page
  @articles
  @<specific>
  Scenario Outline: Any Exporter should be able to get to a list of Advice articles from the home page using link in "<specific>" section
    Given "Robert" visits the "Export Readiness - Home" page

    When "Robert" opens any "link" available in the "<specific>" section

    Then "Robert" should be on the "Export Readiness - Advice - article list" page
    And  "Robert" should see following sections
      | sections                 |
      | Hero                     |
      | Total number of Articles |
      | Breadcrumbs              |
      | List of articles         |
      | Error reporting          |

    Examples: sections
      | specific        |
      | Advice          |
      | Header - Advice |
      | Footer - Advice |


  @CMS-686
  @home-page
  @articles
  Scenario: Advice article counter on the Home page should match the one on the Advice page
    Given "Robert" visits the "Export Readiness - Home" page

    When "Robert" opens any "link" available in the "Advice" section

    Then "Robert" should be on the "Export Readiness - Advice - Article list" page
    And "Robert" should see that article counter matches expected number
    And "Robert" should see that article counter matches the number of articles on the page


  @CMS-686
  @home-page
  @articles
  Scenario Outline: Any Exporter should be able to get to "<advice>" Advice article
    Given "Robert" visits the "Export Readiness - <advice> - Article list" page

    When "Robert" opens any article on the list

    Then "Robert" should be on the "Export Readiness - Advice - Article" page
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
      | Get export finance and funding              |
      | Manage payment for export orders            |
      | Prepare to do business in a foreign country |
      | Manage legal and ethical compliance         |
      | Prepare for export procedures and logistics |


  @CMS-686
  @home-page
  @articles
  @<specific>
  Scenario: Any Exporter should be able to get to a list of Advice articles from the "Advice landing" page
    Given "Robert" visits the "Export Readiness - Advice - landing" page

    When "Robert" opens any "link" available in the "List of Articles" section

    Then "Robert" should be on the "Export Readiness - Advice - Article list" page
    And  "Robert" should see following sections
      | sections                 |
      | Hero                     |
      | Total number of Articles |
      | Breadcrumbs              |
      | List of articles         |
      | Error reporting          |


  @CMS-686
  @bug
  @CMS-733
  @fixed
  @sharing
  @social-media
  @<social_media>
  Scenario Outline: Any Exporter should be able to share Advice article via "<social_media>"
    Given "Robert" is on randomly selected Advice article page

    When "Robert" decides to share the article via "<social_media>"

    Then "Robert" should be taken to a new tab with the "<social_media>" share page opened
    And "Robert" should that "<social_media>" share page has been pre-populated with message and the link to the article

    Examples:
      | social_media |
      | Facebook     |
      | Twitter      |
      | Facebook     |

  @CMS-686
  @bug
  @CMS-733
  @fixed
  @sharing
  @social-media
  @email
  Scenario: Any Exporter should be able to share Advice article via "email"
    Given "Robert" is on randomly selected Advice article page

    When "Robert" decides to share the article via "email"

    Then "Robert" should see that the share via email link will pre-populate the message subject and body with Article title and URL


  @CMS-686
  @report
  Scenario: Any Exporter should be able to report a problem with Advice Article page
    Given "Robert" is on randomly selected Advice article page

    When "Robert" decides to report a problem with the page

    Then "Robert" should be on the "Export Readiness - Feedback - contact us" page


  @CMS-686
  Scenario Outline: Any Exporter visiting the home page should be able to see links to all Advice categories in "Export Readiness - <link_location>"
    Given "Robert" visits the "Export Readiness - Home" page

    Then "Robert" should see links to following "Advice" categories in "Export Readiness - <link_location>"
      | categories                                  |
      | Create an export plan                       |
      | Find an export market                       |
      | Define route to market                      |
      | Get export finance and funding              |
      | Manage payment for export orders            |
      | Prepare to do business in a foreign country |
      | Manage legal and ethical compliance         |
      | Prepare for export procedures and logistics |

    Examples:
      | link_location |
      | header        |
      | home          |
      | footer        |


  @CMS-686
  @breadcrumbs
  Scenario Outline: Any Exporter should see be to use "<breadcrumb>" breadcrumb on "Advice article" page to get to "<target>" page
    Given "Robert" is on randomly selected Advice article page

    When "Robert" decides to open "<breadcrumb>"

    Then "Robert" should be on the "Export Readiness - <target>" page

    Examples:
      | breadcrumb   | target                |
      | great.gov.uk | Home                  |
      | Advice       | Advice - Landing      |
      | Article list | Advice - article list |
