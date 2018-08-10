@regional-pages
Feature: Regional pages

  @CMS-215
  Scenario Outline: Visitors should be able to see regional page for "<selected>"
    Given "Robert" visits the "Invest - <selected> - region" page

    When "Robert" unfolds all topic sections

    Then "Robert" should see following sections
      | Sections         |
      | Header           |
      | Beta bar         |
      | Hero             |
      | Topics           |
      | Topics contents  |
      | Report this page |
      | Footer           |
    And "Robert" should see content specific to "Invest - <selected> - region" page

    Examples: Industries
      | selected         |
      | London           |
      | North England    |
      | Northern Ireland |
      | Scotland         |
      | South of England |
      | The Midlands     |
      | Wales            |
