@advice
Feature: Advice articles

  Background:
    Given hawk cookie is set on "Export Readiness - Home" page

  @CMS-686
  @home-page
  @articles
  @<specific>
  Scenario Outline: Any Exporter should be able to get to a list of Advice articles from the home page
    Given "Robert" visits the "Export Readiness - Home" page

    When "Robert" opens any "link" available in the "<specific>" section

    Then "Robert" should be on the "Export Readiness - Advice" page
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

    Then "Robert" should be on the "Export Readiness - Advice" page
    And "Robert" should see that article counter matches expected number
    And "Robert" should see that article counter matches the number of articles on the page


  @CMS-686
  @home-page
  @articles
  Scenario Outline: Any Exporter should be able to get to "<advice>" Advice article
    Given "Robert" visits the "Export Readiness - <advice> - Article list" page

    When "Robert" opens any article on the list

    Then "Robert" should be on the "Export Readiness - Advice Article" page
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
