@header-footer
Feature: Invest - Header-Footer

  Background:
    Given basic authentication is done for "International - Landing" page

  @CMS-158
  @logo
  @header
  @footer
  Scenario Outline: Visitors should see correct logos in the page header and footer on "<selected>" page
    Given "Robert" visits the "Invest - <selected>" page

    Then "Robert" should be on the "Invest - <selected>" page
    And "Robert" should see correct "Invest in Great - header" logo
    And "Robert" should see correct "Great - footer" logo
    And "Robert" should see the correct favicon

    Examples:
      | selected                         |
      | Landing                          |
      | Contact Us                       |
      | How to set up in the UK          |
      | Access finance in the UK - guide |

    @full
    @dev-only
    Examples: UK setup guides
      | selected                                          |
      | DIT's guide to UK Capital Gains Tax - guide       |
      | DIT's guide to UK Corporation Tax - guide         |
      | DIT's Guide to UK Venture Capital Schemes - guide |
      | Establish a UK business base - guide              |
      | Register a company in the UK - guide              |
      | UK infrastructure - guide                         |
      | UK innovation - guide                             |
      | UK talent and labour - guide                      |


  @stage-only
  @CMS-158
  @logo
  @header
  @footer
  Scenario Outline: Visitors should see correct logos in the page header and footer on "<selected>" page
    Given "Robert" visits the "Invest - <selected> - HPO" page

    Then "Robert" should be on the "Invest - <selected> - HPO" page
    And "Robert" should see correct "Great - header" logo
    And "Robert" should see correct "Great - footer" logo
    And "Robert" should see the correct favicon

    Examples:
      | selected                          |
      | High productivity food production |
      | Lightweight structures            |
      | Rail infrastructure               |


  @CMS-158
  @header
  @footer
  @landing-page
  @<specific>
  Scenario Outline: Visitors should be able to find out more about "<specific topic>" and get to "<expected>" page
    Given "Robert" visits the "Invest - landing" page

    When "Robert" decides to find out more about "<specific topic>"

    Then "Robert" should be on the "<expected>" page

    Examples:
      | specific topic          | expected                         |
      | Overview                | Invest - landing                 |
      | How to expand to the UK | Invest - How to set up in the UK |
      | Find a UK specialist    | ISD - Landing                    |
      | How we help             | Invest - How we help you expand  |
      | Contact us              | Invest - Contact us              |


  @CMS-158
  @logo
  @header
  @footer
  Scenario Outline: Visitors should be able to get to the Invest landing page from "<selected>" page by using UK Government logo in the page header
    Given "Robert" visits the "Invest - <selected>" page

    When "Robert" decides to click on "Invest in Great logo"

    Then "Robert" should be on the "International - Landing" page

    Examples:
      | selected                |
      | Landing                 |
      | How to set up in the UK |
      | Contact Us              |

    @dev-only
    Examples: UK setup guides
      | selected                                          |
      | Access finance in the UK - guide                  |
      | DIT's guide to UK Capital Gains Tax - guide       |
      | DIT's guide to UK Corporation Tax - guide         |
      | DIT's Guide to UK Venture Capital Schemes - guide |
      | Establish a UK business base - guide              |
      | Register a company in the UK - guide              |
      | UK infrastructure - guide                         |
      | UK innovation - guide                             |
      | UK talent and labour - guide                      |

    @stage-only
    Examples: Legacy UK setup guides
      | selected                                         |
      | Access finance in the UK (Staging) - guide       |
      | Open a UK business bank account (Staging) - guide|
      | UK tax and incentives (Staging) - guide          |

    @uat-only
    Examples: UK setup guides
      | selected                                                 |
      | Access finance in the UK - guide                         |
      | Brexit webinars for EU businesses - guide                |
      | Establish a UK business base - guide                     |
      | Get support to move your tech business to the UK - guide |
      | Hire skilled workers for your UK operations - guide      |
      | Open a UK business bank account - guide                  |
      | Register a company in the UK - guide                     |
      | UK tax and incentives - guide                            |
      | UK visas and migration - guide                           |
