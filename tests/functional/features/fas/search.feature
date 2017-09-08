@fas
Feature: Find a Supplier


  @ED-1746
  @case-study
  @profile
  @verified
  @published
  @two-actors
  @bug
  @ED-1968
  @fixed
  Scenario: Buyers should be able to find Supplier by uniquely identifying words present on Supplier's case study
    Given "Annette Geissinger" is a buyer
    And "Peter Alder" is an unauthenticated supplier
    And "Peter Alder" has created and verified profile for randomly selected company "Y"

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
      | testimonial               |
      | source name               |
      | source job                |
      | source company            |
      | website                   |
      | keywords                  |
      | slug                      |


  @ED-1746
  @case-study
  @profile
  @verified
  @published
  Scenario: Buyers should be able to find Supplier by uniquely identifying words present on any of Supplier's case studies
    Given "Annette Geissinger" is a buyer
    And "Peter Alder" is an unauthenticated supplier
    And "Peter Alder" has created and verified profile for randomly selected company "Y"

    When "Peter Alder" adds a complete case study called "no 1"
    And "Peter Alder" adds a complete case study called "no 2"
    And "Peter Alder" adds a complete case study called "no 3"

    Then "Annette Geissinger" should be able to find company "Y" on FAS using any part of case study "no 1"
    And "Annette Geissinger" should be able to find company "Y" on FAS using any part of case study "no 2"
    And "Annette Geissinger" should be able to find company "Y" on FAS using any part of case study "no 3"


  @ED-1746
  @case-study
  @profile
  @unverified
  @unpublished
  Scenario: Buyers should NOT be able to find unverified Supplier by uniquely identifying words present on Supplier's case study
    Given "Annette Geissinger" is a buyer
    And "Peter Alder" is an unauthenticated supplier
    And "Peter Alder" created an unverified profile for randomly selected company "Y"

    When "Peter Alder" adds a complete case study called "no 1"

    Then "Annette Geissinger" should NOT be able to find company "Y" on FAS by using any part of case study "no 1"


  @ED-1967
  @search
  @profile
  @verified
  @published
  Scenario: Buyers should be able to find Supplier by uniquely identifying words present on Supplier's profile
    Given "Annette Geissinger" is a buyer
    And "Peter Alder" is an unauthenticated supplier
    And "Peter Alder" has created and verified profile for randomly selected company "Y"
    And "Peter Alder" gets the slug for company "Y"

    When "Annette Geissinger" searches for company "Y" on FAS using selected company's details
      | company detail |
      | title          |
      | number         |
      | keywords       |
      | website        |
      | summary        |
      | description    |
      | slug           |

    Then "Annette Geissinger" should be able to find company "Y" on FAS using selected company's details
      | company detail |
      | title          |
      | number         |
      | keywords       |
      | website        |
      | summary        |
      | description    |
      | slug           |


  @ED-2000
  @search
  Scenario: Empty search query should return no results
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" searches for companies on FAS with empty search query

    Then "Annette Geissinger" should be told that the search did not match any UK trade profiles

    
  @ED-2020
  @search
  Scenario: Buyers should be able to find Suppliers by product, service or company keyword
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" searches for Suppliers using product name, service name and a keyword
      | product                      | service                                  | keyword                    | company                                                  |
      | Aerosol Paints               | Supply all types of Aerosols             | vanishing spray            | KING OF PAINTS                                           |
      | LINSIG traffic signal models | management of transport                  | drainage civil engineering | CALLIDUS TRANSPORT & ENGINEERING LTD                     |
      | peristaltic pump             | deliver the maximum possible performance | brushless                  | ZIKODRIVE MOTOR CONTROLLERS (ROUND BANK ENGINEERING LTD) |

    Then "Annette Geissinger" should be able to find all sought companies


  @ED-2017
  @filter
  @sector
  @search
  Scenario: Buyers should be able to browse UK Suppliers by any of available sectors
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" browse Suppliers by every available sector filter

    Then "Annette Geissinger" should see search results filtered by appropriate sector


  @ED-2018
  @filter
  @sector
  @search
  Scenario: Buyers should be able to browse UK Suppliers by multiple sectors at once
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" browse Suppliers by multiple sector filters

    Then "Annette Geissinger" should see search results filtered by appropriate sectors


  @ED-2018
  @filter
  @sector
  @search
  @invalid
  Scenario: Buyers should NOT be able to browse UK Suppliers by invalid sectors
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" attempts to browse Suppliers by invalid sector filter

    Then "Annette Geissinger" should be told that the search did not match any UK trade profiles


  @ED-2019
  @filter
  @sector
  @search
  Scenario: Buyers should be able to clear search results filters
    Given "Annette Geissinger" is a buyer

    When "Annette Geissinger" browse Suppliers by multiple sector filters
    And "Annette Geissinger" clears the search filters

    Then "Annette Geissinger" should be told that the search did not match any UK trade profiles
    And "Annette Geissinger" should see that search results are not filtered by any sector


  @ED-1824
  @filter
  @sector
  @search
  Scenario: Buyers should not see the same company multiple times in the search results even if all associated sector filters are used
    Given "Annette Geissinger" is a buyer
    And "Annette Geissinger" finds a Supplier "Y" with a published profile associated with at least "5" different sectors

    When "Annette Geissinger" browse first "10" pages of Suppliers filtered by all sectors associated with company "Y"

    Then "Annette Geissinger" should see company "Y" only once on browsed search result pages
