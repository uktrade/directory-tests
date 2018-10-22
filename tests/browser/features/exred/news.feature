@news
Feature: News articles


  @wip
  Scenario: Visitors should see not see news section on "Export Readiness - Home" page if there aren't any published articles
    Given there are no news articles published on "Export Readiness"

    When "Henry" goes to the "Export Readiness - Home" page

    Then "Henry" should not see following section
      | section |
      | news    |


  @wip
  Scenario Outline: Visitors should see only up to "3" most recent news on "Export Readiness - Home" page
    Given "<a number>" published news articles on "Export Readiness"

    When "Henry" goes to the "Export Readiness - Home" page

    Then "Henry" should see "<expected number>" most recently published news articles
    And "Henry" should see a link to see all news

    Examples: number of published news articles
      | a number | expected number |
      | 1        | 1               |
      | 2        | 2               |
      | 3        | 3               |
      | 4        | 3               |


  @bug
  @CMS-553
  @fixme
  Scenario: Publishers should be able to unpublish news
    Given "Sarah" is a publisher
    And "Henry" is a visitor
    And "1" published news articles on "Export Readiness"

    When "Sarah" unpublish an article visible on the "Export Readiness - Home" page
    And "Henry" goes to the "Export Readiness - Home" page

    Then "Henry" should not see following section
      | section |
      | news    |


  @CMS-506
  Scenario: Visitors should be able to view news article
    Given at least "1" published news article on "Export Readiness"

    When "Henry" goes to the "Export Readiness - Home" page
    And "Henry" opens "first" news article

    Then "Henry" should be on the "Export Readiness - EU Exit news - Domestic" page


  @CMS-506
  Scenario: Visitors should be able to see all news
    Given at least "1" published news article on "Export Readiness"

    When "Henry" goes to the "Export Readiness - Home" page
    And "Henry" decides to "See all news"

    Then "Henry" should be on the "Export Readiness - Updates for UK companies on EU Exit - Domestic" page


  @wip
  @contact-form
  Scenario: Visitors should see be able to navigate to the "EU Exit contact form"
    Given "Henry" is on the "Export Readiness - EU Exit news - Domestic" page

    When "Henry" decides to "contact us"

    Then "Henry" should be on the "EU Exit contact form" page


  @wip
  @bug
  @CMS-557
  @fixme
  @contact-form
  Scenario: Visitors should see be able to filter out news articles by tags
    Given "Henry" is on the "Export Readiness - EU Exit news - Domestic" page

    When "Henry" decides to see related news articles by using one of the tags

    Then "Henry" should be on the "Export Readiness - Updates for UK companies on EU Exit - Domestic" page
    And "Henry" should see list of news articles filtered by selected tag


  @wip
  @bug
  @CMS-556
  @fixme
  Scenario: Visitors should see correct "Last updated" date
    Given "Sarah" is a publisher
    And "Henry" is a visitor
    And at least "1" published news articles on "Export Readiness"

    When "Sarah" updates an article visible on the "Export Readiness - Home" page
    And "Henry" goes to the "Export Readiness - Home" page

    Then "Henry" should see that updated news article has a correct "Last updated" date
