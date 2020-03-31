@pixels
@allure.suite:International
Feature: INTL - Pixels

  Background:
    Given basic authentication is done for "International - Landing" page

  @international
  Scenario Outline: Pixels should be present on "International - <selected>" page
    Given "Robert" visits the "International - <selected>" page

    Then "Robert" should be on the "International - <selected>" page
    And following web statistics analysis or tracking elements should be present
      | Google Tag Manager             |
      | Google Tag Manager - no script |
      | UTM Cookie Domain              |
    And following web statistics analysis or tracking elements should NOT be present
      | LinkedIn tracking pixel |
      | Facebook tracking pixel |

    Examples: Various pages
      | selected                        |
      | Landing                         |
      | Industries                      |
      | About the UK                    |
      | About us                        |
      | How we help you buy from the UK |

    @dev-only
    Examples: Industry pages
      | selected                                 |
      | Aerospace - industry                     |
      | Automotive - industry                    |
      | Creative industries - industry           |
      | Education - industry                     |
      | Engineering and manufacturing - industry |
      | Financial services - industry            |
      | Healthcare and life sciences - industry  |
      | Legal services - industry                |
      | Space - industry                         |
      | Technology - industry                    |

    @stage-only
    Examples: Industry pages
      | selected                                 |
      | Creative industries - industry           |
      | Energy - industry                        |
      | Engineering and manufacturing - industry |
      | Healthcare and life sciences - industry  |
      | Legal services - industry                |
      | Real estate - industry                   |
      | Technology - industry                    |
