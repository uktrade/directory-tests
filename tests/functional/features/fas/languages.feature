@fas
Feature: View FAS in various languages


  @ED-2004
  @internationalization
  @i18n
  @<selected>
  Scenario Outline: Buyers should be able to view specific FAS pages in "<selected>" language
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" chooses to view specific FAS page in "<selected>" language
      | page                            |
      | FAS Landing                     |
      | Industries                      |
      | Health Industry                 |
      | Tech Industry                   |
      | Creative Industry               |
      | Food-and-drink Industry         |
      | Health Industry Summary         |
      | Tech Industry Summary           |
      | Creative Industry Summary       |
      | Food-and-drink Industry Summary |

    Then the "main" part of the viewed FAS page should be presented in "<expected>" language with probability greater than "0.98"
      | page                            |
      | FAS Landing                     |
      | Industries                      |
      | Health Industry                 |
      | Tech Industry                   |
      | Creative Industry               |
      | Food-and-drink Industry         |
      | Health Industry Summary         |
      | Tech Industry Summary           |
      | Creative Industry Summary       |
      | Food-and-drink Industry Summary |

    Examples:
      | selected             | expected   |
      | English              | English    |
      | German               | German     |
      | Spanish              | Spanish    |
      | Portuguese           | Portuguese |
      | Portuguese-Brazilian | Portuguese |
      | Arabic               | Arabic     |
