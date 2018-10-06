@fas
Feature: View FAS in various languages


  @ED-2004
  @internationalization
  @i18n
  @<selected>
  @no-sso-email-verification-required
  Scenario Outline: Buyers should be able to view specific FAS pages in "<selected>" language
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" chooses to view specific FAS page in "<selected>" language
      | page                                |
      | FAS Landing                         |
      | FAS Industries                      |
      | FAS Health Industry                 |
      | FAS Tech Industry                   |
      | FAS Creative Industry               |
      | FAS Food and drink Industry         |
      | FAS Health Industry Summary         |
      | FAS Tech Industry Summary           |
      | FAS Creative Industry Summary       |
      | FAS Food and drink Industry Summary |

    Then the "main" part of the viewed FAS page should be presented in "<expected>" language with probability greater than "<lower limit>"
      | page                                |
      | FAS Landing                         |
      | FAS Industries                      |
      | FAS Health Industry                 |
      | FAS Tech Industry                   |
      | FAS Creative Industry               |
      | FAS Food and drink Industry         |
      | FAS Health Industry Summary         |
      | FAS Tech Industry Summary           |
      | FAS Creative Industry Summary       |
      | FAS Food and drink Industry Summary |

    Examples:
      | selected             | expected   | lower limit |
      | English              | English    | 0.98        |
      | Spanish              | Spanish    | 0.98        |
      | French               | French     | 0.98        |
      | Chinese              | Chinese    | 0.98        |
      | Portuguese           | Portuguese | 0.98        |
      | Portuguese-Brazilian | Portuguese | 0.98        |
      | German               | German     | 0.98        |
      | Arabic               | Arabic     | 0.85        |
