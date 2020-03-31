@pixels
@allure.suite:Domestic
Feature: Domestic - Pixels

  Background:
    Given basic authentication is done for "Domestic - Home" page

  @international
  Scenario Outline: Pixels should be present on "International - <selected>" page
    Given "Robert" visited "Domestic - <selected>" page

    Then "Robert" should be on the "Domestic - <selected>" page
    And following web statistics analysis or tracking elements should be present
      | Google Tag Manager             |
      | Google Tag Manager - no script |
      | UTM Cookie Domain              |
    And following web statistics analysis or tracking elements should NOT be present
      | LinkedIn tracking pixel |
      | Facebook tracking pixel |

    Examples: Various pages
      | selected                                                           |
      | Home                                                               |
      | Advice landing                                                     |
      | Contact us                                                         |
      | Feedback - contact us                                              |
      | Find an export market - Article list                               |
      | Get finance                                                        |
      | Join our Export Community - form                                   |
      | Join our export community - landing                                |
      | Markets listing                                                    |
      | Services                                                           |
      | Trade finance                                                      |
      | What can we help you with? - Domestic Contact us                   |
      | What would you like to know more about? - International Contact us |
