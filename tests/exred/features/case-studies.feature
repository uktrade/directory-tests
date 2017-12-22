@case-studies
Feature: Case Studies


  @ED-2655
  @home-page
  Scenario Outline: Any Exporter should get to "<relevant>" case study from Case Studies carousel on the home page
    Given "Robert" visits the "Home" page

    When "Robert" goes to the "<relevant>" Case Study via carousel

    Then "Robert" should see "<relevant>" case study
    And "Robert" should see the Share Widget

    Examples:
      | relevant |
      | First    |
      | Second   |
      | Third    |


  @ED-2656
  @<social-media>
  Scenario Outline: Any Exporter should be able to share the Case Study Article via "<social-media>"
    Given "Robert" is on the Case Study page accessed via "Home" page

    When "Robert" decides to share the article via "<social-media>"

    Then "Robert" should be taken to a new tab with the "<social-media>" share page opened
    And "Robert" should that "<social-media>" share page has been pre-populated with message and the link to the article

    Examples:
      | social-media |
      | Facebook     |
      | Twitter      |
      | LinkedIn     |


  @ED-2656
  @email
  Scenario: Any Exporter should be able to share the Case Study Article via Email
    Given "Robert" is on the Case Study page accessed via "Home" page

    When "Robert" decides to share the article via "email"

    Then "Robert" should see that the share via email link will pre-populate the message subject and body with Article title and URL
