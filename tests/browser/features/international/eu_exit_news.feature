@international
@allure.suite:International
Feature: INTL - Updates for non-UK companies on EU Exit

  Background:
    Given test authentication is done

  @news
  @eu-exit
  @allure.link:CMS-579
  Scenario: International Visitors should be able to view news article
    Given at least "1" published "international" news article on "Domestic"

    When "Henry" goes to the "International - Updates for non UK companies on EU Exit" page
    And "Henry" opens "first" news article

    Then "Henry" should be on the "International - EU Exit news - article" page


  @news
  @eu-exit
  @allure.link:CMS-579
  Scenario: International Visitors should be able to ge to the "Updates for non-UK companies on EU Exit" from "International - Landing" page
    Given at least "1" published "international" news article on "Domestic"
    And "Henry" went to the "International - Landing" page

    When "Henry" decides to "See our updates on EU Exit"

    Then "Henry" should be on the "Domestic - Updates for non UK companies on EU Exit" page
    And "Henry" should see following sections
      | sections        |
      | Header          |
      | Beta Bar        |
      | Hero            |
      | Articles        |
      | Contact us      |
      | Error reporting |
      | Footer          |


  @allure.link:CMS-579
  @eu-exit
  @contact-form
  Scenario: International Visitors should see be able to navigate to the "EU Exit contact form"
    Given "Henry" went to the "International - Updates for non UK companies on EU Exit" page

    When "Henry" decides to "Contact us"

    Then "Henry" should be on the "International - EU Exit - Contact us" page


  @allure.link:CMS-579
  @eu-exit
  @breadcrumbs
  Scenario: International Visitors should see be able to get to "International" page by using "Great.gov.uk" breadcrumb on "Updates for non-UK companies on EU Exit" page
    Given "Henry" went to the "International - Updates for non UK companies on EU Exit" page

    When "Henry" decides to open "Great.gov.uk"

    Then "Henry" should be on the "International - Landing" page


  @news
  @eu-exit
  @allure.link:CMS-579
  @breadcrumbs
  Scenario: International Visitors should see be able to get to "International" page by using "Great.gov.uk" breadcrumb on international news article page
    Given "Henry" opened random "international" news article

    When "Henry" decides to see "Updates for companies on EU Exit"

    Then "Henry" should be on the "International - Landing" page


  @news
  @eu-exit
  @allure.link:CMS-579
  @breadcrumbs
  Scenario Outline: International Visitors should see be able to get to "<expected page>" by using "<breadcrumb>" breadcrumb on "International EU Exit news" page
    Given "Henry" opened random "international" news article

    When "Henry" decides to open "<breadcrumb>"

    Then "Henry" should be on the "<expected page>" page

    Examples: breadcrumbs
      | breadcrumb                              | expected page                                      |
      | Great.gov.uk                            | International - Landing                            |
      | Updates for non-UK companies on EU exit | Domestic - Updates for non UK companies on EU Exit |


  @wip
  @news
  @eu-exit
  @bug
  @fixme
  Scenario: International Visitors should see not see news section on "International - Landing" page if there aren't any published articles
    Given there are no "international" news articles published on "Domestic"

    When "Henry" goes to the "International - Landing" page

    Then "Henry" should not see following section
      | section         |
      | EU Exit updates |


  @bug
  @allure.issue:CMS-553
  @fixme
  @news
  @eu-exit
  Scenario: Publishers should be able to unpublish International news
    Given "Sarah" is a publisher
    And "Henry" is a visitor
    And "1" published "international" news articles on "Domestic"

    When "Sarah" unpublish an article visible on the "International - Landing" page
    And "Henry" goes to the "International - Updates for non UK companies on EU Exit - Content" page

    Then "Henry" should see "0" most recently published "international" news articles

  @wip
  @bug
  @allure.issue:CMS-556
  @fixme
  @news
  @eu-exit
  Scenario: International Visitors should see correct "Last updated" date
    Given "Sarah" is a publisher
    And "Henry" is a visitor
    And at least "1" published "international" news articles on "Domestic"

    When "Sarah" updates an article visible on the "Domestic - Updates for non UK companies on EU Exit - Content" page
    And "Henry" goes to the "International - Updates for non UK companies on EU Exit - Content" page

    Then "Henry" should see that updated news article has a correct "Last updated" date
