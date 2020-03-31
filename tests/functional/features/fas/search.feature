@fas
@allure.suite:FAS
Feature: Find a Supplier


  @bug
  @allure.issue:TT-1438
  @fixed
  @allure.link:ED-1746
  @case-study
  @profile
  @verified
  @published
  @two-actors
  @bug
  @allure.issue:ED-1968
  @fixed
  @bug
  @allure.issue:ED-3031
  @fixed
  @captcha
  @dev-only
  @found-with-automated-tests
  @fake-sso-email-verification
  Scenario: Buyers should be able to find Supplier by uniquely identifying words present on Supplier's case study
    Given "Annette Geissinger" is a buyer
    And "Peter Alder" is an unauthenticated supplier
    And "Peter Alder" created a "published LTD, PLC or Royal Charter" profile for a random company "Y"

    When "Peter Alder" adds a complete case study called "no 1"
    And "Peter Alder" gets the slug for case study "no 1"

    Then "Annette Geissinger" should be able to find company "Y" on FAS using words from case study "no 1"
      | search using case study's |
      | title                     |
      | summary                   |
      | description               |
      | caption 1                 |
      | caption 2                 |
      | caption 3                 |
#      | testimonial               |
#      | source name               |
#      | source job                |
      | source company            |
      | website                   |
#      | keywords                  |


  @allure.link:ED-1746
  @case-study
  @profile
  @verified
  @published
  @bug
  @allure.issue:ED-3031
  @fixed
  @captcha
  @dev-only
  @found-with-automated-tests
  @fake-sso-email-verification
  Scenario: Buyers should be able to find Supplier by uniquely identifying words present on any of Supplier's case studies
    Given "Annette Geissinger" is a buyer
    And "Peter Alder" is an unauthenticated supplier
    And "Peter Alder" created a "published LTD, PLC or Royal Charter" profile for a random company "Y"

    When "Peter Alder" adds a complete case study called "no 1"
    And "Peter Alder" adds a complete case study called "no 2"
    And "Peter Alder" adds a complete case study called "no 3"
    And "Peter Alder" gets the slug for case study "no 1"
    And "Peter Alder" gets the slug for case study "no 2"
    And "Peter Alder" gets the slug for case study "no 3"

    Then "Annette Geissinger" should be able to find company "Y" on FAS using any part of case study "no 1"
    And "Annette Geissinger" should be able to find company "Y" on FAS using any part of case study "no 2"
    And "Annette Geissinger" should be able to find company "Y" on FAS using any part of case study "no 3"


  @allure.link:ED-1746
  @case-study
  @profile
  @unverified
  @unpublished
  @bug
  @allure.issue:ED-3031
  @fixed
  @bug
  @allure.issue:TT-727
  @fixed
  @captcha
  @dev-only
  @found-with-automated-tests
  @no-sso-email-verification-required
  Scenario: Buyers should NOT be able to find unverified Supplier by uniquely identifying words present on Supplier's case study
    Given "Annette Geissinger" is a buyer
    And "Peter Alder" is an unauthenticated supplier
    And "Peter Alder" created an "unpublished unverified LTD, PLC or Royal Charter" profile for a random company "Y"

    When "Peter Alder" adds a complete case study called "no 1"

    Then "Annette Geissinger" should NOT be able to find company "Y" on FAS by using any part of case study "no 1"


  @allure.link:ED-1967
  @bug
  @allure.issue:TT-1256
  @fixed
  @search
  @profile
  @verified
  @published
  @captcha
  @dev-only
  @fake-sso-email-verification
  Scenario: Buyers should be able to find Supplier by uniquely identifying words present on Supplier's profile
    Given "Annette Geissinger" is a buyer
    And "Peter Alder" is an unauthenticated supplier
    And "Peter Alder" created a "published LTD, PLC or Royal Charter" profile for a random company "Y"
    And "Peter Alder" updates company's details
      | detail              |
      | other keywords      |
      | number of employees |
      | sector of interest  |
    And "Peter Alder" gets the slug for company "Y"

    When "Annette Geissinger" searches for company "Y" on FAS using selected company's details
      | company detail |
      | title          |
#      | keywords       | see TT-1525
      | summary        |
      | description    |
      | slug           |
#      | number         | see TT-1514
#      | website        |

    Then "Annette Geissinger" should be able to find company "Y" on FAS using selected company's details
      | company detail |
      | title          |
#      | keywords       | see TT-1525
      | summary        |
      | description    |
      | slug           |
