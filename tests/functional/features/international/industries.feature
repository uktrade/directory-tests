@international
Feature: Industry pages

  @ED-2013
  @internationalization
  @i18n
  @<selected>
  @no-sso-email-verification-required
  Scenario Outline: Visitors should be able to view specific pages on International site in "<selected>" language
    Given "Annette" is an anonymous visitor

    When "Annette" chooses to view following pages in "<selected>" language
      | page                                                     |
      | International - Industries                               |
      | International - Creative industries - Industry           |
      | International - Engineering and manufacturing - Industry |

    Then the "whole" part of the viewed pages should be presented in "<expected>" language with probability greater than "<lower limit>"
      | page                                                     |
      | International - Industries                               |
      | International - Creative industries - Industry           |
      | International - Engineering and manufacturing - Industry |

    Examples:
      | selected   | expected   | lower limit |
      | English    | English    | 0.98        |
      | French     | French     | 0.85        |
      | German     | German     | 0.98        |
      | Portuguese | Portuguese | 0.98        |
      | Spanish    | Spanish    | 0.98        |

    @wip
    Examples: Missing translations
      | selected   | expected   | lower limit |
      | Arabic     | Arabic     | 0.85        |

    # langdetect struggles to detect Chinese
    @wip
    Examples: Missing translations
      | selected   | expected   | lower limit |
      | Chinese    | Chinese    | 0.85        |

  @ED-2015
  @industries
  @no-sso-email-verification-required
  Scenario Outline: Buyers should be able to find out more about every promoted industry - visit "<selected>" page
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" goes to "<selected>" page

    Then "Annette Geissinger" should see "<selected>" page

    Examples:
      | selected                                                 |
      | International - Creative industries - Industry           |
      | International - Engineering and manufacturing - Industry |
      | International - Technology - Industry                    |
