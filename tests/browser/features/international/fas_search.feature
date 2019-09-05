@ED-3183
@ED-4259
@industry-pages
@no-sso-email-verification-required
Feature: Industry pages

  Background:
    Given basic authentication is done for "International - Landing" page


  @ED-4263
  @search
  Scenario Outline: Buyers should be able to find UK suppliers from the "<specific> Industry" page
    Given "Robert" visits the "International - <specific> - industry" page

    When "Robert" searches for companies using "<following>" keyword

    Then "Robert" should be on the "International - search results" page
    And "Robert" should see search results filtered by "<pre-selected>" industry

    Examples: Industries
      | specific          | following  | pre-selected                           |
      | Agritech          | plants     | Agriculture horticulture and fisheries |
      | Creative services | digital    | Creative and media                     |
      | Healthcare        | surgery    | Healthcare and medical                 |

    @full
    Examples: Industries
      | specific          | following  | pre-selected                           |
      | Cyber security    | WiFi       | Security                               |
      | Food and drink    | beer       | Food and drink                         |
      | Life sciences     | biotech    | Healthcare And Medical, Life sciences  |
      | Sports economy    | arenas     | Global sports infrastructure           |
      | Consumer & retail | salon      | Clothing Footwear And Fashion, Giftware Jewellery And Tableware, Household Goods Furniture And Furnishings, Retail and luxury, Textiles Interior Textiles And Carpets |

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

    @wip
    Examples: Industries which redirect to the new International site
      | specific       | following  | pre-selected                                                |
      | Aerospace      | satellites | Aerospace                                                   |
      | Legal services | lawyer     | Legal services                                              |
      | Technology     | holograms  | Electronics and IT hardware, Software and computer services |


  @ED-4264
  @search
  Scenario Outline: Buyers should be able to find more UK suppliers than visible on the "<specific> Industry" page
    Given "Robert" visits the "International - <specific> - industry" page

    When "Robert" decides to view more companies in the current industry

    Then "Robert" should be on the "International - search results" page
    And "Robert" should see search results filtered by "<pre-selected>" industry

    Examples: Promoted Industries
      | specific          | pre-selected                           |
      | Agritech          | Agriculture horticulture and fisheries |
      | Healthcare        | Healthcare and medical                 |

    @wip
    Examples: Industries with no companies in them on DEV or STAGE
      | specific       | pre-selected                                                |
      | Legal services | Legal services                                              |
      | Life sciences  | Life sciences                                               |
      | Cyber security | Security                                                    |
      | Food and drink | Food and drink                                              |
      | Sports economy | Global sports infrastructure                                |
      | Creative services | Creative and media                     |
      | Technology     | Electronics and IT hardware, Software and computer services |

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

    @wip
    Examples: Industries which redirect to the new International site
      | specific          | pre-selected                           |
      | Aerospace         | Aerospace                              |
