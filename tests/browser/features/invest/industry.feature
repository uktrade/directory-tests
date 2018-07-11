@wip
@industry
Feature: Industry pages

  Scenario Outline: Visitors should be able to see the "Invest <industry>" page
    Given "Robert" visits the "Invest - <selected> industry" page

    Then "Robert" should see expected page sections
      | Header     |
      | Beta bar   |
      | Hero       |
      | Statistics |
      | Content    |
      | Footer     |

    Examples: Industries
      | selected                            |
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


  Scenario Outline: Visitors should be able to read through all of the sections on the "Invest <industry>" page
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
