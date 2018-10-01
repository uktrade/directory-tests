@pixels
Feature: Pixels

  Scenario Outline: Pixels should be present on "<selected>" page
    Given "Robert" visits the "Invest - <selected>" page

    Then following web statistics analysis or tracking elements should be present
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
      | UK Setup Guide |
      | Contact Us     |
#      | Feedback   |

    Examples: Industry pages
      | selected                                       |
      | Advanced manufacturing - industry              |
      | Aerospace - industry                           |
      | Agri-tech - industry                           |

    @full
    Examples: Industry pages
      | selected                                       |
      | Asset management - industry                    |
      | Automotive - industry                          |
      | Automotive research and development - industry |
      | Automotive supply chain - industry             |
      | Capital Investment - industry                  |
      | Chemicals - industry                           |
      | Creative content and production - industry     |
      | Creative industries - industry                 |
      | Data Analytics - industry                      |
      | Digital media - industry                       |
      | Electrical networks - industry                 |
      | Energy - industry                              |
      | Energy from waste - industry                   |
      | Financial services - industry                  |
      | Financial technology - industry                |
      | Food and drink - industry                      |
      | Free-from foods - industry                     |
      | Health and life sciences - industry            |
      | Meat, poultry and dairy - industry             |
      | Medical technology - industry                  |
      | Motorsport - industry                          |
      | Nuclear energy - industry                      |
      | Offshore wind energy - industry                |
      | Oil and gas - industry                         |
      | Pharmaceutical manufacturing - industry        |
      | Retail - industry                              |
      | Technology - industry                          |

    Examples: UK Setup Guides
      | selected                                                        |
      | Apply for a UK visa - guide                                     |
      | Establish a base for business in the UK - guide                 |
      | Hire skilled workers for your UK operations - guide             |

    @full
    Examples: UK Setup Guides
      | selected                                 |
      | Open a UK business bank account - guide  |
      | Register a company in the UK - guide     |
      | Understand UK tax and incentives - guide |
