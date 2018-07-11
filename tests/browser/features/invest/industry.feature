@wip
@industry
Feature: Industry pages

  @CMS-160
  Scenario Outline: Visitors should be able to see the "Invest - <selected> industry" page
    Given "Robert" visits the "Invest - <selected> industry" page

    Then "Robert" should see expected sections on "Invest - Industry" page
      | Sections         |
      | Header           |
      | Beta bar         |
      | Hero             |
      | Industry pullout |
      | Big number       |
      | Content          |
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
    Given "Robert" visits the "Invest - <selected> industry" page

    Then "Robert" should see expected sections on "Invest - Industry" page
      | Sections           |
      | Header             |
      | Beta bar           |
      | Hero               |
      | Industry pullout   |
      | Big number         |
      | Content            |
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
    Given "Robert" visits the "Invest - <selected> industry" page

    When "Robert" unfolds all content sections

    Then "Robert" should see content for every section

    Examples: Industries
      | selected                                     |
      | Advanced manufacturing              |
      | Aerospace                           |
      | Agri-tech                           |
      | Asset management                    |
      | Automotive                          |
      | Automotive research and development |
      | Automotive supply chain             |
      | Capital Investment                  |
      | Chemicals                           |
      | Creative content and production     |
      | Creative industries                 |
      | Data Analytics                      |
      | Digital media                       |
      | Electrical networks                 |
      | Energy                              |
      | Energy from waste                   |
      | Financial services                  |
      | Financial technology                |
      | Food and drink                      |
      | Free-from foods                     |
      | Health and life sciences            |
      | Meat, poultry and dairy             |
      | Medical technology                  |
      | Motorsport                          |
      | Nuclear energy                      |
      | Offshore wind energy                |
      | Oil and gas                         |
      | Pharmaceutical manufacturing        |
      | Retail                              |
      | Technology                          |
