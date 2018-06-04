@ED-3183
@ED-4259
@industry-pages
@no-sso-email-verification-required
Feature: FAS Industry pages


  @ED-4260
  Scenario Outline: Buyers should be able to see all expected page elements on "<specific>" page
    Given "Robert" visits the "FAS <specific> Industry" page

    Then "Robert" should see expected sections on "FAS Industry" page
      | Hero                    |
      | Breadcrumbs             |
      | Contact us              |
      | Selling points          |
      | Search for UK suppliers |
      | Articles                |
#      | Case studies            |  # ATM these sections are not present
#      | Report this page        |

    Examples: promoted industries
      | specific          |
      | Aerospace         |
      | Agritech          |
      | Consumer retail   |
      | Creative services |
      | Cyber security    |
      | Food and drink    |
      | Healthcare        |
      | Sports economy    |
      | Technology        |

    @wip
    Examples: Industries with no companies in them on DEV
      | specific          |
      | Life sciences     |

    @wip
    # ATM these Industries are not present on Dev
    Examples: more industries
      | specific                           |
      | Automotive                         |
      | Business & Government Partnerships |
      | Education                          |
      | Energy                             |
      | Engineering                        |
      | Infrastructure                     |
      | Innovation                         |
      | Legal services                     |
      | Marine                             |
      | Professional & financial services  |
      | Space                              |


  @ED-4261
  @breadcrumbs
  Scenario Outline: Buyers should be able to go back to the "<expected>" page via "<selected>" breadcrumb on the "FAS <specific> Industry" page
    Given "Robert" visits the "FAS <specific> Industry" page

    When "Robert" decides to use "<selected>" breadcrumb on the "FAS Industry" page

    Then "Robert" should be on the "<expected>" page

    Examples: Promoted Industries
      | specific          | selected   | expected       |
      | Agritech          | Home       | FAS Landing    |
      | Creative services | Home       | FAS Landing    |
      | Cyber security    | Home       | FAS Landing    |
      | Food and drink    | Home       | FAS Landing    |
      | Sports economy    | Home       | FAS Landing    |
      | Healthcare        | Home       | FAS Landing    |
      | Life sciences     | Home       | FAS Landing    |
      | Technology        | Home       | FAS Landing    |
      | Agritech          | Industries | FAS Industries |
      | Creative services | Industries | FAS Industries |
      | Cyber security    | Industries | FAS Industries |
      | Food and drink    | Industries | FAS Industries |
      | Sports economy    | Industries | FAS Industries |
      | Healthcare        | Industries | FAS Industries |
      | Life sciences     | Industries | FAS Industries |
      | Technology        | Industries | FAS Industries |

    @wip
    # ATM these Industries are not present on Dev
    Examples: More Industries
      | specific                           | selected   | expected       |
      | Automotive                         | Home       | FAS Landing    |
      | Business & Government Partnerships | Home       | FAS Landing    |
      | Education                          | Home       | FAS Landing    |
      | Energy                             | Home       | FAS Landing    |
      | Engineering                        | Home       | FAS Landing    |
      | Infrastructure                     | Home       | FAS Landing    |
      | Innovation                         | Home       | FAS Landing    |
      | Legal services                     | Home       | FAS Landing    |
      | Marine                             | Home       | FAS Landing    |
      | Professional & financial services  | Home       | FAS Landing    |
      | Space                              | Home       | FAS Landing    |
      | Automotive                         | Industries | FAS Industries |
      | Business & Government Partnerships | Industries | FAS Industries |
      | Education                          | Industries | FAS Industries |
      | Energy                             | Industries | FAS Industries |
      | Engineering                        | Industries | FAS Industries |
      | Infrastructure                     | Industries | FAS Industries |
      | Innovation                         | Industries | FAS Industries |
      | Legal services                     | Industries | FAS Industries |
      | Marine                             | Industries | FAS Industries |
      | Professional & financial services  | Industries | FAS Industries |
      | Space                              | Industries | FAS Industries |


  @ED-4262
  @contact-us
  Scenario Outline: Buyers should be able to contact us (DIT) from the  "<specific> Industry" page
    Given "Robert" visits the "FAS <specific> Industry" page
    And "Robert" decided to "contact us" via "FAS <specific> Industry" page

    When "Robert" fills out and submits the contact us form

    Then "Robert" should be on the "FAS Thank you for your message" page

    Examples: Promoted industries
      | specific          |
      | Agritech          |
      | Creative services |

    @bug
    @TT-82
    @fixme
    Examples: Promoted industries
      | specific          |
      | Cyber security    |
      | Food and drink    |
      | Sports economy    |
      | Healthcare        |
      | Life sciences     |
      | Technology        |

    @wip
    # ATM these Industries are not present on Dev
    Examples: More Industries
      | specific                           |
      | Automotive                         |
      | Business & Government Partnerships |
      | Education                          |
      | Energy                             |
      | Engineering                        |
      | Infrastructure                     |
      | Innovation                         |
      | Legal services                     |
      | Marine                             |
      | Professional & financial services  |
      | Space                              |


  @ED-4263
  @search
  Scenario Outline: Buyers should be able to find UK suppliers from the "<specific> Industry" page
    Given "Robert" visits the "FAS <specific> Industry" page

    When "Robert" searches for companies using "<following>" keyword

    Then "Robert" should be on the "FAS search results" page
    And "Robert" should see search results filtered by "<pre-selected>" industry

    Examples: Promoted Industries
      | specific          | following  | pre-selected                           |
      | Aerospace         | satellites | Aerospace                              |
      | Agritech          | plants     | Agriculture horticulture and fisheries |
      | Consumer retail   | salon      | Retail and luxury                      |
      | Creative services | digital    | Creative and media                     |
      | Cyber security    | WiFi       | Security                               |
      | Food and drink    | beer       | Food and drink                         |
      | Sports economy    | arenas     | Global sports infrastructure           |
      | Healthcare        | surgery    | Healthcare and medical                 |
      | Technology        | holograms  | Software and computer services         |
      | Legal services    | lawyer     | Legal services                         |

    @wip
    Examples: Industries with no companies in them on DEV
      | specific          | following  | pre-selected  |
      | Life sciences     | biotech    | Life sciences |

    @wip
    # ATM these Industries are not present on Dev
    Examples: More Industries
      | specific                           | following   |
      | Automotive                         | vehicles    |
      | Business & Government Partnerships | procurement |
      | Education                          | literacy    |
      | Energy                             | solar power |
      | Engineering                        | marquees    |
      | Infrastructure                     | mineral     |
      | Innovation                         | robotics    |
      | Legal services                     | criminal    |
      | Marine                             | ships       |
      | Professional & financial services  | insight     |
      | Space                              | satellite   |


  @ED-4264
  @search
  Scenario Outline: Buyers should be able to find more UK suppliers than visible on the "<specific> Industry" page
    Given "Robert" visits the "FAS <specific> Industry" page

    When "Robert" decides to view more companies in the current industry

    Then "Robert" should be on the "FAS search results" page
    And "Robert" should see search results filtered by "<pre-selected>" industry

    Examples: Promoted Industries
      | specific          | pre-selected                           |
      | Aerospace         | Aerospace                              |
      | Agritech          | Agriculture horticulture and fisheries |
      | Consumer retail   | Retail and luxury                      |
      | Creative services | Creative and media                     |
      | Cyber security    | Security                               |
      | Food and drink    | Food and drink                         |
      | Sports economy    | Global sports infrastructure           |
      | Healthcare        | Healthcare and medical                 |
      | Technology        | Software and computer services         |
      | Legal services    | Legal services                         |

    @wip
    Examples: Industries with no companies in them on DEV
      | specific          | pre-selected  |
      | Life sciences     | Life sciences |

    @wip
    # ATM these Industries are not present on Dev
    Examples: More Industries
      | specific                           |
      | Automotive                         |
      | Business & Government Partnerships |
      | Education                          |
      | Energy                             |
      | Engineering                        |
      | Infrastructure                     |
      | Innovation                         |
      | Legal services                     |
      | Marine                             |
      | Professional & financial services  |
      | Space                              |


  @ED-4265
  @company-profiles
  Scenario Outline: Buyers should be able to view "<selected>" company profile from the "<specific>" Industry page
    Given "Robert" visits the "FAS <specific> Industry" page

    When "Robert" decides to view "<selected>" company profile

    Then "Robert" should be on the "FAS company profile" page

    Examples:
      | specific          | selected |
      | Aerospace         | first    |
      | Agritech          | second   |
      | Consumer retail   | third    |
      | Creative services | second   |
      | Cyber security    | third    |
      | Food and drink    | fourth   |
      | Sports economy    | fifth    |
      | Healthcare        | sixth    |
      | Technology        | third    |

    @wip
    Examples: Industries with no companies in them on DEV
      | specific          | selected |
      | Life sciences     | first    |

    @wip
    # ATM these Industries are not present on Dev
    Examples: More Industries
      | specific                           | selected |
      | Automotive                         | first    |
      | Business & Government Partnerships | second   |
      | Education                          | third    |
      | Energy                             | fourth   |
      | Engineering                        | fifth    |
      | Infrastructure                     | sixth    |
      | Innovation                         | second   |
      | Legal services                     | third    |
      | Marine                             | first    |
      | Professional & financial services  | second   |
      | Space                              | third    |


  @ED-4266
  @marketing-content
  Scenario Outline: Buyers should be able to view "<selected>" article from the "<specific> Industry" page
    Given "Robert" visits the "FAS <specific> Industry" page

    When "Robert" decides to read "<selected>" marketing article

    Then "Robert" should be on the "<expected>" page

    Examples: Promoted Industries
      | specific          | selected | expected       |
      | Agritech          | first    | FAS article    |
      | Consumer retail   | first    | FAS article    |
      | Creative services | first    | FAS article    |
      | Creative services | second   | FAS Contact us |
      | Cyber security    | first    | FAS article    |
      | Food and drink    | first    | FAS Contact us |
      | Sports economy    | first    | FAS Contact us |
      | Sports economy    | second   | FAS Contact us |
      | Healthcare        | first    | FAS article    |
      | Healthcare        | second   | FAS article    |
      | Life sciences     | first    | FAS article    |
      | Technology        | first    | FAS article    |

    @wip
    Examples: Industries without articles
      | specific          | selected | expected       |
      | Aerospace         | first    | non FAS        |

    @wip
    # ATM these Industries are not present on Dev
    Examples: More Industries
      | specific                           |
      | Automotive                         |
      | Business & Government Partnerships |
      | Education                          |
      | Energy                             |
      | Engineering                        |
      | Infrastructure                     |
      | Innovation                         |
      | Legal services                     |
      | Marine                             |
      | Professional & financial services  |
      | Space                              |


  @ED-4267
  @legal-services
  @marketing-content
  # link to Legal Services industry page should take users to an external
  # Legal Services website (not hosted on great.gov.uk)
  Scenario: Buyers should be able to learn more from the Legal Services page
    Given "Annette Geissinger" visits the "FAS Legal Services Industry" page

    When "Annette Geissinger" decides to read "first" marketing article

    Then "Annette Geissinger" should be on the "Legal Services landing" page


  @wip
  @report-this-page
  Scenario Outline: Buyers should be able to report a problem with the "FAS Industries" page from the  "<specific> Industry" page
    Given "Robert" visits the "FAS <specific> Industry" page

    When "Robert" decides to report a problem with the page
    And "Robert" fills out and submits the Help us improve great.gov.uk form

    Then "Robert" should be on the "Thank you for your feedback" page

    Examples:
      | specific          |
      | Agritech          |
      | Creative services |
      | Cyber security    |
      | Food and drink    |
      | Sports economy    |
      | Healthcare        |
      | Legal services    |
      | Life sciences     |
      | Technology        |

    @wip
    # ATM these Industries are not present on Dev
    Examples: More Industries
      | specific                           |
      | Automotive                         |
      | Business & Government Partnerships |
      | Education                          |
      | Energy                             |
      | Engineering                        |
      | Infrastructure                     |
      | Innovation                         |
      | Legal services                     |
      | Marine                             |
      | Professional & financial services  |
      | Space                              |
