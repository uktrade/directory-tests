@advice
@allure.suite:Domestic
Feature: Domestic - Advice articles

  Background:
    Given test authentication is done


  @allure.link:CMS-686
  @home-page
  @articles
  Scenario: Any Exporter should see all expected sections on "Domestic - Advice landing" page
    When "Robert" goes to the "Domestic - Advice landing" page

    Then "Robert" should see following sections
      | sections                 |
      | Header                   |
      | Hero                     |
      | Breadcrumbs              |
      | Advice & Guidance tiles  |
      | Error reporting          |
      | Footer                   |


  @allure.link:CMS-686
  @home-page
  @articles
  Scenario: Any Exporter should be able to get to a list of Advice articles from the home page using link in "<specific>" section
    Given "Robert" visits the "Domestic - Advice landing" page

    When "Robert" opens any article on the list

    Then "Robert" should be on the "Domestic - Advice article list" page
    And "Robert" should see following sections
      | sections                 |
      | Header                   |
      | Hero                     |
      | Breadcrumbs              |
      | List of articles         |
      | Error reporting          |
      | Footer                   |


  @allure.link:CMS-686
  @home-page
  @articles
  Scenario Outline: Any Exporter should be able to get to "<advice>" Advice article
    Given "Robert" visits the "Domestic - <advice> - Article list" page

    When "Robert" opens any article on the list

    Then "Robert" should be on the "Domestic - Advice article" page
    And "Robert" should see following sections
      | sections        |
      | Header          |
      | Breadcrumbs     |
      | Share buttons   |
      | Article         |
      | Error reporting |
      | Footer          |

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

    @bug
    @allure.issue:TT-2311
    @fixme
    Examples: None of "Prepare for export procedures and logistics" pages work in Dev & Staging
      | advice                                      |
      | Prepare for export procedures and logistics |


  @allure.link:CMS-686
  @report
  Scenario: Any Exporter should be able to report a problem with Advice Article page
    Given "Robert" is on randomly selected Advice article page

    When "Robert" decides to report a problem with the page

    Then "Robert" should be on the "Domestic - Feedback - contact us" page


  @bug
  @allure.issue:CMS-1698
  @fixed
  @allure.link:CMS-686
  @breadcrumbs
  Scenario Outline: Any Exporter should see be to use "<breadcrumb>" breadcrumb on "Advice article" page to get to "<target>" page
    Given "Robert" is on randomly selected Advice article page

    When "Robert" decides to open "<breadcrumb>"

    Then "Robert" should be on the "Domestic - <target>" page or be redirected to "International - Landing" page

    Examples:
      | breadcrumb   | target              |
      | great.gov.uk | Home                |
      | Advice       | Advice Landing      |
      | Article list | Advice article list |
