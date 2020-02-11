@dev-only
@regional-pages
@allure.suite:International
Feature: International - Regional pages

  Background:
    Given basic authentication is done for "International - Landing" page


  @allure.link:CMS-215
  Scenario: Visitors should be able to see all expected sections on "International - Regions" page
    Given "Robert" visits the "International - Regions" page

    Then "Robert" should see following sections
      | Sections         |
      | Header           |
      | Hero             |
      | Breadcrumbs      |
      | Regions list     |
      | The UK map       |
      | Contact us       |
      | Error reporting  |
      | Footer           |


  @allure.link:CMS-215
  @link
  @anchor
  Scenario Outline: Visitors should be able to find out more about "<region>" using regular page links
    Given "Robert" visits the "International - Regions" page

    When "Robert" decides to find out more about "<region>"

    Then "Robert" should be on the "International - <region> - region" page
    And "Robert" should see following sections
      | Sections         |
      | Header           |
      | Hero             |
      | Error reporting  |
      | Footer           |
    And "Robert" should see content specific to "International - <region> - region" page

    Examples: Regions
      | region           |
      | Scotland         |
      | Northern Ireland |
      | North England    |
      | Wales            |
      | Midlands         |
      | South England    |


  @allure.link:CMS-215
  @link
  @map
  @skip-in-firefox
  Scenario Outline: Visitors should be able to find out more about "<region>" using links on UK map
    Given "Robert" visits the "International - Regions" page

    When "Robert" decides to use "<region> - svg" link

    Then "Robert" should be on the "International - <region> - region" page
    And "Robert" should see following sections
      | Sections         |
      | Header           |
      | Hero             |
      | Error reporting  |
      | Footer           |
    And "Robert" should see content specific to "International - <region> - region" page

    Examples: Regions
      | region           |
      | Scotland         |
      | Northern Ireland |
      | North England    |
      | Wales            |
      | Midlands         |
      | South England    |


  @allure.link:CMS-215
  @breadcrumbs
  Scenario Outline: Visitors should be able to go back to the "Regions" page via breadcrumb on "<region>" page
    Given "Robert" visits the "International - <region> - region" page

    When "Robert" decides to find out more about "regions"

    Then "Robert" should be on the "International - Regions" page

    Examples: UK Regions
      | region           |
      | North England    |
      | Northern Ireland |
      | South England    |
      | Midlands         |
      | Wales            |

    @wip
    Examples: Other regional pages without breadcrumbs
      | region           |
      | Scotland         |
