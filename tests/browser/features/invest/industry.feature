@industry
Feature: Industry pages

  @CMS-160
  Scenario Outline: Visitors should be able to see the "Invest - <selected> industry" page
    Given "Robert" visits the "Invest - <selected> - industry" page

    When "Robert" unfolds all topic sections

    Then "Robert" should see following sections
      | Sections         |
      | Header           |
      | Beta bar         |
      | Hero             |
      | Industry pullout |
      | Big number       |
      | Topics           |
      | Topics contents  |
      | Report this page |
      | Footer           |

    Examples: Industries
      | selected                            |
      | Advanced manufacturing              |
      | Aerospace                           |
      | Agri-tech                           |
      | Asset management                    |
      | Automotive research and development |
      | Automotive supply chain             |
      | Capital Investment                  |
      | Chemicals                           |
      | Creative content and production     |
      | Data Analytics                      |
      | Digital media                       |
      | Electrical networks                 |
      | Energy from waste                   |
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
      | Beta bar           |
      | Hero               |
      | Industry pullout   |
      | Big number         |
      | Topics             |
      | Topics contents    |
      | Related industries |
      | Report this page   |
      | Footer             |

    Examples: Industries
      | selected                 |
      | Automotive               |
      | Creative industries      |
      | Energy                   |
      | Financial services       |
      | Food and drink           |
      | Health and life sciences |
      | Technology               |
