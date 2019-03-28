Feature: Trade Profile


  @wip
  @needs-rework
  @ED-2093
  @ED-1759
  @profile
  @logo
  @bug
  @ED-2160
  @fixed
  @fake-sso-email-verification
  Scenario Outline: Supplier should be able to upload an image to set company's logo
    Given "Peter Alder" has created verified and published business profile for randomly selected company "Y"

    When "Peter Alder" uploads "<valid_image>" as company's logo

    Then "Peter Alder" should see that logo on FAB Company's Directory Profile page
    And "Peter Alder" should see a PNG logo thumbnail on FAS Company's Directory Profile page

    Examples:
      | valid_image                                  |
      | Anfiteatro_El_Jem.jpeg                       |
      | Kobe_Port_Tower.jpg                          |
      | archive-org-solid-background.png             |
      | Wikipedia-logo-v2-en-alpa-channel.png        |
      | Animated_PNG_example_bouncing_beach_ball.png |


  @wip
  @needs-rework
  @ED-2093
  @ED-1759
  @profile
  @logo
  @fake-sso-email-verification
  Scenario Outline: Supplier should be able to replace an existing company's logo with a new one
    Given "Peter Alder" has created verified and published business profile for randomly selected company "Y"
    And "Peter Alder" has set "<original>" picture as company's logo
    And "Peter Alder" can see that logo on FAB Company's Directory Profile page
    And "Peter Alder" can see a PNG logo thumbnail on FAS Company's Directory Profile page

    When "Peter Alder" uploads "<new_picture>" as company's logo

    Then "Peter Alder" should see that logo on FAB Company's Directory Profile page
    And "Peter Alder" should see different updated thumbnail of the logo on FAS Company's Directory Profile page

    Examples:
      | original               | new_picture         |
      | Anfiteatro_El_Jem.jpeg | Kobe_Port_Tower.jpg |


  @wip
  @needs-rework
  @ED-1759
  @profile
  @logo
  @fake-sso-email-verification
  Scenario: Supplier should not be able to upload files other than images as company's logo
    Given "Peter Alder" has created verified and published business profile for randomly selected company "Y"

    When "Peter Alder" attempts to upload a file of unsupported type as company's logo
      | file                  | type                    |
      | Anfiteatro_El_Jem.bmp | Bitmap                  |
      | Anfiteatro_El_Jem.jp2 | JPEG 2000               |
      | Kobe_Port_Tower.webp  | Web P                   |
      | example.exe           | Windows executable file |
      | example.com           | Windows executable file |
      | example.sh            | Linux shell script      |
      | example.bat           | Windows shell script    |
      | example.txt           | text file               |

    Then for every uploaded unsupported file "Peter Alder" should be told that only certain image types can be used as company's logo


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

    Then "Peter Alder" should see links to all online profiles on FAB Company's Directory Profile page
    And "Peter Alder" should see links to all online profiles on FAS Company's Directory Profile page


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

    Then "Peter Alder" should not see any links to online profiles on FAB Company's Directory Profile page
    And "Peter Alder" should not see any links to online profiles on FAS Company's Directory Profile page


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
