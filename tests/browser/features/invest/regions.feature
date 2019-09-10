@dev-only
@regional-pages
Feature: Invest - Regional pages

  Background:
    Given basic authentication is done for "International - Landing" page

  @CMS-215
  Scenario Outline: Visitors should be able to see regional page for "<selected>"
    Given "Robert" visits the "Invest - <selected> - region" page

#    When "Robert" unfolds all topic sections

    Then "Robert" should see following sections
      | Sections         |
      | Header           |
      | Hero             |
#      | Topics           |
#      | Topics contents  |
      | Error reporting  |
      | Footer           |
    And "Robert" should see content specific to "Invest - <selected> - region" page

    Examples: Industries
      | selected         |
      | North England    |
      | Northern Ireland |
      | Scotland         |
      | South England    |
      | Midlands         |
      | Wales            |
