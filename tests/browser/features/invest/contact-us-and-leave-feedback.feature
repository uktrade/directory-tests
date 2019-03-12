@contact-us
Feature: Contact us and Leave feedback

  Background:
    Given basic authentication is done for "Invest - Home" page
    And basic authentication is done for "Export Readiness - Home" page

  @CMS-163
  @beta
  @feedback
  @header
  @footer
  Scenario Outline: Visitors should be able to access feedback form from "<selected>" page
    Given "Robert" visits the "Invest - <selected>" page

    When "Robert" decides to use "Feedback" link on "Invest - <selected>" page

    Then "Robert" should be on the "Export Readiness - Feedback" page

    Examples: Various pages
      | selected       |
      | Home           |
      | Industries     |
      | UK Setup Guide |

    Examples: Industry pages
      | selected                                       |
      | Advanced manufacturing - industry              |
      | Aerospace - industry                           |

    @full
    Examples: Industry pages
      | selected                                       |
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
      | Energy from waste market - industry            |
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
      | selected                                       |
      | Apply for a UK visa - guide                    |
      | Establish a base for business in the UK - guide|

    @full
    Examples: UK Setup Guides
      | selected                                            |
      | Hire skilled workers for your UK operations - guide |
      | Open a UK business bank account - guide             |
      | Register a company in the UK - guide                |
      | Understand UK tax and incentives - guide            |


  @CMS-163
  @dev-only
  @captcha
  @contact-us
  @header
  @footer
  Scenario Outline: Visitors should be able to contact us from "<selected>" page
    Given "Robert" visits the "Invest - <selected>" page
    And "Robert" decided to use "Contact us" link
    And "Robert" is on the "Invest - Contact us" page

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Invest - Thank you for your message" page

    Examples: Various pages
      | selected                          |
      | Home                              |

    @full
    Examples: Various pages
      | selected                          |
      | Industries                        |
      | UK Setup Guide                    |
      | Advanced manufacturing - industry |
      | Apply for a UK visa - guide       |


  @CMS-237
  @contact-us
  @dev-only
  @captcha
  @header
  @footer
  Scenario Outline: An email should be sent after visitor submits the contact-us form
    Given "Robert" visits the "Invest - <selected>" page
    And "Robert" decided to use "Contact us" link
    And "Robert" is on the "Invest - Contact us" page

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Invest - Thank you for your message" page
    And "Robert" should receive a contact confirmation email from "no-reply@mailgun.directory.uktrade.io"
    And Invest mailbox admin should also receive a contact confirmation email from "no-reply@mailgun.directory.uktrade.io"

    Examples: Various pages
      | selected                          |
      | Home                              |
