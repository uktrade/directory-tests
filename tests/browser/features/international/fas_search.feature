@ED-3183
@ED-4259
@industry-pages
@no-sso-email-verification-required
Feature: Industry pages

  Background:
    Given basic authentication is done for "International - Landing" page


  @ED-4263
  @search
  Scenario Outline: Buyers should be able to find UK suppliers from "<specific> Industry"
    Given "Robert" visits the "Find a Supplier - Landing" page

    When "Robert" searches for companies using "<following>" keyword in "<specific>" sector

    Then "Robert" should be on the "Find a Supplier - search results" page
    And "Robert" should see search results filtered by "<specific>" industry

    Examples: Industries
      | following  | specific                               |
      | plants     | Agriculture horticulture and fisheries |
      | digital    | Creative and media                     |
      | surgery    | Healthcare and medical                 |

    @full
    Examples: Industries
      | following  | specific                               |
      | WiFi       | Security                               |
      | beer       | Food and drink                         |
      | arenas     | Global sports infrastructure           |
      | salon      | Clothing Footwear And Fashion          |
