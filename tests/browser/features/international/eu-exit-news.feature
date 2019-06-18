@international
Feature: Updates for non-UK companies on EU Exit

  Background:
    Given basic authentication is done for "Export Readiness - Home" page

  @news
  @eu-exit
  @CMS-579
  Scenario: International Visitors should be able to view news article
    Given at least "1" published "international" news article on "Export Readiness"

    When "Henry" goes to the "International - Updates for non UK companies on EU Exit" page
    And "Henry" opens "first" news article

    Then "Henry" should be on the "International - EU Exit news - article" page


  @news
  @eu-exit
  @CMS-579
  Scenario: International Visitors should be able to ge to the "Updates for non-UK companies on EU Exit" from "International - Landing" page
    Given at least "1" published "international" news article on "Export Readiness"
    And "Henry" went to the "International - Landing" page

    When "Henry" decides to "See our updates on EU Exit"

    Then "Henry" should be on the "Export Readiness - Updates for non UK companies on EU Exit" page
    And "Henry" should see following sections
      | sections        |
      | Header          |
      | Beta Bar        |
      | Hero            |
      | Articles        |
      | Contact us      |
      | Error reporting |
      | Footer          |


  @CMS-579
  @eu-exit
  @contact-form
  Scenario: International Visitors should see be able to navigate to the "EU Exit contact form"
    Given "Henry" went to the "International - Updates for non UK companies on EU Exit" page

    When "Henry" decides to "Contact us"

    Then "Henry" should be on the "International - EU Exit - Contact us" page


  @wip
  @news
  @eu-exit
  @CMS-579
  @tags
  Scenario: International Visitors should see be able to filter out news articles by tags
    Given "Henry" opened random "international" news article

    When "Henry" decides to see related news articles by using one of the tags

    Then "Henry" should be on the "Export Readiness - Search by tag" page
    And "Henry" should see list of news articles filtered by selected tag
    And "Henry" should see following sections
      | sections        |
      | Hero            |
      | Article List    |
      | Error reporting |


  @CMS-579
  @eu-exit
  @breadcrumbs
  Scenario: International Visitors should see be able to get to "International" page by using "Great.gov.uk" breadcrumb on "Updates for non-UK companies on EU Exit" page
    Given "Henry" went to the "International - Updates for non UK companies on EU Exit" page

    When "Henry" decides to open "Great.gov.uk"

    Then "Henry" should be on the "International - Landing" page


  @news
  @eu-exit
  @CMS-579
  @breadcrumbs
  Scenario: International Visitors should see be able to get to "International" page by using "Great.gov.uk" breadcrumb on international news article page
    Given "Henry" opened random "international" news article

    When "Henry" decides to see "Updates for companies on EU Exit"

    Then "Henry" should be on the "International - Landing" page


  @news
  @eu-exit
  @CMS-579
  @breadcrumbs
  Scenario Outline: International Visitors should see be able to get to "<expected page>" by using "<breadcrumb>" breadcrumb on "International EU Exit news" page
    Given "Henry" opened random "international" news article

    When "Henry" decides to open "<breadcrumb>"

    Then "Henry" should be on the "<expected page>" page

    Examples: breadcrumbs
      | breadcrumb                              | expected page                                              |
      | Great.gov.uk                            | International - Landing                                    |
      | Updates for non-UK companies on EU exit | Export Readiness - Updates for non UK companies on EU Exit |


  @wip
  @news
  @eu-exit
  @bug
  @fixme
  Scenario: International Visitors should see not see news section on "International - Landing" page if there aren't any published articles
    Given there are no "international" news articles published on "Export Readiness"

    When "Henry" goes to the "International - Landing" page

    Then "Henry" should not see following section
      | section         |
      | EU Exit updates |


  @bug
  @CMS-553
  @fixme
  @news
  @eu-exit
  Scenario: Publishers should be able to unpublish International news
    Given "Sarah" is a publisher
    And "Henry" is a visitor
    And "1" published "international" news articles on "Export Readiness"

    When "Sarah" unpublish an article visible on the "International - Landing" page
    And "Henry" goes to the "International - Updates for non UK companies on EU Exit - International" page

    Then "Henry" should see "0" most recently published "international" news articles

  @wip
  @bug
  @CMS-556
  @fixme
  @news
  @eu-exit
  Scenario: International Visitors should see correct "Last updated" date
    Given "Sarah" is a publisher
    And "Henry" is a visitor
    And at least "1" published "international" news articles on "Export Readiness"

    When "Sarah" updates an article visible on the "Export Readiness - Updates for non UK companies on EU Exit - International" page
    And "Henry" goes to the "International - Updates for non UK companies on EU Exit - International" page

    Then "Henry" should see that updated news article has a correct "Last updated" date
