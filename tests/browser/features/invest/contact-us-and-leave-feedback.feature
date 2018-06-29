@wip
@ontact-us
Feature: Contact us & Leave feedback


  @beta
  @feedback
  @header
  @footer
  Scenario Outline: Visitors should be able to access feedback form from "<selected>" page
    Given "Robert" visits the "<selected>" page

    When "Robert" decides to leave some feedback

    Then "Robert" should be on the "Invest - Feedback" page

    Examples: Various pages
      | selected                |
      | Invest - Home           |
      | Invest - Industries     |
      | Invest - UK Setup Guide |
      | Invest - Contact Us     |
      | Invest - Feedback       |

    Examples: Industry pages
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

    Examples: UK Setup Guides
      | selected                                                         |
      | Invest - Apply for a UK visa                                     |
      | Invest - Establish a base for business in the UK                 |
      | Invest - Hire skilled workers for your UK operations             |
      | Invest - Open a UK business bank account                         |
      | Invest - Set up a company in the UK                              |
      | Invest - Understand the UK's tax, incentives and legal framework |


  @contact-us
  @header
  @footer
  Scenario Outline: Visitors should be able to contact us from "<selected>" page
    Given "Robert" visits the "<selected>" page
    And "Robert" decided to "contact us"

    When "Robert" fills out and submits the contact us form

    Then "Robert" should be on the "Invest - Thank you for your message" page

    Examples: Various pages
      | selected                |
      | Invest - Home           |
      | Invest - Industries     |
      | Invest - UK Setup Guide |
      | Invest - Contact Us     |
      | Invest - Feedback       |
