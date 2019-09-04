@pixels
Feature: Pixels

  Background:
    Given basic authentication is done for "International - Landing" page

  Scenario Outline: Pixels should be present on "<selected>" page
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
      | selected       |
      | Home           |
      | Industries     |
      | Contact Us     |

    Examples: Industry pages
      | selected                                       |
      | Advanced manufacturing - industry              |
      | Agri-tech - industry                           |

    @full
    Examples: Industry pages
      | selected                                       |
      | Asset management - industry                    |
      | Automotive research and development - industry |
      | Automotive supply chain - industry             |
      | Capital Investment - industry                  |
      | Chemicals - industry                           |
      | Creative content and production - industry     |
      | Data Analytics - industry                      |
      | Digital media - industry                       |
      | Electrical networks - industry                 |
      | Energy - industry                              |
      | Energy from waste market - industry            |
      | Financial technology - industry                |
      | Food and drink - industry                      |
      | Free-from foods - industry                     |
      | Meat, poultry and dairy - industry             |
      | Medical technology - industry                  |
      | Motorsport - industry                          |
      | Nuclear energy - industry                      |
      | Offshore wind energy - industry                |
      | Oil and gas - industry                         |
      | Pharmaceutical manufacturing - industry        |
      | Retail - industry                              |
