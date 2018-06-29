@wip
@industry
Feature: Industry pages

  Scenario Outline: Visitors should be able to see the "Invest <industry>" page
    Given "Robert" visits the "Invest <industry>" page

    Then "Robert" should see expected page sections
      | Header     |
      | Beta bar   |
      | Hero       |
      | Statistics |
      | Content    |
      | Footer     |

    Examples: Industries
      | industry                                     |
      | Invest - Advanced manufacturing              |
      | Invest - Aerospace                           |
      | Invest - Agri-tech                           |
      | Invest - Asset management                    |
      | Invest - Automotive                          |
      | Invest - Automotive research and development |
      | Invest - Automotive supply chain             |
      | Invest - Capital Investment                  |
      | Invest - Chemicals                           |
      | Invest - Creative content and production     |
      | Invest - Creative industries                 |
      | Invest - Data Analytics                      |
      | Invest - Digital media                       |
      | Invest - Electrical networks                 |
      | Invest - Energy                              |
      | Invest - Energy from waste                   |
      | Invest - Financial services                  |
      | Invest - Financial technology                |
      | Invest - Food and drink                      |
      | Invest - Free-from foods                     |
      | Invest - Health and life sciences            |
      | Invest - Meat, poultry and dairy             |
      | Invest - Medical technology                  |
      | Invest - Motorsport                          |
      | Invest - Nuclear energy                      |
      | Invest - Offshore wind energy                |
      | Invest - Oil and gas                         |
      | Invest - Pharmaceutical manufacturing        |
      | Invest - Retail                              |
      | Invest - Technology                          |


  Scenario Outline: Visitors should be able to read through all of the sections on the "Invest <industry>" page
    Given "Robert" visits the "Invest <industry>" page

    When "Robert" unfolds all content sections

    Then "Robert" should see content for every section

    Examples: Industries
      | industry                                     |
      | Invest - Advanced manufacturing              |
      | Invest - Aerospace                           |
      | Invest - Agri-tech                           |
      | Invest - Asset management                    |
      | Invest - Automotive                          |
      | Invest - Automotive research and development |
      | Invest - Automotive supply chain             |
      | Invest - Capital Investment                  |
      | Invest - Chemicals                           |
      | Invest - Creative content and production     |
      | Invest - Creative industries                 |
      | Invest - Data Analytics                      |
      | Invest - Digital media                       |
      | Invest - Electrical networks                 |
      | Invest - Energy                              |
      | Invest - Energy from waste                   |
      | Invest - Financial services                  |
      | Invest - Financial technology                |
      | Invest - Food and drink                      |
      | Invest - Free-from foods                     |
      | Invest - Health and life sciences            |
      | Invest - Meat, poultry and dairy             |
      | Invest - Medical technology                  |
      | Invest - Motorsport                          |
      | Invest - Nuclear energy                      |
      | Invest - Offshore wind energy                |
      | Invest - Oil and gas                         |
      | Invest - Pharmaceutical manufacturing        |
      | Invest - Retail                              |
      | Invest - Technology                          |
