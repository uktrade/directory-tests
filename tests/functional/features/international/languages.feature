@international
Feature: International - View pages in various languages


  @ED-2013
  @internationalization
  @i18n
  @<selected>
  @no-sso-email-verification-required
  Scenario Outline: Visitors should be able to view International landing page in "<selected>" language
    Given "Annette" is an anonymous visitor

    When "Annette" chooses to view following pages in "<selected>" language
      | page                    |
      | International - Landing |

    Then the HTML document language for viewed pages should be set to "<selected>" language
    And the language switcher on viewed pages should show "<selected>" as selected language
    And the "main" part of the viewed pages should be presented in "<selected>" language with probability greater than "<lower limit>"

    Examples:
      | selected   | lower limit |
      | English    | 0.98        |
      | French     | 0.98        |
      | German     | 0.98        |
      | Portuguese | 0.98        |
      | Spanish    | 0.98        |
      | Chinese    | 0.98        |

    @wip
    Examples: Missing translations
      | selected   | lower limit |
      | Arabic     | 0.85        |


  @ED-2013
  @internationalization
  @i18n
  @<selected>
  @no-sso-email-verification-required
  Scenario Outline: Visitors should be able to view Industry pages in "<selected>" language
    Given "Annette" is an anonymous visitor

    When "Annette" chooses to view following pages in "<selected>" language
      | page                                                     |
      | International - Industries                               |
      | International - Creative industries - Industry           |
      | International - Engineering and manufacturing - Industry |

    Then the HTML document language for viewed pages should be set to "<selected>" language
    And the language switcher on viewed pages should show "<selected>" as selected language
    And the "main" part of the viewed pages should be presented in "<selected>" language with probability greater than "<lower limit>"

    Examples:
      | selected   | lower limit |
      | English    | 0.98        |
      | French     | 0.85        |
      | German     | 0.85        |
      | Portuguese | 0.98        |
      | Spanish    | 0.85        |

    @wip
    Examples: Missing translations
      | selected   | lower limit |
      | Arabic     | 0.85        |


  # langdetect library can't detect Chinese on Industries pages, thus that assertion is omitted from this scenario
  @ED-2013
  @internationalization
  @i18n
  @<selected>
  @no-sso-email-verification-required
  Scenario Outline: Visitors should be able to view Industry page in "<selected>"
    Given "Annette" is an anonymous visitor

    When "Annette" chooses to view following pages in "<selected>" language
      | page                                                     |
      | International - Industries                               |
      | International - Creative industries - Industry           |
      | International - Engineering and manufacturing - Industry |

    Then the HTML document language for viewed pages should be set to "<selected>" language
    And the language switcher on viewed pages should show "<selected>" as selected language

    Examples: Missing translations
      | selected   |
      | Chinese    |
