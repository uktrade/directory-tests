Feature: Trade Profile


  @wip
  @needs-rework
  @ED-1764
  @fab
  @case-study
  @profile
  @fake-sso-email-verification
  Scenario: Supplier should be able to add a case study to unverified company
    Given "Peter Alder" created an unverified business profile for randomly selected company "Y"

    When "Peter Alder" adds a complete case study called "no 1"

    Then "Peter Alder" should see all case studies on the FAB Company's Directory Profile page


  @wip
  @needs-rework
  @ED-1764
  @fab
  @case-study
  @profile
  @fake-sso-email-verification
  Scenario: Supplier should be able to add a case study to verified company
    Given "Peter Alder" has created verified and published business profile for randomly selected company "Y"

    When "Peter Alder" adds a complete case study called "no 1"

    Then "Peter Alder" should see all case studies on the FAB Company's Directory Profile page
    And "Peter Alder" should see all case studies on the FAS Company's Directory Profile page


  @wip
  @needs-rework
  @ED-1765
  @fab
  @case-study
  @profile
  @fake-sso-email-verification
  Scenario: Supplier should be able to add multiple case studies to unverified company
    Given "Peter Alder" created an unverified business profile for randomly selected company "Y"

    When "Peter Alder" adds a complete case study called "no 1"
    And "Peter Alder" adds a complete case study called "no 2"
    And "Peter Alder" adds a complete case study called "no 3"
    And "Peter Alder" adds a complete case study called "no 4"

    Then "Peter Alder" should see all case studies on the FAB Company's Directory Profile page


  @wip
  @needs-rework
  @ED-1765
  @fab
  @case-study
  @profile
  @fake-sso-email-verification
  Scenario: Supplier should be able to add multiple case studies to verified company
    Given "Peter Alder" has created verified and published business profile for randomly selected company "Y"

    When "Peter Alder" adds a complete case study called "no 1"
    And "Peter Alder" adds a complete case study called "no 2"
    And "Peter Alder" adds a complete case study called "no 3"
    And "Peter Alder" adds a complete case study called "no 4"

    Then "Peter Alder" should see all case studies on the FAB Company's Directory Profile page
    And "Peter Alder" should see all case studies on the FAS Company's Directory Profile page


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

    Then "Peter Alder" should see all case studies on the FAB Company's Directory Profile page


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

    Then "Peter Alder" should see all case studies on the FAB Company's Directory Profile page
    And "Peter Alder" should see all case studies on the FAS Company's Directory Profile page


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

    Then "Peter Alder" should see all case studies on the FAB Company's Directory Profile page


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

    Then "Peter Alder" should see all case studies on the FAB Company's Directory Profile page
    And "Peter Alder" should see all case studies on the FAS Company's Directory Profile page
