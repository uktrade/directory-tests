@international-page
Feature: International Page


  @ED-3114
  Scenario: Visitors should see "Buy from the UK, Invest in the UK, Study in the UK, Visit the UK" sections on the International page
    Given "Robert" visits the "International" page

    Then "Robert" should see "Buy from the UK, Invest in the UK, Study in the UK, Visit the UK" sections on "International" page


  @ED-3136
  @external-service
  @<expected_service>
  Scenario Outline: Visitors should be able to go to "<expected_service>" page from the International page
    Given "Robert" visits the "International" page

    When "Robert" goes to "<expected_service>" using "<section>" link on "International Page"

    Then "Robert" should be on the "<expected_service>" page

    Examples:
      | expected_service | section          |
      | Invest in Great  | Invest in the UK |
      | British Council  | Study in the UK  |
      | Visit Britain    | Visit the UK     |

    @bug
    @ED-3242
    @fixme
    Examples:
      | expected_service | section          |
      | Find a Supplier  | Buy from the UK  |

  @ED-3083
  @language-selector
  Scenario: Visitor should be able to open and close the language selector
    Given "Robert" visits the "International" page

    When "Robert" opens up the language selector
    Then "Robert" should see the language selector

    When "Robert" closes the language selector
    Then "Robert" should not see the language selector


  @ED-3083
  @language-selector
  @accessibility
  Scenario: Keyboard users should be able to open and close the language selector using just the keyboard
    Given "Robert" visits the "International" page

    When "Robert" opens up the language selector using his keyboard
    Then "Robert" should see the language selector

    When "Robert" closes the language selector using his keyboard
    Then "Robert" should not see the language selector


  @ED-3083
  @language-selector
  @accessibility
  Scenario: Language selector should trap the keyboard in order to help Keyboard users to navigate
    Given "Robert" visits the "International" page

    When "Robert" opens up the language selector using his keyboard
    And "Robert" uses his keyboard to navigate through all links visible on language selector

    Then "Robert"'s keyboard should be trapped to the language selector


  @ED-3149
  @language-selector
  Scenario Outline: Visitors should be able to view International page in "<preferred_language>"
    Given "Robert" visits the "International" page

    When "Robert" decides to view the page in "<preferred_language>"

    Then "Robert" should be on the "International" page
    And "Robert" should see the page in "<preferred_language>"

    Examples: available languages
      | preferred_language |
      | English            |
      | 简体中文            |
      | Deutsch            |
      | 日本語              |
      | Español            |
      | Português          |
      | العربيّة            |


  @ED-3149
  @language-selector
  Scenario: Visitors should be able to "get guidance and services to help them export" (visit ExRed) from International page
    Given "Robert" visits the "International" page

    When "Robert" decides to view the page in "English (UK)"

    Then "Robert" should be on the "Home" page


  @wip
  @ED-2846
  @geoip
  Scenario: Visitors accessing Export Readiness page from Abroad, should be presented with the International Page and if possible in language matching their geographical IP location
    Given "Robert" checks his geoip
    And "Robert" visits the "Home" page

    Then "Robert" should be on the "Home" page
