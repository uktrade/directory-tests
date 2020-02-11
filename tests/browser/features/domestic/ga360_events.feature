@wip
@ga360
@allure.suite:Domestic
Feature: Domestic - Google Analytics 360 Events

  Background:
    Given basic authentication is done for "Domestic - Home" page


  @skip
  @allure.link:CMS-1672
  @header-events
  Scenario Outline: All GA360 events should registered for event handlers attached to "Domestic Header" elements on "Domestic - <specific>" page
    Given "Robert" visits the "Domestic - <specific>" page

    When "Robert" triggers all GTM events defined for "Domestic header"

    Then following GTM events should be registered
      | action     | element          | event   | type        | value        |
      | SignIn     | HeaderSignInLink | gaEvent | Account     | Not present  |
      | Search     | HeaderSearchBar  | gaEvent | General     | Empty string |
      | Navigation | HeaderMenuLink   | gaEvent | Not present | Advice       |
      | Navigation | HeaderMenuLink   | gaEvent | Not present | Markets      |
      | Navigation | HeaderMenuLink   | gaEvent | Not present | Services     |

    Examples:
      | specific                             |
      | Home                                 |
      | Advice landing                       |
      | Markets                              |
      | Services                             |
      | Search results                       |
      | Domestic EU Exit contact form        |
      | Create an export plan - article list |
      | Get export finance - article list    |
      | Join our export community - landing  |
      | Join our Export Community - form     |

    @bug
    @allure.issue:CMS-1683
    @fixme
    Examples: Pages without Domestic Header tagging
      | specific                             |
      | Feedback                             |
      | Get finance                          |
      | Trade finance                        |

    @bug
    @allure.issue:CMS-1683
    @fixme
    @dev-only
    Examples: Pages without Domestic Header tagging
      | specific                             |
      | Report a trade barrier               |


  @bug
  @allure.issue:CMS-1684
  @fixme
  @allure.link:CMS-1672
  @page-events
  Scenario Outline: All GA360 "LandingPage" events should registered for event handlers attached to "Domestic Pages" elements on "Domestic - <specific>" page
    Given "Robert" visits the "Domestic - <specific>" page

    When "Robert" triggers all GTM "LandingPage" events defined for "Domestic pages"

    Then following GTM events should be registered
      | action      | element             | event   | type          | value       |
      | ContentLink | EuExitBanner        | gaEvent | EuExit        | Not present |
      | ContentLink | HeroBannerVideoLink | gaEvent | Video         | Not present |
      | Cta         | Link                | gaEvent | Advice        | Not present |
      | Cta         | Link                | gaEvent | ExporterStory | Not present |
      | Cta         | Link                | gaEvent | Service       | Not present |

    Examples:
      | specific                             |
      | Home                                 |
      | Advice landing                       |
      | Markets                              |
      | Services                             |
      | Feedback                             |
      | Search results                       |
      | Domestic EU Exit contact form        |
      | Get export finance - article list    |


  @allure.link:CMS-1672
  @dev-only
  @page-events
  Scenario Outline: All GA360 "ArticleList" events should registered for event handlers attached to "Domestic Pages" elements on "Domestic - <specific>" page (Dev)
    Given "Robert" visits the "Domestic - <specific>" page

    When "Robert" triggers all GTM "ArticleList" events defined for "Domestic pages"

    Then following GTM events should be registered
      | action      | element | event   | type                  | value                        |
      | ContentLink | Article | gaEvent | Create an export plan | How to create an export plan |

    Examples:
      | specific                             |
      | Create an export plan - article list |


  @allure.link:CMS-1672
  @stage-only
  @page-events
  Scenario Outline: All GA360 "ArticleList" events should registered for event handlers attached to "Domestic Pages" elements on "Domestic - <specific>" page (Staging)
    Given "Robert" visits the "Domestic - <specific>" page

    When "Robert" triggers all GTM "ArticleList" events defined for "Domestic pages"

    Then following GTM events should be registered
      | action      | element | event   | type                  | value                                         |
      | ContentLink | Article | gaEvent | Create an export plan | Prepare to sell and deliver services overseas |
      | ContentLink | Article | gaEvent | Create an export plan | How to create an export plan                  |
      | ContentLink | Article | gaEvent | Create an export plan | Market services overseas                      |
      | ContentLink | Article | gaEvent | Create an export plan | Deliver services overseas                     |

    Examples:
      | specific                             |
      | Create an export plan - article list |


  @allure.link:CMS-1672
  @dev-only
  @page-events
  Scenario Outline: All GA360 "CountryGuidePage" events should registered for event handlers attached to "Domestic Pages" elements on "Domestic - <specific>" page (Dev)
    Given "Robert" visits the "Domestic - <specific>" page

    When "Robert" triggers all GTM "CountryGuidePage" events defined for "Domestic pages"

    Then following GTM events should be registered
      | action          | element         | event   | type        | value                                          |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Health and life sciences                       |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Oil and gas                                    |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Renewables                                     |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Fintech                                        |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Education                                      |
