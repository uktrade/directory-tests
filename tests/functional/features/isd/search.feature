@isd
Feature: Investment Support Directory


  @search
  @no-sso-email-verification-required
  Scenario: Empty search query should return all published ISD companies
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" searches for ISD companies with empty search query

    Then "Annette Geissinger" should see that ISD search results are not filtered by any sector


  @wip
  @search
  @no-sso-email-verification-required
  Scenario Outline: Buyers should be able to find UK specialist "<UK specialist>" by its profile details
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" searches for UK specialists by profile details
      | description   | case study   | service   | keyword   | website   |
      | <description> | <case study> | <service> | <keyword> | <website> |

    Then "Annette Geissinger" should be able to find ISD "<UK specialist>" company

    Examples: search terms
      | description | case study | service  | keyword             | website                             | UK specialist                         |
      | key needs   | seminar    | Branding | Exhibition Training | http://www.inspiringexhibitors.com/ | 12th MAN SOLUTIONS LIMITED / PROEXTRA |


  @wip
  @filter
  @sector
  @search
  @no-sso-email-verification-required
  Scenario: Buyers should be able to browse UK specialists by any of available sectors
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" browse UK specialists by every available sector filter

    Then "Annette Geissinger" should see ISD search results filtered by all selected sectors


  @wip
  @filter
  @sector
  @search
  @no-sso-email-verification-required
  Scenario: Buyers should be able to browse UK suppliers by multiple sectors at once
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" browse UK suppliers by multiple sector filters

    Then "Annette Geissinger" should see ISD search results filtered by all selected sectors


  @wip
  @filter
  @sector
  @search
  @invalid
  @no-sso-email-verification-required
  Scenario: Buyers should NOT be able to browse UK suppliers by invalid sectors
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" attempts to browse UK suppliers by invalid sector filter

    Then "Annette Geissinger" should be told that the ISD search did not match any UK businesses


  @wip
  @filter
  @sector
  @search
  @no-sso-email-verification-required
  Scenario: Buyers should be able to clear search results filters
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" browse UK suppliers by multiple sector filters
    And "Annette Geissinger" clears the search filters

    Then "Annette Geissinger" should be told that the ISD search did not match any UK businesses
    And "Annette Geissinger" should see that ISD search results are not filtered by any sector


  @wip
  @filter
  @sector
  @search
  @no-sso-email-verification-required
  Scenario: Buyers should not see the same company multiple times in the search results even if all associated sector filters are used
    Given "Annette Geissinger" is a buyer
    And "Annette Geissinger" finds a UK specialist "Y" with a published profile associated with at least "4" different sectors

    When "Annette Geissinger" browse first "10" pages of UK specialists filtered by all sectors associated with company "Y"

    Then "Annette Geissinger" should see ISD company "Y" only once on browsed search result pages


  @wip
  @search
  @contextual
  @no-sso-email-verification-required
  Scenario Outline: Buyers should see highlighted search terms in the search results - contextual results
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" searches for UK suppliers using "<specific>" term

    Then "Annette Geissinger" should see that some of the ISD results have the "<specific>" search terms highlighted

    Examples: terms
      | specific |
      | sweets   |
      | metal    |
