@pixels
Feature: Pixels

  Background:
    Given basic authentication is done for "International - Landing" page

  @international
  Scenario Outline: Pixels should be present on "<selected>" page
    Given "Robert" visits the "International - <selected>" page

    Then "Robert" should be on the "International - <selected>" page
    And following web statistics analysis or tracking elements should be present
      | Google Tag Manager             |
      | Google Tag Manager - no script |
      | UTM Cookie Domain              |
    And following web statistics analysis or tracking elements should NOT be present
      | LinkedIn tracking pixel |
      | Facebook tracking pixel |

    Examples: Various pages
      | selected                     |
      | Landing                      |
      | Industries                   |
      | How to set up in the UK      |
      | Contact Us                   |

    @dev-only
    Examples: UK Setup Guides
      | selected                                                          |
      | UK visas and migration - UK setup guide                           |
      | Establish a UK business base - UK setup guide                     |
      | Hire skilled workers for your UK operations - UK setup guide      |
      | Open a UK business bank account - UK setup guide                  |
      | Register a company in the UK - UK setup guide                     |
      | UK tax and incentives - UK setup guide                            |
      | UK visas and migration - UK setup guide                           |
      | Research and development (R&D) support in the UK - UK setup guide |

    @stage-only
    Examples: UK Setup Guides
      | selected                                                          |
      | Open a UK business bank account - UK setup guide                  |
      | UK tax and incentives - UK setup guide                            |
      | Access finance in the UK - UK setup guide                         |

    @dev-only
    Examples: Industry pages
      | selected                                 |
      | Aerospace - industry                     |
      | Automotive - industry                    |
      | Creative industries - industry           |
      | Education - industry                     |
      | Engineering and manufacturing - industry |
      | Financial services - industry            |
      | Health and life sciences - industry      |
      | Legal services - industry                |
      | Space - industry                         |
      | Technology - industry                    |

    @stage-only
    Examples: Industry pages
      | selected                                       |
      | Creative industries - industry                 |
      | Engineering and manufacturing - industry       |
      | Financial and professional services - industry |
