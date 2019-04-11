@international
Feature: View International site in various languages


  @internationalization
  @i18n
  @<selected>
  @no-sso-email-verification-required
  Scenario Outline: Visitors should be able to view specific pages on International site in "<selected>" language
    Given "Annette" is an anonymous visitor

    When "Annette" chooses to view following pages in "<selected>" language
      | page                    |
      | International - Landing |

    Then the "main" part of the viewed pages should be presented in "<expected>" language with probability greater than "<lower limit>"
      | page                    |
      | International - Landing |

    Examples:
      | selected   | expected   | lower limit |
      | English    | English    | 0.98        |
      | French     | French     | 0.98        |
      | German     | German     | 0.98        |
      | Portuguese | Portuguese | 0.98        |
      | Spanish    | Spanish    | 0.98        |
      | Arabic     | Arabic     | 0.85        |
      | Chinese    | Chinese    | 0.85        |