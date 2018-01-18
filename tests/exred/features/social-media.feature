@sharing
@social-media
Feature: Sharing on Social Media and via emails


  @ED-2640
  @articles
  @<group>
  @<social_media>
  Scenario Outline: Any Exporter should be able to share the article via "<social_media>"
    Given "Robert" is on the "<group>" Article List for randomly selected category
    And "Robert" opened any Article

    When "Robert" decides to share the article via "<social_media>"

    Then "Robert" should be taken to a new tab with the "<social_media>" share page opened
    And "Robert" should that "<social_media>" share page has been pre-populated with message and the link to the article

    Examples:
      | group            | social_media |
      | Export Readiness | Facebook     |
      | Guidance         | Twitter      |
      | Export Readiness | LinkedIn     |


  @ED-2640
  @articles
  @<group>
  @<social_media>
  Scenario Outline: Any Exporter should be able to share the article via "<social_media>"
    Given "Robert" is on the "<group>" Article List for randomly selected category
    And "Robert" opened any Article

    When "Robert" decides to share the article via "<social_media>"

    Then "Robert" should see that the share via email link will pre-populate the message subject and body with Article title and URL

    Examples:
      | group            | social_media |
      | Guidance         | email        |


  @ED-2656
  @case-studies
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
  @case-studies
  @email
  Scenario: Any Exporter should be able to share the Case Study Article via Email
    Given "Robert" is on the Case Study page accessed via "Home" page

    When "Robert" decides to share the article via "email"

    Then "Robert" should see that the share via email link will pre-populate the message subject and body with Article title and URL
