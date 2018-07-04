@invest-home-page
@no-sso-email-verification-required
Feature: Invest home page


  @browser
  @requests
  Scenario: Visitors should be able to view "Invest home" page
    Given "Robert" visits the "Invest - home" page

    Then "Robert" should see expected sections on "Invest - home" page
      | Header                             |
      | Beta bar                           |
      | Reasons to move business to the UK |
      | Sectors                            |
      | Setup Guides                       |
      | How we help                        |
      | Footer                             |


  @browser
  Scenario: Overseas businesses should be able to find out why UK is the best place for their business
    Given "Robert" visits the "Invest - home" page

    When "Robert" decides to read more on following topics
      | Bring your business to the UK     |
      | Access a highly skilled workforce |
      | Benefit from low business costs   |

    Then "Robert" should see brief explanation why the UK is the best place for his business


  @browser
  @requests
  Scenario Outline: Overseas businesses should be able to learn more about "<selected>" UK Industry
    Given "Robert" visits the "Invest - home" page

    When "Robert" decides to find out out more about "Invest - <selected> industry"

    Then "Robert" should be on the "Invest - Industry" page
    And "Robert" should see content specific to "Invest - <selected> industry" page

    Examples: promoted industries
      | selected                 |
      | Automotive               |
      | Capital Investment       |
      | Creative industries      |
      | Financial services       |
      | Health and life sciences |
      | Technology               |


  @browser
  @requests
  Scenario: Overseas businesses should be able to also learn more about UK Industries other than the promoted ones
    Given "Robert" visits the "Invest - home" page

    When "Robert" decides to see more UK industries

    Then "Robert" should be on the "Invest - Industries" page


  @browser
  @requests
  Scenario Outline: Overseas businesses should be able to learn how to grow their businesses in the UK by reading "<selected>" guide
    Given "Robert" visits the "Invest - home" page

    When "Robert" decides to read "Invest - <selected>" guide

    Then "Robert" should be on the "Invest - Guide" page
    And "Robert" should see content specific to "Invest - <selected> guide" page

    Examples: UK Setup Guides
      | selected                                    |
      | Apply for a UK visa                         |
      | Establish a base for business in the UK     |
      | Hire skilled workers for your UK operations |
      | Open a UK business bank account             |
      | Set up a company in the UK                  |


  @browser
  @requests
  Scenario: Overseas businesses should be able to learn how UK government can help them to establish in the UK
    Given "Robert" visits the "Invest - home" page

    Then "Robert" should see on "Invest - home" page how DIT can help foreign companies
      | Build connections   |
      | Apply for visas     |
      | Find grants         |
      | Get insights        |
      | Grow workforce      |

  @bug
  @CMS-255
  @fixme
  @browser
  @requests
  Scenario: Overseas businesses should be able to learn how UK government can help them to establish in the UK
    Given "Robert" visits the "Invest - home" page

    Then "Robert" should see on "Invest - home" page how DIT can help foreign companies
      | Contact us for help |