# On DEV country-guide-intro-ctas are not present
#      | Cta             | IntroRelatedCta | gaEvent | Not present | Export opportunities for Brazil                |
#      | Cta             | IntroRelatedCta | gaEvent | Not present | Sell online in Brazil                          |
#      | Cta             | IntroRelatedCta | gaEvent | Not present | Trade events for Brazil                        |
      | Cta             | NextStepCta     | gaEvent | Not present | Exporting to Brazil if there's no EU Exit deal |
      | Cta             | NextStepCta     | gaEvent | Not present | Get in touch with one of our trade advisers    |
      | Cta             | NextStepCta     | gaEvent | Not present | Read more advice about doing business abroad   |

    Examples:
      | specific       |
      | Brazil - guide |


  @allure.link:CMS-1672
  @stage-only
  @page-events
  Scenario Outline: All GA360 "CountryGuidePage" events should registered for event handlers attached to "Domestic Pages" elements on "Domestic - <specific>" page (Staging)
    Given "Robert" visits the "Domestic - <specific>" page

    When "Robert" triggers all GTM "CountryGuidePage" events defined for "Domestic pages"

    Then following GTM events should be registered
      | action          | element         | event   | type        | value                                          |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Health and life sciences                       |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Oil and gas                                    |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Renewables                                     |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Fintech                                        |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Education                                      |
      | Cta             | IntroRelatedCta | gaEvent | Not present | Export opportunities for Brazil                |
      | Cta             | IntroRelatedCta | gaEvent | Not present | Sell online in Brazil                          |
      | Cta             | IntroRelatedCta | gaEvent | Not present | Trade events for Brazil                        |
      | Cta             | NextStepCta     | gaEvent | Not present | Exporting to Brazil if there's no EU Exit deal |
      | Cta             | NextStepCta     | gaEvent | Not present | Get in touch with one of our trade advisers    |
      | Cta             | NextStepCta     | gaEvent | Not present | Read more advice about doing business abroad   |

    Examples:
      | specific       |
      | Brazil - guide |


  @allure.link:CMS-1672
  @stage-only
  @page-events
  Scenario Outline: All GA360 "CountryGuidePage" events should registered for event handlers attached to "Domestic Pages" elements on "Domestic - <specific>" page
    Given "Robert" visits the "Domestic - <specific>" page

    When "Robert" triggers all GTM "CountryGuidePage" events defined for "Domestic pages"

    Then following GTM events should be registered
      | action          | element         | event   | type        | value                                           |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Automotive                                      |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Food and drink                                  |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Health and life sciences                        |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Technology                                      |
      | Cta             | NextStepCta     | gaEvent | Not present | Exporting to Germany if there's no EU Exit deal |
      | Cta             | NextStepCta     | gaEvent | Not present | Get in touch with one of our trade advisers     |
      | Cta             | NextStepCta     | gaEvent | Not present | Read more advice about doing business abroad    |

    Examples:
      | specific                |
      | Germany - guide |


  @allure.link:CMS-1672
  @stage-only
  @page-events
  Scenario Outline: All GA360 "CountryGuidePage" events should registered for event handlers attached to "Domestic Pages" elements on "Domestic - <specific>" page
    Given "Robert" visits the "Domestic - <specific>" page

    When "Robert" triggers all GTM "CountryGuidePage" events defined for "Domestic pages"

    Then following GTM events should be registered
      | action          | element         | event   | type        | value                                         |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Aerospace and engineering                     |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Cyber security                                |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Health and life sciences                      |
      | Cta             | NextStepCta     | gaEvent | Not present | Exporting to Italy if there's no EU Exit deal |
      | Cta             | NextStepCta     | gaEvent | Not present | Get in touch with one of our trade advisers   |
      | Cta             | NextStepCta     | gaEvent | Not present | Read more advice about doing business abroad  |

    Examples:
      | specific              |
      | Italy - guide |


  @allure.link:CMS-1672
  @stage-only
  @page-events
  Scenario Outline: All GA360 "CountryGuidePage" events should registered for event handlers attached to "Domestic Pages" elements on "Domestic - <specific>" page
    Given "Robert" visits the "Domestic - <specific>" page

    When "Robert" triggers all GTM "CountryGuidePage" events defined for "Domestic pages"

    Then following GTM events should be registered
      | action          | element         | event   | type        | value                                               |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Automotive                                          |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Fintech                                             |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Life sciences                                       |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Offshore wind                                       |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Technology                                          |
      | Cta             | NextStepCta     | gaEvent | Not present | Exporting to South Korea if there's no EU Exit deal |
      | Cta             | NextStepCta     | gaEvent | Not present | Get in touch with one of our trade advisers         |
      | Cta             | NextStepCta     | gaEvent | Not present | Read more advice about doing business abroad        |

    Examples:
      | specific                    |
      | South Korea - guide |


  @allure.link:CMS-1672
  @stage-only
  @page-events
  Scenario Outline: All GA360 "CountryGuidePage" events should registered for event handlers attached to "Domestic Pages" elements on "Domestic - <specific>" page
    Given "Robert" visits the "Domestic - <specific>" page

    When "Robert" triggers all GTM "CountryGuidePage" events defined for "Domestic pages"

    Then following GTM events should be registered
      | action          | element         | event   | type        | value                                                   |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Defence and security                                    |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Food and drink                                          |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Offshore wind energy                                    |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Technology                                              |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Financial and professional services                     |
      | Cta             | NextStepCta     | gaEvent | Not present | Exporting to The Netherlands if there's no EU Exit deal |
      | Cta             | NextStepCta     | gaEvent | Not present | Get in touch with one of our trade advisers             |
      | Cta             | NextStepCta     | gaEvent | Not present | Read more advice about doing business abroad            |

    Examples:
      | specific                        |
      | The Netherlands - guide |


  @allure.link:CMS-1672
  @stage-only
  @page-events
  Scenario Outline: All GA360 "CountryGuidePage" events should registered for event handlers attached to "Domestic Pages" elements on "Domestic - <specific>" page
    Given "Robert" visits the "Domestic - <specific>" page

    When "Robert" triggers all GTM "CountryGuidePage" events defined for "Domestic pages"

    Then following GTM events should be registered
      | action          | element         | event   | type        | value                                          |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Healthcare and life sciences                   |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Advanced manufacturing                         |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Energy                                         |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Defence and security                           |
      | ExpressInterest | ExpanderControl | gaEvent | Not present | Infrastructure                                 |
      | Cta             | NextStepCta     | gaEvent | Not present | Exporting to Turkey if there's no EU Exit deal |
      | Cta             | NextStepCta     | gaEvent | Not present | Get in touch with one of our trade advisers    |
      | Cta             | NextStepCta     | gaEvent | Not present | Read more advice about doing business abroad   |

    Examples:
      | specific               |
      | Turkey - guide |
