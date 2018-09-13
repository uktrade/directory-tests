@industries
@no-sso-email-verification-required
Feature: Industries page

  @CMS-159
  Scenario: Visitors should be able to view "Invest Industries" page
    Given "Robert" visits the "Invest - Industries" page

    Then "Robert" should see following sections
      | Sections         |
      | Header           |
      | Beta bar         |
      | Hero             |
      | Sectors          |
      | Report this page |
      | Footer           |


  @CMS-159
  Scenario Outline: Overseas businesses should be able to learn more about "<selected>" UK Industry from Industries page
    Given "Robert" visits the "Invest - Industries" page

    When "Robert" decides to find out out more about "Invest - <selected> - industry"

    Then "Robert" should be on the "Invest - <selected> - industry" page
    And "Robert" should see content specific to "Invest - <selected> - industry" page

    Examples: Industries
      | selected                            |
      | Advanced manufacturing              |
      | Aerospace                           |
      | Agri-tech                           |

    @full
    Examples: Industries
      | selected                            |
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
