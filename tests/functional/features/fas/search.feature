Feature: Find a Supplier


  @ED-1746
  @fas
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


  @ED-1746
  @fas
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
  @fas
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
  @fas
  @search
  @profile
  @verified
  @published
  Scenario: Buyers should be able to find Supplier by uniquely identifying words present on Supplier's profile
    Given "Annette Geissinger" is a buyer
    And "Peter Alder" is an unauthenticated supplier
    And "Peter Alder" has created and verified profile for randomly selected company "Y"
    And "Peter Alder" has added links to online profiles
      | online profile  |
      | Facebook        |
      | LinkedIn        |
      | Twitter         |

    When "Annette Geissinger" searches for company "Y" on FAS using selected company's details
      | company detail |
      | title          |
      | number         |
      | keywords       |
      | website        |
      | summary        |
      | description    |
      | facebook       |
      | twitter        |
      | linkedin       |

    Then "Annette Geissinger" should be able to find company "Y" on FAS using selected company's details
      | company detail |
      | title          |
      | number         |
      | keywords       |
      | website        |
      | summary        |
      | description    |
      | facebook       |
      | twitter        |
      | linkedin       |
