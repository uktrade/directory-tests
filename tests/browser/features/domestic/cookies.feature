@cookies
@allure.suite:Domestic
Feature: Domestic - Cookies Policy

  Background:
    Given test authentication is done


  @allure.link:TT-2319
  Scenario Outline: Accepting all cookies on "<specific>" page should trigger appropriate GA event and set correct cookies policy
    Given "Robert" visited the "Domestic - <specific>" page

    When "Robert" accepts all cookies

    Then following GTM events should be registered
      | action    | destination | element | event   | type | value              |
      | clickLink | #           |         | gaEvent | CTA  | Accept all cookies |
    And following cookies should be set
      | name                   | value                                                            |
      | cookie_preferences_set | true                                                             |
      | cookies_policy         | {"essential":true,"settings":true,"usage":true,"campaigns":true} |

    Examples:
      | specific                                 |
      | Home                                     |
      | Advice landing                           |
      | Markets listing                          |
      | Services                                 |
      | Search results                           |
      | Transition period enquiries - contact us |
      | Create an export plan - article list     |
      | Get export finance - article list        |
      | Join our export community - landing      |
      | Join our Export Community - form         |


  @allure.link:TT-2319
  Scenario Outline: Users should be able to "<make a decision on>" cookies via "Cookies on great.gov.uk" page should trigger appropriate GA event and set correct cookies policy
    Given "Robert" visited the "Domestic - Cookies" page

    When "Robert" fills out and submits the form with captcha dev check turned "off"
      | field                              | value           |
      | Allow measure website use          | <usage on>      |
      | Allow use for marketing campaigns  | <campaigns on>  |
      | Allow to remember my settings      | <settings on>   |
      | Do not measure website use         | <usage off>     |
      | Do not use for marketing campaigns | <campaigns off> |
      | Do not remember my settings        | <settings off>  |

    Then "Robert" should see following sections
      | Sections            |
      | Confirmation banner |
    And following GTM events should be registered
      | action | element                 | event   | type | value |
      | submit | cookie-preferences-form | gaEvent | form |       |
    And following cookies should be set
      | name                   | value            |
      | cookie_preferences_set | true             |
      | cookies_policy         | <cookies_policy> |

    Examples:
      | make a decision on             | usage on  | campaigns on | settings on | usage off | campaigns off | settings off | cookies_policy                                                      |
      | Accept all                     | checked   | checked      | checked     | unchecked | unchecked     | unchecked    | {"essential":true,"settings":true,"usage":true,"campaigns":true}    |
      | Reject all                     | unchecked | unchecked    | unchecked   | checked   | checked       | checked      | {"essential":true,"settings":false,"usage":false,"campaigns":false} |
      | Reject measuring website use   | unchecked | checked      | checked     | checked   | unchecked     | unchecked    | {"essential":true,"settings":true,"usage":false,"campaigns":true}   |
      | Reject marketing campaigns     | checked   | unchecked    | checked     | unchecked | checked       | unchecked    | {"essential":true,"settings":true,"usage":true,"campaigns":false}   |
      | Reject remembering my settings | checked   | checked      | unchecked   | unchecked | unchecked     | checked      | {"essential":true,"settings":false,"usage":true,"campaigns":true}   |
      | Allow measuring website use    | checked   | unchecked    | unchecked   | unchecked | checked       | checked      | {"essential":true,"settings":false,"usage":true,"campaigns":false}  |
      | Allow marketing campaigns      | unchecked | checked      | unchecked   | checked   | unchecked     | checked      | {"essential":true,"settings":false,"usage":false,"campaigns":true}  |
      | Allow to remember my settings  | unchecked | unchecked    | checked     | checked   | checked       | unchecked    | {"essential":true,"settings":true,"usage":false,"campaigns":false}  |
