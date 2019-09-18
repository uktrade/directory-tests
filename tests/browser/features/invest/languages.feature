@wip
@internationalisation
Feature: Invest - Internationalisation


  Scenario Outline: Overseas businesses should be able to view "<selected>" page in multiple languages
    Given "Robert" visits the "<selected>" page

    When "Robert" chooses to view the page in selected languages
      | languages  |
      | English    |
      | German     |
      | Spanish    |
      | French     |
      | Portuguese |
      | Arabic     |
      | Japanesse  |
      | Chinese    |

    Then the "main" part of the page should be presented in expected languages with probability greater than the lower limit
      | expected   | lower limit |
      | English    | 0.98        |
      | German     | 0.98        |
      | Spanish    | 0.98        |
      | French     | 0.98        |
      | Portuguese | 0.98        |
      | Arabic     | 0.85        |
      | Japanese   | 0.98        |
      | Chinese    | 0.98        |

    Examples: Various pages
      | selected                |
      | Invest - landing           |
      | Invest - UK Setup Guide |
      | Invest - Contact Us     |
      | Invest - Feedback       |

    Examples: UK Setup Guides
      | selected                                                         |
      | Invest - Apply for a UK visa                                     |
      | Invest - Establish a base for business in the UK                 |
      | Invest - Hire skilled workers for your UK operations             |
      | Invest - Open a UK business bank account                         |
      | Invest - Set up a company in the UK                              |
      | Invest - Understand the UK's tax, incentives and legal framework |
