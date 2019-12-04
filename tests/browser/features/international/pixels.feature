@pixels
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
      | selected                     |
      | Landing                      |
      | Industries                   |
      | Contact Us                   |

    @dev-only
    Examples: Industry pages
      | selected                                 |
      | Aerospace - industry                     |
      | Automotive - industry                    |
      | Creative industries - industry           |
      | Education - industry                     |
      | Engineering and manufacturing - industry |
      | Financial services - industry            |
      | Health and life sciences - industry      |
      | Legal services - industry                |
      | Space - industry                         |
      | Technology - industry                    |
