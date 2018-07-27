@wip
@contact-us
Feature: Contact us & Leave feedback


  @CMS-163
  @beta
  @feedback
  @header
  @footer
  Scenario Outline: Visitors should be able to access feedback form from "<selected>" page
    Given "Robert" visits the "Invest - <selected>" page

    When "Robert" decides to use "Feedback" link on "Invest - <selected>" page

    Then "Robert" should be on the "Invest - Feedback" page

    Examples: Various pages
      | selected       |
      | Home           |
      | Industries     |
      | UK Setup Guide |

    Examples: Industry pages
      | selected                                       |
      | Advanced manufacturing - industry              |
      | Aerospace - industry                           |
      | Agri-tech - industry                           |
      | Asset management - industry                    |
      | Automotive - industry                          |
      | Automotive research and development - industry |
      | Automotive supply chain - industry             |
      | Capital Investment - industry                  |
      | Chemicals - industry                           |
      | Creative content and production - industry     |
      | Creative industries - industry                 |
      | Data Analytics - industry                      |
      | Digital media - industry                       |
      | Electrical networks - industry                 |
      | Energy - industry                              |
      | Energy from waste - industry                   |
      | Financial services - industry                  |
      | Financial technology - industry                |
      | Food and drink - industry                      |
      | Free-from foods - industry                     |
      | Health and life sciences - industry            |
      | Meat, poultry and dairy - industry             |
      | Medical technology - industry                  |
      | Motorsport - industry                          |
      | Nuclear energy - industry                      |
      | Offshore wind energy - industry                |
      | Oil and gas - industry                         |
      | Pharmaceutical manufacturing - industry        |
      | Retail - industry                              |
      | Technology - industry                          |

    Examples: UK Setup Guides
      | selected                                                        |
      | Apply for a UK visa - guide                                     |
      | Establish a base for business in the UK - guide                 |
      | Hire skilled workers for your UK operations - guide             |
      | Open a UK business bank account - guide                         |
      | Set up a company in the UK - guide                              |
      | Understand the UK's tax, incentives and legal framework - guide |


    @wip
  @CMS-163
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
