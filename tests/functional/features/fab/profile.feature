Feature: Trade Profile


    @ED-1659
    @registration
    @real-sso-email-verification
    Scenario: Supplier should receive a verification email after successful registration - company has exported in the past
      Given "Peter Alder" is an unauthenticated supplier

      When "Peter Alder" randomly selects an active company without a Directory Profile identified by an alias "Company X"
      And "Peter Alder" confirms that "Company X" is the correct one
      And "Peter Alder" confirms that the company has exported in the past
      And "Peter Alder" creates a SSO/great.gov.uk account for "Company X" using valid credentials

      Then "Peter Alder" should be told about the verification email
      And "Peter Alder" should receive an email verification msg entitled "Your great.gov.uk account: Please Confirm Your E-mail Address"


    @ED-1659
    @registration
    @real-sso-email-verification
    Scenario: Supplier should receive a verification email after successful registration - company has not exported in the past
      Given "Peter Alder" is an unauthenticated supplier

      When "Peter Alder" randomly selects an active company without a Directory Profile identified by an alias "Company X"
      And "Peter Alder" confirms that "Company X" is the correct one
      And "Peter Alder" confirms that the company has not exported in the past
      And "Peter Alder" creates a SSO/great.gov.uk account for "Company X" using valid credentials

      Then "Peter Alder" should be told about the verification email
      And "Peter Alder" should receive an email verification msg entitled "Your great.gov.uk account: Please Confirm Your E-mail Address"


    @ED-1692
    @verification
    @real-sso-email-verification
    Scenario: Unauthenticated Suppliers should be able to verify their email address via confirmation link sent in an email
      Given "Annette Geissinger" created an unverified SSO/great.gov.uk account associated with randomly selected company "Company X"
      And "Annette Geissinger" received the email verification message with the email confirmation link

      When "Annette Geissinger" decides to confirm her email address by using the email confirmation link
      And "Annette Geissinger" confirms the email address

      Then "Annette Geissinger" should be prompted to build and improve your Directory Profile


    @ED-1757
    @verification
    @login
    @no-sso-email-verification-required
    Scenario: Suppliers without verified email should be told to verify the email address first before being able to log in
      Given "Annette Geissinger" created an unverified SSO/great.gov.uk account associated with randomly selected company "Company X"

      When "Annette Geissinger" attempts to sign in to Find a Buyer profile

      Then "Annette Geissinger" should be told that she needs to verify her email address first


    @ED-1716
    @profile
    @fake-sso-email-verification
    Scenario: Supplier should be able to build the Directory Profile once the email address is confirmed
      Given "Annette Geissinger" created a verified SSO/great.gov.uk account associated with randomly selected company "Company X"

      When "Annette Geissinger" provides valid details of selected company
      And "Annette Geissinger" selects sector the company is in and preferred country of export
      And "Annette Geissinger" decides to verify her identity with a verification letter

      Then "Annette Geissinger" should be on edit Company's Directory Profile page
      And "Annette Geissinger" should be told that her company has no description


    @ED-2141
    @profile
    @fake-sso-email-verification
    Scenario: Supplier should not be able to use other characters than alphanumerics and commas in profile keywords
      Given "Annette Geissinger" created a verified SSO/great.gov.uk account associated with randomly selected company "Company X"

      When "Annette Geissinger" provides company details using following values
        |company name  |website       |keywords         |separator |size    |error                                                       |
        |empty string  |empty string  |book, keys, food |comma     |1-10    |This field is required.                                     |
        |unchanged     |empty string  |book, keys, food |pipe      |11-50   |You can only enter letters, numbers and commas.             |
        |unchanged     |valid http    |sky, sea, blues  |semi-colon|51-200  |You can only enter letters, numbers and commas.             |
        |unchanged     |valid https   |sand, dunes, bird|colon     |201-500 |You can only enter letters, numbers and commas.             |
        |unchanged     |empty string  |bus, ferry, plane|full stop |501-1000|You can only enter letters, numbers and commas.             |
        |unchanged     |valid https   |sand, dunes, bird|comma     |unset   |This field is required.                                     |
        |unchanged     |valid http    |empty string     |comma     |51-200  |This field is required.                                     |
        |256 characters|valid https   |sand, dunes, bird|comma     |1-10    |Ensure this value has at most 255 characters (it has 256).  |
        |unchanged     |empty string  |1001 characters  |comma     |1-10    |Ensure this value has at most 1000 characters (it has 1001).|

      Then "Annette Geissinger" should see expected error messages


    @ED-2141
    @profile
    @bug
    @ED-2170
    @fixme
    @fake-sso-email-verification
    Scenario: Supplier should not be able to use other characters than alphanumerics and commas in profile keywords
      Given "Annette Geissinger" created a verified SSO/great.gov.uk account associated with randomly selected company "Company X"

      When "Annette Geissinger" provides company details using following values
        |company name  |website       |keywords         |separator |size  |error                                                     |
        |unchanged     |256 characters|sand, dunes, bird|comma     |1-10  |Ensure this value has at most 255 characters (it has 256).|
        |unchanged     |invalid http  |sand, dunes, bird|comma     |1-10  |Enter a valid URL.                                        |
        |unchanged     |invalid https |sand, dunes, bird|comma     |11-50 |Enter a valid URL.                                        |

      Then "Annette Geissinger" should see expected error messages


    @ED-1722
    @verification
    @letter
    @fake-sso-email-verification
    Scenario: Supplier should be able to verify company using code sent in the verification letter
      Given "Annette Geissinger" created a verified SSO/great.gov.uk account associated with randomly selected company "Company X"
      And "Annette Geissinger" built the company profile
      And "Annette Geissinger" set the company description

      When "Annette Geissinger" verifies the company with the verification code from the letter sent after Directory Profile was created

      Then "Annette Geissinger" should be on edit Company's Directory Profile page
      And "Annette Geissinger" should be told that her company is published


    @ED-1727
    @publish
    @FAS
    @fake-sso-email-verification
    Scenario: Once verified Company's Directory Profile should be published on FAS
      Given "Peter Alder" has created and verified profile for randomly selected company "Y"

      When "Peter Alder" decides to view published Directory Profile

      Then "Peter Alder" should be on FAS Directory Profile page of company "Y"


    @ED-1769
    @login
    @fab
    @fake-sso-email-verification
    Scenario: Suppliers with unverified company profile should be able to logout and log back in
      Given "Annette Geissinger" created a verified SSO/great.gov.uk account associated with randomly selected company "Company X"
      And "Annette Geissinger" signed out from Find a Buyer service

      When "Annette Geissinger" signs in to Find a Buyer profile

      Then "Annette Geissinger" should be on edit Company's Directory Profile page
      And "Annette Geissinger" should be told that her company has no description


    @ED-1770
    @sso
    @fab
    @account
    @fake-sso-email-verification
    Scenario: Suppliers with a standalone SSO/great.gov.uk account should be able to select their company for Directory Profile creation
      Given "Peter Alder" has a verified standalone SSO/great.gov.uk account
      And "Peter Alder" is signed in to SSO/great.gov.uk account

      When "Peter Alder" decides to create a trade profile
      And "Peter Alder" randomly selects an active company without a Directory Profile identified by an alias "Company X"
      And "Peter Alder" confirms that "Company X" is the correct one
      And "Peter Alder" confirms that the company has exported in the past

      Then "Peter Alder" should be prompted to build and improve your Directory Profile


    @ED-1770
    @sso
    @fab
    @account
    @fake-sso-email-verification
    Scenario: Suppliers with a standalone SSO/great.gov.uk account should be able to create a Directory profile
      Given "Peter Alder" has a verified standalone SSO/great.gov.uk account
      And "Peter Alder" is signed in to SSO/great.gov.uk account
      And "Peter Alder" selected an active company without a Directory Profile identified by an alias "Company X"

      When "Peter Alder" provides valid details of selected company
      And "Peter Alder" selects sector the company is in and preferred country of export
      And "Peter Alder" decides to verify his identity with a verification letter

      Then "Peter Alder" should be on edit Company's Directory Profile page
      And "Peter Alder" should be told that her company has no description


    @ED-1758
    @fab
    @login
    @fake-sso-email-verification
    Scenario: Suppliers with verified company profile should be able to logout and log back in
      Given "Peter Alder" has created and verified profile for randomly selected company "Y"
      And "Peter Alder" signed out from Find a Buyer service

      When "Peter Alder" signs in to Find a Buyer profile

      Then "Peter Alder" should be on edit Company's Directory Profile page
      And "Peter Alder" should be told that her company is published


    @ED-1760
    @ED-1766
    @fab
    @profile
    @fake-sso-email-verification
    Scenario: Supplier should be able to update company's details
      Given "Annette Geissinger" has created and verified profile for randomly selected company "Y"

      When "Annette Geissinger" updates company's details
        | detail                      |
        | business name               |
        | website                     |
        | keywords                    |
        | number of employees         |
        | sector of interest          |
        | countries to export to      |

      Then "Annette Geissinger" should see new details on FAB Company's Directory Profile page
        | detail                      |
        | business name               |
        | website                     |
        | keywords                    |
        | number of employees         |
        | sector of interest          |
      And "Annette Geissinger" should see new details on FAS Company's Directory Profile page
        | detail                      |
        | business name               |
        | website                     |
        | keywords                    |
        | number of employees         |
        | sector of interest          |


    @ED-2093
    @ED-1759
    @profile
    @logo
    @bug
    @ED-2160
    @fixed
    @fake-sso-email-verification
    Scenario Outline: Supplier should be able to upload an image to set company's logo
      Given "Peter Alder" has created and verified profile for randomly selected company "Y"

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



    @ED-2093
    @ED-1759
    @profile
    @logo
    @fake-sso-email-verification
    Scenario Outline: Supplier should be able to replace an existing company's logo with a new one
      Given "Peter Alder" has created and verified profile for randomly selected company "Y"
      And "Peter Alder" has set "<original>" picture as company's logo
      And "Peter Alder" can see that logo on FAB Company's Directory Profile page
      And "Peter Alder" can see a PNG logo thumbnail on FAS Company's Directory Profile page

      When "Peter Alder" uploads "<new_picture>" as company's logo

      Then "Peter Alder" should see that logo on FAB Company's Directory Profile page
      And "Peter Alder" should see different updated thumbnail of the logo on FAS Company's Directory Profile page

      Examples:
        | original               | new_picture         |
        | Anfiteatro_El_Jem.jpeg | Kobe_Port_Tower.jpg |


    @ED-1759
    @profile
    @logo
    @fake-sso-email-verification
    Scenario: Supplier should not be able to upload files other than images as company's logo
      Given "Peter Alder" has created and verified profile for randomly selected company "Y"

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


    @ED-1761
    @fab
    @profile
    @fake-sso-email-verification
    Scenario: Supplier should be able to add valid links to Online Profiles (social media URLs)
      Given "Peter Alder" has created and verified profile for randomly selected company "Y"

      When "Peter Alder" adds links to online profiles
        | online profile  |
        | Facebook        |
        | LinkedIn        |
        | Twitter         |

      Then "Peter Alder" should see links to all online profiles on FAB Company's Directory Profile page
      And "Peter Alder" should see links to all online profiles on FAS Company's Directory Profile page


    @ED-1762
    @fab
    @profile
    @fake-sso-email-verification
    Scenario: Supplier should NOT be able to use invalid links to Online Profiles - explicit social media URLs
      Given "Peter Alder" has created and verified profile for randomly selected company "Y"

      When "Peter Alder" attempts to use invalid links to online profiles
        | online profile  | invalid link               |
        | Facebook        | https://wrong.facebook.url |
        | LinkedIn        | https://wrong.linkedin.url |
        | Twitter         | https://wrong.twitter.url  |

      Then "Peter Alder" should be told to provide valid links to all online profiles


    @ED-1762
    @fab
    @profile
    @bug
    @ED-1833
    @fixed
    @fake-sso-email-verification
    Scenario: Supplier should NOT be able to use invalid links to Online Profiles (social media URLs)
      Given "Peter Alder" has created and verified profile for randomly selected company "Y"

      When "Peter Alder" attempts to use invalid links to online profiles
        | online profile  | invalid link           |
        | Facebook        | http://notfacebook.com |
        | LinkedIn        | http://notlinkedin.com |
        | Twitter         | http://nottwitter.com  |

      Then "Peter Alder" should be told to provide valid links to all online profiles


    @ED-1763
    @fab
    @profile
    @fake-sso-email-verification
    Scenario: Supplier should be able to remove links to all online profiles (social media URLs)
      Given "Peter Alder" has created and verified profile for randomly selected company "Y"
      And "Peter Alder" has added links to online profiles
        | online profile  |
        | Facebook        |
        | LinkedIn        |
        | Twitter         |

      When "Peter Alder" removes links to all online profiles

      Then "Peter Alder" should not see any links to online profiles on FAB Company's Directory Profile page
      And "Peter Alder" should not see any links to online profiles on FAS Company's Directory Profile page


    @ED-1764
    @fab
    @case-study
    @profile
    @fake-sso-email-verification
    Scenario: Supplier should be able to add a case study to unverified company
      Given "Peter Alder" created an unverified profile for randomly selected company "Y"

      When "Peter Alder" adds a complete case study called "no 1"

      Then "Peter Alder" should see all case studies on the FAB Company's Directory Profile page


    @ED-1764
    @fab
    @case-study
    @profile
    @fake-sso-email-verification
    Scenario: Supplier should be able to add a case study to verified company
      Given "Peter Alder" has created and verified profile for randomly selected company "Y"

      When "Peter Alder" adds a complete case study called "no 1"

      Then "Peter Alder" should see all case studies on the FAB Company's Directory Profile page
      And "Peter Alder" should see all case studies on the FAS Company's Directory Profile page


  @ED-1765
  @fab
  @case-study
  @profile
  @fake-sso-email-verification
  Scenario: Supplier should be able to add multiple case studies to unverified company
    Given "Peter Alder" created an unverified profile for randomly selected company "Y"

    When "Peter Alder" adds a complete case study called "no 1"
    And "Peter Alder" adds a complete case study called "no 2"
    And "Peter Alder" adds a complete case study called "no 3"
    And "Peter Alder" adds a complete case study called "no 4"

    Then "Peter Alder" should see all case studies on the FAB Company's Directory Profile page


    @ED-1765
    @fab
    @case-study
    @profile
    @fake-sso-email-verification
    Scenario: Supplier should be able to add multiple case studies to verified company
      Given "Peter Alder" has created and verified profile for randomly selected company "Y"

      When "Peter Alder" adds a complete case study called "no 1"
      And "Peter Alder" adds a complete case study called "no 2"
      And "Peter Alder" adds a complete case study called "no 3"
      And "Peter Alder" adds a complete case study called "no 4"

      Then "Peter Alder" should see all case studies on the FAB Company's Directory Profile page
      And "Peter Alder" should see all case studies on the FAS Company's Directory Profile page


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
    Given "Peter Alder" created an unverified profile for randomly selected company "Y"
    And "Peter Alder" added a complete case study called "no 1"

    When "Peter Alder" updates all the details of case study called "no 1"

    Then "Peter Alder" should see all case studies on the FAB Company's Directory Profile page


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
    Given "Peter Alder" has created and verified profile for randomly selected company "Y"
    And "Peter Alder" added a complete case study called "no 1"

    When "Peter Alder" updates all the details of case study called "no 1"

    Then "Peter Alder" should see all case studies on the FAB Company's Directory Profile page
    And "Peter Alder" should see all case studies on the FAS Company's Directory Profile page


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
    Given "Peter Alder" created an unverified profile for randomly selected company "Y"
    And "Peter Alder" added a complete case study called "no 1"
    And "Peter Alder" added a complete case study called "no 2"
    And "Peter Alder" added a complete case study called "no 3"

    When "Peter Alder" updates all the details of case study called "no 1"
    And "Peter Alder" updates all the details of case study called "no 2"
    And "Peter Alder" updates all the details of case study called "no 3"

    Then "Peter Alder" should see all case studies on the FAB Company's Directory Profile page


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
    Given "Peter Alder" has created and verified profile for randomly selected company "Y"
    And "Peter Alder" added a complete case study called "no 1"
    And "Peter Alder" added a complete case study called "no 2"
    And "Peter Alder" added a complete case study called "no 3"

    When "Peter Alder" updates all the details of case study called "no 1"
    And "Peter Alder" updates all the details of case study called "no 2"
    And "Peter Alder" updates all the details of case study called "no 3"

    Then "Peter Alder" should see all case studies on the FAB Company's Directory Profile page
    And "Peter Alder" should see all case studies on the FAS Company's Directory Profile page
