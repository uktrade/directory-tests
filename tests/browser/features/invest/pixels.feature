@pixels
@allure.suite:Invest
Feature: Invest - Pixels

  Background:
    Given basic authentication is done for "International - Landing" page

  Scenario Outline: Pixels should be present on "Invest - <selected>" page
    Given "Robert" visits the "Invest - <selected>" page

    Then "Robert" should be on the "Invest - <selected>" page
    And following web statistics analysis or tracking elements should be present
      | Google Tag Manager             |
      | Google Tag Manager - no script |
      | UTM Cookie Domain              |
    And following web statistics analysis or tracking elements should NOT be present
      | LinkedIn tracking pixel |
      | Facebook tracking pixel |

    Examples: Various pages
      | selected                |
      | Landing                 |
      | Contact Us              |
      | How to set up in the UK |

    @stage-only
    Examples: HPO pages
      | selected                               |
      | High productivity food production - HPO|
      | Lightweight structures - HPO           |
      | Rail infrastructure - HPO              |

    @dev-only
    Examples: UK Setup Guides
      | selected                                          |
      | DIT's Guide to UK Venture Capital Schemes - guide |
      | DIT's guide to UK Capital Gains Tax - guide       |
      | UK infrastructure - guide                         |
      | DIT's guide to UK Corporation Tax - guide         |
      | Access finance in the UK - guide                  |
      | Register a company in the UK - guide              |
      | UK talent and labour - guide                      |
      | Establish a UK business base - guide              |
      | UK innovation - guide                             |
