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
