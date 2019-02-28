@home-page
Feature: Home Page

  Background:
    Given hawk cookie is set on "Export Readiness - Home" page

  @ED-2366
  @sections
  Scenario: Any Exporter should see the "Beta bar, Hero, EU Exit enquiries banner, Advice, Services, Case Studies, Business is Great, Error Reporting" sections on the home page
      Given "Robert" visits the "Export Readiness - Home" page
      Then "Robert" should see following sections
        | Sections                 |
        | Beta bar                 |
        | Hero                     |
        | EU Exit enquiries banner |
#        | News                     |
        | Advice                   |
        | Services                 |
        | Case Studies             |
        | Business is Great        |
        | Error Reporting          |


  @ED-3014
  @video
  Scenario: Any Exporter should be able to play promotional video on the Home page
    Given "Robert" visits the "Export Readiness - Home" page

    When "Robert" decides to watch "6" seconds of the promotional video

    Then "Robert" should be able to watch at least first "5" seconds of the promotional video


  @ED-3014
  @video
  Scenario: Any Exporter should be able to close the window with promotional video on the Home page
    Given "Robert" visits the "Export Readiness - Home" page

    When "Robert" decides to watch "6" seconds of the promotional video
    And "Robert" closes the window with promotional video

    Then "Robert" should not see the window with promotional video


  @ED-3083
  @language-selector
  Scenario: Visitor should be able to open and close the language selector on "Export Readiness - Home" page
    Given "Robert" visits the "Export Readiness - Home" page

    When "Robert" opens up the language selector
    Then "Robert" should see the language selector

    When "Robert" closes the language selector
    Then "Robert" should not see the language selector


  @ED-3083
  @language-selector
  @accessibility
  Scenario: Keyboard users should be able to open and close the language selector using just the keyboard on "Export Readiness - Home" page
    Given "Robert" visits the "Export Readiness - Home" page

    When "Robert" opens up the language selector using his keyboard
    Then "Robert" should see the language selector

    When "Robert" closes the language selector using his keyboard
    Then "Robert" should not see the language selector


  @ED-3083
  @language-selector
  @accessibility
  Scenario: Language selector should trap the keyboard in order to help Keyboard users to navigat on "Export Readiness - Home" pagee
    Given "Robert" visits the "Export Readiness - Home" page

    When "Robert" opens up the language selector using his keyboard
    And "Robert" uses his keyboard to navigate through all links visible on language selector

    Then "Robert"'s keyboard should be trapped to the language selector


  @ED-3083
  @language-selector
  Scenario Outline: Visitors should be able to view go to International page after changing language to "<preferred_language>" on the Domestic Home Page
    Given "Robert" visits the "Export Readiness - Home" page

    When "Robert" decides to view the page in "<preferred_language>"

    Then "Robert" should be on the "Export Readiness - International" page
    # ATM International page doesn't support translations
    # And "Robert" should see the page in "<preferred_language>"

    Examples: available languages
      | preferred_language |
      | English            |
      | 简体中文            |
      | Deutsch            |
      | 日本語              |
      | Español            |
      | Português          |
      | العربيّة            |
      | Français           |
