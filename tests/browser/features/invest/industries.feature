@wip
@industries
Feature: Industries page

  @CMS-159
  Scenario: Visitors should be able to view "Invest Industries" page
    Given "Robert" visits the "Invest - Industries" page

    Then "Robert" should see expected sections on "Invest - Industries" page
      | Sections         |
      | Header           |
      | Beta bar         |
      | Hero             |
      | Sectors          |
      | Report this page |
      | Footer           |


  Scenario Outline: Overseas businesses should be able to learn more about "<selected>" UK Industry from Industries page
    Given "Robert" visits the "Invest - Industries" page

    When "Robert" decides to find out out more about "<selected>"

    Then "Robert" should be on the "Invest - Industry" page
    And "Robert" should see content specific to "<selected>" industry page

    Examples: Industries
      | selected                                     |
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
