@sharing
@social-media
@allure.suite:Domestic
Feature: Domestic - Sharing on Social Media and via emails

  Background:
    Given basic authentication is done for "Domestic - Home" page


  @CMS-686
  @bug
  @CMS-733
  @fixed
  @advice
  @article
  @<social_media>
  Scenario Outline: Any Exporter should be able to share Advice article via "<social_media>"
    Given "Robert" is on randomly selected Advice article page

    When "Robert" decides to share the article via "<social_media>"

    Then "Robert" should be taken to a new tab with the "<social_media>" share page opened
    And "Robert" should see that "<social_media>" share page has been pre-populated with message and the link to the article

    Examples:
      | social_media |
      | Facebook     |
      | Twitter      |


  @CMS-686
  @bug
  @CMS-733
  @fixed
  @advice
  @article
  @linkedin
  Scenario: Any Exporter should be able to share Advice article via "LinkedIn"
    Given "Robert" is on randomly selected Advice article page

    When "Robert" decides to share the article via "LinkedIn"

    Then "Robert" should see that "LinkedIn" share link contains link to the article


  @CMS-686
  @bug
  @CMS-733
  @fixed
  @advice
  @article
  @email
  Scenario: Any Exporter should be able to share Advice article via "email"
    Given "Robert" is on randomly selected Advice article page

    When "Robert" decides to share the article via "email"

    Then "Robert" should see that the share via email link will pre-populate the message subject and body with Article title and URL
