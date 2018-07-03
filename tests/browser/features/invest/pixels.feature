@pixels
Feature: Pixels

  Scenario Outline: Pixels should be present on "<selected>" page
    Given "Robert" visits the "<selected>" page

    Then following web statistics analysis or tracking elements should be present
      | Google Tag Manager             |
      | Google Tag Manager - no script |
      | UTM Cookie Domain              |

    And following web statistics analysis or tracking elements should NOT be present
      | LinkedIn tracking pixel |
      | Facebook tracking pixel |

    Examples: Various pages
      | selected            |
      | Invest - Home       |
      | Invest - Industries |
      | Invest - Guide      |
      | Invest - Contact Us |
#      | Invest - Feedback   |

    Examples: Industry pages
      | selected                                              |
      | Invest - Advanced manufacturing Industry              |
      | Invest - Aerospace Industry                           |
      | Invest - Agri-tech Industry                           |
      | Invest - Asset management Industry                    |
      | Invest - Automotive Industry                          |
      | Invest - Automotive research and development Industry |
      | Invest - Automotive supply chain Industry             |
      | Invest - Capital Investment Industry                  |
      | Invest - Chemicals Industry                           |
      | Invest - Creative content and production Industry     |
      | Invest - Creative industries Industry                 |
      | Invest - Data Analytics Industry                      |
      | Invest - Digital media Industry                       |
      | Invest - Electrical networks Industry                 |
      | Invest - Energy Industry                              |
      | Invest - Energy from waste Industry                   |
      | Invest - Financial services Industry                  |
      | Invest - Financial technology Industry                |
      | Invest - Food and drink Industry                      |
      | Invest - Free-from foods Industry                     |
      | Invest - Health and life sciences Industry            |
      | Invest - Meat, poultry and dairy Industry             |
      | Invest - Medical technology Industry                  |
      | Invest - Motorsport Industry                          |
      | Invest - Nuclear energy Industry                      |
      | Invest - Offshore wind energy Industry                |
      | Invest - Oil and gas Industry                         |
      | Invest - Pharmaceutical manufacturing Industry        |
      | Invest - Retail Industry                              |
      | Invest - Technology Industry                          |

    Examples: UK Setup Guides
      | selected                                                         |
      | Invest - Apply for a UK visa                                     |
      | Invest - Establish a base for business in the UK                 |
      | Invest - Hire skilled workers for your UK operations             |
      | Invest - Open a UK business bank account                         |
      | Invest - Set up a company in the UK                              |
#      | Invest - Understand the UK's tax, incentives and legal framework |
