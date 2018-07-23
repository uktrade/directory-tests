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
      | selected                                     |
      | Advanced manufacturing Industry              |
      | Aerospace Industry                           |
      | Agri-tech Industry                           |
      | Asset management Industry                    |
      | Automotive Industry                          |
      | Automotive research and development Industry |
      | Automotive supply chain Industry             |
      | Capital Investment Industry                  |
      | Chemicals Industry                           |
      | Creative content and production Industry     |
      | Creative industries Industry                 |
      | Data Analytics Industry                      |
      | Digital media Industry                       |
      | Electrical networks Industry                 |
      | Energy Industry                              |
      | Energy from waste Industry                   |
      | Financial services Industry                  |
      | Financial technology Industry                |
      | Food and drink Industry                      |
      | Free-from foods Industry                     |
      | Health and life sciences Industry            |
      | Meat, poultry and dairy Industry             |
      | Medical technology Industry                  |
      | Motorsport Industry                          |
      | Nuclear energy Industry                      |
      | Offshore wind energy Industry                |
      | Oil and gas Industry                         |
      | Pharmaceutical manufacturing Industry        |
      | Retail Industry                              |
      | Technology Industry                          |

    Examples: UK Setup Guides
      | selected                                                      |
      | Apply for a UK visa guide                                     |
      | Establish a base for business in the UK guide                 |
      | Hire skilled workers for your UK operations guide             |
      | Open a UK business bank account guide                         |
      | Set up a company in the UK guide                              |
      | Understand the UK's tax, incentives and legal framework guide |
