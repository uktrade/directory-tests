@ED-3183
@ED-4259
@industry-pages
@no-sso-email-verification-required
Feature: Find a Supplier - Industry pages


  @ED-4260
  Scenario Outline: Buyers should be able to see all expected page elements on "<specific>" page
    Given "Robert" visits the "Find a Supplier - <specific> - industry" page

    Then "Robert" should see following sections
      | Sections                |
      | Hero                    |
      | Breadcrumbs             |
      | Contact us              |
      | Selling points          |
      | Search for UK suppliers |
      | Articles                |

    Examples: promoted industries
      | specific          |
      | Aerospace         |
      | Agritech          |
      | Consumer retail   |
      | Creative services |

    @full
    Examples: promoted industries
      | specific          |
      | Cyber security    |
      | Food and drink    |
      | Healthcare        |
      | Sports economy    |
      | Technology        |

    @wip
    Examples: Industries with no companies in them on DEV
      | specific          |
      | Life sciences     |
      | Legal services    |

    @wip
    Examples: Industries not present on Dev
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


  @bug
  @TT-433
  @fixed
  @ED-4261
  @breadcrumbs
  Scenario Outline: Buyers should be able to go back to the "<specific>" page via "<selected>" breadcrumb on the "Find a Supplier - <specific> Industry" page
    Given "Robert" visits the "Find a Supplier - <specific> - industry" page

    When "Robert" decides to use "<selected>" breadcrumb on the "Find a Supplier - <specific> - industry" page

    Then "Robert" should be on the "Find a Supplier - <selected>" page

    Examples: Promoted Industries
      | specific          | selected   |
      | Agritech          | Home       |
      | Creative services | Home       |
      | Cyber security    | Home       |
      | Food and drink    | Home       |
      | Sports economy    | Industries |
      | Healthcare        | Industries |
      | Life sciences     | Industries |
      | Technology        | Industries |

    @full
    Examples: Promoted Industries
      | specific          | selected   |
      | Sports economy    | Home       |
      | Healthcare        | Home       |
      | Life sciences     | Home       |
      | Technology        | Home       |
      | Agritech          | Industries |
      | Creative services | Industries |
      | Cyber security    | Industries |
      | Food and drink    | Industries |

    @wip
    Examples: Industries not present on Dev
      | specific                           | selected   |
      | Automotive                         | Home       |
      | Business & Government Partnerships | Home       |
      | Education                          | Home       |
      | Energy                             | Home       |
      | Engineering                        | Home       |
      | Infrastructure                     | Home       |
      | Innovation                         | Home       |
      | Legal services                     | Home       |
      | Marine                             | Home       |
      | Professional & financial services  | Home       |
      | Space                              | Home       |
      | Automotive                         | Industries |
      | Business & Government Partnerships | Industries |
      | Education                          | Industries |
      | Energy                             | Industries |
      | Engineering                        | Industries |
      | Infrastructure                     | Industries |
      | Innovation                         | Industries |
      | Legal services                     | Industries |
      | Marine                             | Industries |
      | Professional & financial services  | Industries |
      | Space                              | Industries |


  @ED-4262
  @contact-us
  Scenario Outline: Buyers should be able to contact us (DIT) from the  "<specific> Industry" page
    Given "Robert" visits the "Find a Supplier - <specific> - industry" page
    And "Robert" decided to use "contact us" button

    When "Robert" fills out and submits the contact us form

    Then "Robert" should be on the "Find a Supplier - Thank you for your message" page

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
    Examples: Industries not present on Dev
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

  @bug
  @TT-277
  @fixed
  @full
  @contact-us
  Scenario: Buyers shouldn't be able to submit the contact us form without passing captcha
    Given "Robert" visits the "Find a Supplier - Contact Us" page

    When "Robert" fills out and submits the contact us form without passing captcha

    Then "Robert" should be on the "Find a Supplier - Contact us" page


  @ED-4263
  @search
  Scenario Outline: Buyers should be able to find UK suppliers from the "<specific> Industry" page
    Given "Robert" visits the "Find a Supplier - <specific> - industry" page

    When "Robert" searches for companies using "<following>" keyword

    Then "Robert" should be on the "Find a Supplier - search results" page
    And "Robert" should see search results filtered by "<pre-selected>" industry

    Examples: Industries
      | specific          | following  | pre-selected                           |
      | Aerospace         | satellites | Aerospace                              |
      | Agritech          | plants     | Agriculture horticulture and fisheries |
      | Consumer retail   | salon      | Retail and luxury                      |
      | Creative services | digital    | Creative and media                     |

    @full
    Examples: Industries
      | specific          | following  | pre-selected                           |
      | Cyber security    | WiFi       | Security                               |
      | Food and drink    | beer       | Food and drink                         |
      | Sports economy    | arenas     | Global sports infrastructure           |
      | Healthcare        | surgery    | Healthcare and medical                 |
      | Technology        | holograms  | Software and computer services         |

    @wip
    Examples: Industries with no companies in them on DEV
      | specific          | following  | pre-selected   |
      | Legal services    | lawyer     | Legal services |
      | Life sciences     | biotech    | Life sciences  |

    @wip
    Examples: Industries not present on Dev
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
    Given "Robert" visits the "Find a Supplier - <specific> - industry" page

    When "Robert" decides to view more companies in the current industry

    Then "Robert" should be on the "Find a Supplier - search results" page
    And "Robert" should see search results filtered by "<pre-selected>" industry

    Examples: Promoted Industries
      | specific          | pre-selected                           |
      | Aerospace         | Aerospace                              |
      | Agritech          | Agriculture horticulture and fisheries |
      | Consumer retail   | Retail and luxury                      |
      | Creative services | Creative and media                     |

    @full
    Examples: Promoted Industries
      | specific          | pre-selected                           |
      | Cyber security    | Security                               |
      | Food and drink    | Food and drink                         |
      | Sports economy    | Global sports infrastructure           |
      | Healthcare        | Healthcare and medical                 |
      | Technology        | Software and computer services         |

    @wip
    Examples: Industries with no companies in them on DEV
      | specific          | pre-selected  |
      | Legal services    | Legal services|
      | Life sciences     | Life sciences |

    @wip
    Examples: Industries not present on Dev
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
    Given "Robert" visits the "Find a Supplier - <specific> - industry" page

    When "Robert" decides to view "<selected>" company profile

    Then "Robert" should be on the "Find a Supplier - company profile" page

    Examples:
      | specific          | selected |
      | Aerospace         | first    |
      | Agritech          | second   |
      | Consumer retail   | third    |
      | Creative services | second   |

    @full
    Examples:
      | specific          | selected |
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
    Examples: Industries not present on Dev
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
    Given "Robert" visits the "Find a Supplier - <specific> - industry" page

    When "Robert" decides to read "<selected>" marketing article

    Then "Robert" should be on the "<expected>" page

    Examples: Industries
      | specific          | selected | expected                     |
      | Agritech          | first    | Find a Supplier - Article    |
      | Consumer retail   | first    | Find a Supplier - Article    |
      | Creative services | first    | Find a Supplier - Article    |
      | Creative services | second   | Find a Supplier - Contact us |
      | Cyber security    | first    | Find a Supplier - Article    |

    @full
    Examples: Industries
      | specific          | selected | expected                     |
      | Food and drink    | first    | Find a Supplier - Contact us |
      | Sports economy    | first    | Find a Supplier - Contact us |
      | Sports economy    | second   | Find a Supplier - Contact us |
      | Healthcare        | first    | Find a Supplier - Article    |
      | Healthcare        | second   | Find a Supplier - Article    |
      | Life sciences     | first    | Find a Supplier - Article    |
      | Technology        | first    | Find a Supplier - Article    |

    @wip
    Examples: Industries without articles
      | specific          | selected | expected                     |
      | Aerospace         | first    | non Find a Supplier -        |

    @wip
    Examples: Industries not present on Dev
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
    Given "Annette Geissinger" visits the "Find a Supplier - Legal Services - industry" page

    When "Annette Geissinger" decides to read "first" marketing article

    Then "Annette Geissinger" should be on the "Legal Services - Home" page


  @wip
  @report-this-page
  Scenario Outline: Buyers should be able to report a problem with the "Find a Supplier - Industries" page from the  "<specific> Industry" page
    Given "Robert" visits the "Find a Supplier - <specific> - industry" page

    When "Robert" decides to report a problem with the page
    And "Robert" fills out and submits the Help us improve great.gov.uk form

    Then "Robert" should be on the "Find a Supplier - Thank you for your feedback" page

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
