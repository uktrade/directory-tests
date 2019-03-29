Feature: Trade Profile


  @wip
  @needs-rework
  @ED-1803
  @fab
  @case-study
  @profile
  @fake-sso-email-verification
  @bug
  @ED-3040
  @fixed
  @found-with-automated-tests
  Scenario: Supplier should be able to update a case study for an unverified company
    Given "Peter Alder" created an unverified business profile for randomly selected company "Y"
    And "Peter Alder" added a complete case study called "no 1"

    When "Peter Alder" updates all the details of case study called "no 1"

    Then "Peter Alder" should see all case studies on the edit Business Profile page


  @wip
  @needs-rework
  @ED-1803
  @fab
  @case-study
  @profile
  @fake-sso-email-verification
  @bug
  @ED-3040
  @fixed
  @found-with-automated-tests
  Scenario: Supplier should be able to update a case study for a verified company
    Given "Peter Alder" has created verified and published business profile for randomly selected company "Y"
    And "Peter Alder" added a complete case study called "no 1"

    When "Peter Alder" updates all the details of case study called "no 1"

    Then "Peter Alder" should see all case studies on the edit Business Profile page
    And "Peter Alder" should see all case studies on the FAS Business Profile page


  @wip
  @needs-rework
  @ED-1804
  @fab
  @case-study
  @profile
  @fake-sso-email-verification
  @bug
  @ED-3040
  @fixed
  @found-with-automated-tests
  Scenario: Supplier should be able to update multiple case studies for an unverified company
    Given "Peter Alder" created an unverified business profile for randomly selected company "Y"
    And "Peter Alder" added a complete case study called "no 1"
    And "Peter Alder" added a complete case study called "no 2"
    And "Peter Alder" added a complete case study called "no 3"

    When "Peter Alder" updates all the details of case study called "no 1"
    And "Peter Alder" updates all the details of case study called "no 2"
    And "Peter Alder" updates all the details of case study called "no 3"

    Then "Peter Alder" should see all case studies on the edit Business Profile page


  @wip
  @needs-rework
  @ED-1804
  @fab
  @case-study
  @profile
  @fake-sso-email-verification
  @bug
  @ED-3040
  @fixed
  @found-with-automated-tests
  Scenario: Supplier should be able to update multiple case studies for a verified company
    Given "Peter Alder" has created verified and published business profile for randomly selected company "Y"
    And "Peter Alder" added a complete case study called "no 1"
    And "Peter Alder" added a complete case study called "no 2"
    And "Peter Alder" added a complete case study called "no 3"

    When "Peter Alder" updates all the details of case study called "no 1"
    And "Peter Alder" updates all the details of case study called "no 2"
    And "Peter Alder" updates all the details of case study called "no 3"

    Then "Peter Alder" should see all case studies on the edit Business Profile page
    And "Peter Alder" should see all case studies on the FAS Business Profile page
