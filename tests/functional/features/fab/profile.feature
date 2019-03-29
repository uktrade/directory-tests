Feature: Trade Profile


  @wip
  @needs-rework
  @ED-1761
  @fab
  @profile
  @fake-sso-email-verification
  Scenario: Supplier should be able to add valid links to Online Profiles (social media URLs)
    Given "Peter Alder" has created verified and published business profile for randomly selected company "Y"

    When "Peter Alder" adds links to online profiles
      | online profile  |
      | Facebook        |
      | LinkedIn        |
      | Twitter         |

    Then "Peter Alder" should see links to all online profiles on Edit Business Profile page
    And "Peter Alder" should see links to all online profiles on FAS Business Profile page


  @wip
  @needs-rework
  @ED-1762
  @fab
  @profile
  @fake-sso-email-verification
  Scenario: Supplier should NOT be able to use invalid links to Online Profiles - explicit social media URLs
    Given "Peter Alder" has created verified and published business profile for randomly selected company "Y"

    When "Peter Alder" attempts to use invalid links to online profiles
      | online profile  | invalid link               |
      | Facebook        | https://wrong.facebook.url |
      | LinkedIn        | https://wrong.linkedin.url |
      | Twitter         | https://wrong.twitter.url  |

    Then "Peter Alder" should be told to provide valid links to all online profiles


  @wip
  @needs-rework
  @ED-1762
  @fab
  @profile
  @bug
  @ED-1833
  @fixed
  @fake-sso-email-verification
  Scenario: Supplier should NOT be able to use invalid links to Online Profiles (social media URLs)
    Given "Peter Alder" has created verified and published business profile for randomly selected company "Y"

    When "Peter Alder" attempts to use invalid links to online profiles
      | online profile  | invalid link           |
      | Facebook        | http://notfacebook.com |
      | LinkedIn        | http://notlinkedin.com |
      | Twitter         | http://nottwitter.com  |

    Then "Peter Alder" should be told to provide valid links to all online profiles


  @wip
  @needs-rework
  @ED-1763
  @fab
  @profile
  @fake-sso-email-verification
  Scenario: Supplier should be able to remove links to all online profiles (social media URLs)
    Given "Peter Alder" has created verified and published business profile for randomly selected company "Y"
    And "Peter Alder" has added links to online profiles
      | online profile  |
      | Facebook        |
      | LinkedIn        |
      | Twitter         |

    When "Peter Alder" removes links to all online profiles

    Then "Peter Alder" should not see any links to online profiles on edit Business Profile page
    And "Peter Alder" should not see any links to online profiles on FAS Business Profile page


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
