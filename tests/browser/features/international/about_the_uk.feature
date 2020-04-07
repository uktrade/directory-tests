@allure.suite:International
Feature: International - About the UK

  Background:
    Given test authentication is done


  Scenario: Visitors should be able to see all expected sections on "International - About the UK" page
    Given "Robert" visits the "International - About the UK" page

    Then "Robert" should see following sections
      | Sections               |
      | Header                 |
      | Hero                   |
      | Breadcrumbs            |
      | About the UK subheader |
      | Teaser                 |
      | Why choose the UK      |
      | UK industries          |
      | UK Regions             |
      | How we help            |
      | Speak to us            |
      | Error reporting        |
      | Footer                 |
