@home-page
@no-sso-email-verification-required
Feature: Invest home page

  Background:
    Given basic authentication is done for "International - Landing" page

  @dev-only
  @CMS-157
  Scenario: Visitors should be able to view "Invest home" page
    Given "Robert" visits the "Invest - home" page

    Then "Robert" should see following sections
      | Sections                     |
      | Header                       |
      | Breadcrumbs                  |
      | EU exit news banner          |
      | Benefits                     |
      | UK setup guides              |
      | Sectors                      |
      | High-Potential Opportunities |
      | How we help                  |
      | Contact us                   |
      | Error reporting              |
      | Footer                       |

  @stage-only
  @CMS-157
  Scenario: Visitors should be able to view "Invest home" page
    Given "Robert" visits the "Invest - home" page

    Then "Robert" should see following sections
      | Sections                     |
      | Header                       |
      | Breadcrumbs                  |
      | UK setup guides              |
      | Sectors                      |
      | High-Potential Opportunities |
      | How we help                  |
      | Contact us                   |
      | Error reporting              |
      | Footer                       |


  @dev-only
  @CMS-157
  Scenario Outline: Overseas businesses should be able to learn more about "<selected>" UK Industry
    Given basic authentication is done for "International - Landing" page
    And "Robert" visits the "Invest - home" page

    When "Robert" decides to find out out more about "Invest - <selected> - industry"

    Then "Robert" should be on the "<service> - <selected> - industry" page

    Examples: promoted industries available via International site
      | selected                 | service       |
      | Automotive               | International |
      | Health and life sciences | International |
      | Technology               | International |


  @stage-only
  @CMS-157
  Scenario Outline: Overseas businesses should be able to learn more about "<selected>" UK Industry
    Given "Robert" visits the "Invest - home" page

    When "Robert" decides to find out out more about "Invest - <selected> - industry"

    Then "Robert" should be on the "<service> - <selected> - industry" page

    Examples: promoted industries
      | selected                 | service |
      | Automotive               | Invest  |
      | Health and life sciences | Invest  |
      | Technology               | Invest  |


  @CMS-157
  Scenario: Overseas businesses should be able to also learn more about UK Industries other than the promoted ones
    Given "Robert" visits the "Invest - home" page

    When "Robert" decides to "see more industries"

    Then "Robert" should be on the "Invest - Industries" page


  @CMS-157
  Scenario: Overseas businesses should be able to learn how to set up in the UK
    Given "Robert" visits the "Invest - home" page

    When "Robert" decides to "Get started in the UK"

    Then "Robert" should be on the "International - How to set up in the UK" page


  @ISD
  Scenario: Overseas businesses should be able to learn how to find a UK specialist
    Given basic authentication is done for "Domestic - Home" page
    Given "Robert" visits the "Invest - home" page

    When "Robert" decides to "Get help to set up or expand in the UK"

    Then "Robert" should be on the "ISD - Landing" page


  @HPO
  Scenario Outline: Overseas businesses should be able to learn about "<selected>" High-Potential Opportunities
    Given "Robert" visits the "Invest - home" page

    When "Robert" decides to find out more about "<selected>"

    Then "Robert" should be on the "Invest - <selected> - hpo" page
    And "Robert" should see content specific to "Invest - <selected> - hpo" page

    Examples: UK Setup Guides
      | selected                          |
      | Advanced food production |
      | Lightweight structures            |
      | Rail infrastructure               |
