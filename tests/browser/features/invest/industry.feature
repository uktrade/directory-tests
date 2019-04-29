@industry
Feature: Industry pages

  Background:
    Given basic authentication is done for "Invest - Home" page
    
  @CMS-160
  Scenario Outline: Visitors should be able to see the "Invest - <selected> industry" page
    Given "Robert" visits the "Invest - <selected> - industry" page

    When "Robert" unfolds all topic sections

    Then "Robert" should see following sections
      | Sections         |
      | Header           |
#      | Beta bar         |
      | Hero             |
      | Industry pullout |
      | Big number       |
      | Topics           |
      | Topics contents  |
      | Error reporting  |
      | Footer           |

    Examples: Industries
      | selected                            |
      | Advanced manufacturing              |
      | Aerospace                           |
      | Agri-tech                           |
      | Asset management                    |

    @full
    Examples: Industries
      | selected                            |
      | Automotive research and development |
      | Automotive supply chain             |
      | Capital investment                  |
      | Chemicals                           |
      | Creative content and production     |
      | Data Analytics                      |
      | Digital media                       |
      | Electrical networks                 |
      | Energy from waste market            |
      | Financial technology                |
      | Free-from foods                     |
      | Meat, poultry and dairy             |
      | Medical technology                  |
      | Motorsport                          |
      | Nuclear energy                      |
      | Offshore wind energy                |
      | Oil and gas                         |
      | Pharmaceutical manufacturing        |
      | Retail                              |


  @CMS-160
  Scenario Outline: Visitors should be able to see the "Invest - <selected> industry" page with related Industries
    Given "Robert" visits the "Invest - <selected> - industry" page

    When "Robert" unfolds all topic sections

    Then "Robert" should see following sections
      | Sections           |
      | Header             |
#      | Beta bar           |
      | Hero               |
      | Industry pullout   |
      | Big number         |
      | Topics             |
      | Topics contents    |
      | Related industries |
      | Error reporting    |
      | Footer             |

    Examples: Industries
      | selected                 |
      | Automotive               |
      | Creative industries      |
      | Energy                   |

    @full
    Examples: Industries
      | selected                 |
      | Financial services       |
      | Food and drink           |
      | Health and life sciences |
      | Technology               |
