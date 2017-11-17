@case-studies
Feature: Case Studies


  @ED-2655
  @home-page
  Scenario Outline: Any Exporter should get to "<relevant>" case study from Case Studies carousel on the home page
    Given "Robert" visits the "Home" page

    When "Robert" goes to the "<relevant>" Case Study via carousel

    Then "Robert" should see "<relevant>" case study with a Share widget
    Then "Robert" should see the Share Widget

    Examples:
      | relevant |
      | First    |
      | Second   |
      | Third    |


  @wip
  @ED-2656
  @<social-media>
  Scenario Outline: Any Exporter should be able to share the Case Study Article via "<social-media>"
    Given "Robert" is on the Case Study page

    When "Robert" decides to share the article via "<social-media>"

    Then "Robert" should be taken to "<social-media>" page with a message containing the link to the article

    Examples:
      | social-media |
      | Facebook     |
      | Twitter      |
      | Linked       |


  @wip
  @ED-2656
  @email
  Scenario: Any Exporter should be able to share the Case Study Article via Email
    Given "Robert" is on the Case Study page

    When "Robert" decides to share the article via "email"

    Then "Robert" should see new email window with
    And Article name should appear in the email Subject
    And link to the Article should appear in the email body
