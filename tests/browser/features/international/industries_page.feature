@ED-3190
@industries-page
@no-sso-email-verification-required
Feature: INTL - Industries page

  Background:
    Given basic authentication is done for "International - Landing" page

  @ED-4253
  Scenario: Buyers should be able to view "International - Industries" page
    Given "Annette Geissinger" visits the "International - Industries" page

    Then "Annette Geissinger" should see following sections
      | Sections         |
      | Header           |
      | Hero             |
      | Breadcrumbs      |
      | Industries       |
      | Error reporting  |
      | Footer           |


  @ED-4254
  @industry-pages
  Scenario Outline: Buyers should be able to find out more about "<specific>" industry from the "International - Industries" page
    Given "Robert" visits the "International - Industries" page

    When "Robert" decides to find out out more about "International - <specific> - industry"

    Then "Robert" should be on the "International - <specific> - industry" page
    And "Robert" should see content specific to "International - <specific> - industry" page

    Examples: common industries
      | specific                            |
      | Creative industries                 |

    @full
    @dev-only
    Examples: promoted industries
      | specific                            |
      | Automotive                          |
      | Aerospace                           |
      | Education                           |
      | Engineering and manufacturing       |
      | Healthcare and Life Sciences        |
      | Legal services                      |
      | Real Estate                         |
      | Space                               |
      | Technology                          |

    @full
    @stage-only
    Examples: promoted industries
      | specific                            |
      | Engineering and manufacturing       |
      | Financial and professional services |
      | Legal services                      |
      | Technology                          |

    @wip
    @dev-only
    Examples: missing content
      | specific                            |
      | Energy                              |


  @ED-4255
  @breadcrumbs
  Scenario: Buyers should be able to go back to the "International - Landing" page via breadcrumbs on the "International - Industries" page
    Given "Robert" visits the "International - Industries" page

    When "Robert" decides to click on "great.gov.uk international"

    Then "Robert" should be on the "International - Landing" page


  @ED-4258
  @report-this-page
  Scenario: Buyers should be able to report a problem with the "International - Industries" page
    Given "Robert" visits the "International - Industries" page

    When "Robert" decides to "report a problem with the page"

    Then "Robert" should be on the "Domestic - Feedback" page
