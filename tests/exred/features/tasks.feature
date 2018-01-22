@tasks
@articles
Feature: Articles


  @wip
  @ED-2774
  @out-of-scope
  Scenario: Any Exporter should see his task completion progress on the articles list page
    Given "Robert" is on the Article page

    When "Robert" marks any task as completed
    And "Robert" goes back to the Article List page

    Then "Robert" should see the tasks completed counter increased by 1


  @wip
  @ED-2774
  @out-of-scope
  Scenario: Any Exporter should see his task completion progress on the article page
    Given "Robert" is on the Article page
    And "Robert" marks any task as completed
    And "Robert" went back to the Article List page

    When "Robert" views the same article

    Then "Robert" should see the tasks he already marked as completed
