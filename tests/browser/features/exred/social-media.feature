@sharing
@social-media
Feature: Sharing on Social Media and via emails

  Background:
    Given hawk cookie is set on "Export Readiness - Home" page


  @ED-2656
  @case-studies
  @<social-media>
  Scenario Outline: Any Exporter should be able to share the Case Study Article via "<social-media>"
    Given "Robert" is on the Case Study page accessed via "Export Readiness - Home" page

    When "Robert" decides to share the article via "<social-media>"

    Then "Robert" should be taken to a new tab with the "<social-media>" share page opened
    And "Robert" should see that "<social-media>" share page has been pre-populated with message and the link to the article

    Examples:
      | social-media |
      | Facebook     |
      | Twitter      |


  @ED-2656
  @case-studies
  @linkedin
  Scenario: Any Exporter should be able to share the Case Study Article via "LinkedIn"
    Given "Robert" is on the Case Study page accessed via "Export Readiness - Home" page

    When "Robert" decides to share the article via "LinkedIn"

    Then "Robert" should see that "LinkedIn" share link contains link to the article


  @ED-2656
  @case-studies
  @email
  Scenario: Any Exporter should be able to share the Case Study Article via Email
    Given "Robert" is on the Case Study page accessed via "Export Readiness - Home" page

    When "Robert" decides to share the article via "email"

    Then "Robert" should see that the share via email link will pre-populate the message subject and body with Article title and URL