#      | number         | see TT-1514
#      | website        |


  @allure.link:ED-2000
  @search
  @no-sso-email-verification-required
  Scenario: Empty search query should return no results
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" searches for FAS companies with empty search query

    Then "Annette Geissinger" should be told to enter a search term or use the filters


  @dev-only
  @allure.link:ED-2020
  @search
  @no-sso-email-verification-required
  Scenario: Buyers should be able to find Suppliers by product, service or keyword (Dev)
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" searches for Suppliers using product name, service name and a keyword
      | product                  | service                 | keyword           | company                 |
      | meaningful relationships | Strategy & Planning     | NationalJigsawDay | AGENCY UK               |
      | logo animations          | content for broadcast   | 3dCG              | LIGHTRHYTHM VISUALS LTD |
      | CANbus displays          | CAN bus Instrumentation | NMEA2000          | CANTRONIK LTD           |
    Then "Annette Geissinger" should be able to find all sought companies


  @stage-only
  @allure.link:ED-2020
  @search
  @no-sso-email-verification-required
  Scenario: Buyers should be able to find Suppliers by product, service or keyword (Staging)
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" searches for Suppliers using product name, service name and a keyword
      | product                  | service                 | keyword           | company                 |
      | meaningful relationships | Strategy & Planning     | NationalJigsawDay | AGENCY UK               |
      | logo animations          | content for broadcast   | 3dCG              | LIGHTRHYTHM VISUALS LTD |
      | CANbus displays          | CAN bus Instrumentation | NMEA2000          | CANTRONIK LTD           |
    Then "Annette Geissinger" should be able to find all sought companies


  @uat-only
  @allure.link:ED-2020
  @search
  @no-sso-email-verification-required
  Scenario: Buyers should be able to find Suppliers by product, service or keyword (UAT)
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" searches for Suppliers using product name, service name and a keyword
      | product         | service                 | keyword  | company                 |
      | pokers          | construction equipment  | screeds  | MULTIQUIP (UK) LIMITED  |
      | logo animations | content for broadcast   | 3dCG     | LIGHTRHYTHM VISUALS LTD |
      | CANbus displays | CAN bus Instrumentation | NMEA2000 | CANTRONIK LTD           |
    Then "Annette Geissinger" should be able to find all sought companies


  @allure.link:ED-2017
  @filter
  @sector
  @search
  @no-sso-email-verification-required
  Scenario: Buyers should be able to browse UK Suppliers by any of available sectors
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" browse Suppliers by every available sector filter

    Then "Annette Geissinger" should see search results filtered by appropriate sector


  @allure.link:ED-2018
  @filter
  @sector
  @search
  @no-sso-email-verification-required
  Scenario: Buyers should be able to browse UK Suppliers by multiple sectors at once
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" browse Suppliers by multiple sector filters

    Then "Annette Geissinger" should see search results filtered by appropriate sectors


  @allure.link:ED-2018
  @filter
  @sector
  @search
  @invalid
  @no-sso-email-verification-required
  Scenario: Buyers should NOT be able to browse UK Suppliers by invalid sectors
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" attempts to browse Suppliers by invalid sector filter

    Then "Annette Geissinger" should be told that the search did not match any UK trade profiles


  @allure.link:ED-2019
  @filter
  @sector
  @search
  @no-sso-email-verification-required
  Scenario: Buyers should be able to clear search results filters
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" browse Suppliers by multiple sector filters
    And "Annette Geissinger" clears the search filters

    Then "Annette Geissinger" should be told to enter a search term or use the filters
    And "Annette Geissinger" should see that FAS search results are not filtered by any sector


  @allure.link:ED-1824
  @filter
  @sector
  @search
  @no-sso-email-verification-required
  Scenario: Buyers should not see the same company multiple times in the search results even if all associated sector filters are used
    Given "Annette Geissinger" is a buyer
    And "Annette Geissinger" finds a Supplier "Y" with a published profile associated with at least "4" different sectors

    When "Annette Geissinger" browse first "10" pages of Suppliers filtered by all sectors associated with company "Y"

    Then "Annette Geissinger" should see company "Y" only once on browsed search result pages


  @allure.link:ED-1983
  @search
  @contextual
  @no-sso-email-verification-required
  Scenario Outline: Buyers should see highlighted search term "<specific>" in the FAS search results - contextual results
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" searches for Suppliers using "<specific>" term

    Then "Annette Geissinger" should see that some of the results have the "<specific>" search terms highlighted

    Examples: terms
      | specific |
      | sweets   |
      | metal    |


  @allure.link:TT-1258
  @profile
  @verified
  @unpublished
  @captcha
  @dev-only
  @found-with-automated-tests
  Scenario: Unpublished business profiles (for any or ISD company) shouldn't appear in FAS search results
    Given "Peter Alder" created an "unpublished verified LTD, PLC or Royal Charter" profile for a random company "Y"
    And "Peter Alder" updates company's details
      | detail         |
      | keywords       |

    When "Peter Alder" searches for company "Y" on FAS using selected company's details
      | company detail |
      | title          |
      | number         |
      | website        |
      | summary        |
      | description    |
      | slug           |
      | keywords       |

    Then "Peter Alder" should NOT be able to find company "Y" on FAS using selected company's details
      | company detail |
      | title          |
      | number         |
      | website        |
      | summary        |
      | description    |
      | slug           |
      | keywords       |
