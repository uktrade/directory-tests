Feature: Trade Profile


    @ED-1659
    @registration
    Scenario Outline: Supplier should receive a verification email after successful registration - export status is "<current>"
      Given "Peter Alder" is an unauthenticated supplier

      When "Peter Alder" randomly selects an active company without a Directory Profile identified by an alias "Company X"
      And "Peter Alder" confirms that "Company X" is the correct one
      And "Peter Alder" confirms that the export status is "<current>"
      And "Peter Alder" creates a SSO/great.gov.uk account for "Company X" using valid credentials

      Then "Peter Alder" should be told about the verification email
      And "Peter Alder" should receive an email verification msg entitled "Your great.gov.uk account: Please Confirm Your E-mail Address"

      Examples:
        | current                        |
        | Yes, in the last year          |
        | Yes, 1 to 2 years ago          |
        | Yes, but more than 2 years ago |
        | No, but we are preparing to    |


    @ED-1692
    @verification
    @email
    Scenario: Unauthenticated Suppliers should be able to verify their email address via confirmation link sent in an email
      Given "Annette Geissinger" is an unauthenticated supplier
      And "Annette Geissinger" created a SSO/great.gov.uk account associated with randomly selected company "Company X"
      And "Annette Geissinger" received the email verification message with the email confirmation link

      When "Annette Geissinger" decides to confirm her email address by using the email confirmation link
      And "Annette Geissinger" confirms the email address

      Then "Annette Geissinger" should be prompted to build and improve your Directory Profile


    @ED-1757
    @verification
    @login
    Scenario: Suppliers without verified email should be told to verify the email address first before being able to log in
      Given "Annette Geissinger" is an unauthenticated supplier
      And "Annette Geissinger" created a SSO/great.gov.uk account associated with randomly selected company "Company X"

      When "Annette Geissinger" attempts to sign in to Find a Buyer profile

      Then "Annette Geissinger" should be told that she needs to verify her email address first


    @ED-1716
    @profile
    Scenario: Supplier should be able to build the Directory Profile once the email address is confirmed
      Given "Annette Geissinger" is an unauthenticated supplier
      And "Annette Geissinger" created a SSO/great.gov.uk account associated with randomly selected company "Company X"
      And "Annette Geissinger" confirmed her email address

      When "Annette Geissinger" provides valid details of selected company
      And "Annette Geissinger" selects random sector the company is interested in working in
      And "Annette Geissinger" provides her full name which will be used to sent the verification letter
      And "Annette Geissinger" confirms the details which will be used to sent the verification letter

      Then "Annette Geissinger" should be on edit Company's Directory Profile page
      And "Annette Geissinger" should be told that her company has no description


    @ED-1722
    @verification
    @letter
    Scenario: Supplier should be able to verify company using code sent in the verification letter
      Given "Annette Geissinger" is an unauthenticated supplier
      And "Annette Geissinger" created a SSO/great.gov.uk account associated with randomly selected company "Company X"
      And "Annette Geissinger" confirmed her email address
      And "Annette Geissinger" built the company profile
      And "Annette Geissinger" set the company description

      When "Annette Geissinger" verifies the company with the verification code from the letter sent after Directory Profile was created

      Then "Annette Geissinger" should be on edit Company's Directory Profile page
      And "Annette Geissinger" should be told that her company is published


    @ED-1727
    @publish
    @FAS
    Scenario: Once verified Company's Directory Profile should be published on FAS
      Given "Peter Alder" has created and verified profile for randomly selected company "Y"

      When "Peter Alder" decides to view published Directory Profile

      Then "Peter Alder" should be on FAS Directory Profile page of company "Y"


    @ED-1740
    @registration
    Scenario: Some suppliers are not appropriate to feature in the Find a Buyer service
      Given "Peter Alder" is an unauthenticated supplier

      When "Peter Alder" randomly selects an active company without a Directory Profile identified by an alias "Company X"
      And "Peter Alder" confirms that "Company X" is the correct one
      And "Peter Alder" decides that the export status of his company is "No, we are not planning to sell overseas"

      Then "Peter Alder" should be told that his company is currently not appropriate to feature in the FAB service


    @ED-1769
    @login
    @fab
    Scenario: Suppliers with unverified company profile should be able to logout and log back in
      Given "Annette Geissinger" is an unauthenticated supplier
      And "Annette Geissinger" created a SSO/great.gov.uk account associated with randomly selected company "Company X"
      And "Annette Geissinger" confirmed her email address
      And "Annette Geissinger" signed out from Find a Buyer service

      When "Annette Geissinger" signs in to Find a Buyer profile

      Then "Annette Geissinger" should be on edit Company's Directory Profile page
      And "Annette Geissinger" should be told that her company has no description


    @ED-1770
    @sso
    @fab
    @account
    Scenario Outline: Suppliers with a standalone SSO/great.gov.uk account should be able to select their company for Directory Profile creation
      Given "Peter Alder" has a verified standalone SSO/great.gov.uk account
      And "Peter Alder" is signed in to SSO/great.gov.uk account

      When "Peter Alder" decides to create a trade profile
      And "Peter Alder" randomly selects an active company without a Directory Profile identified by an alias "Company X"
      And "Peter Alder" confirms that "Company X" is the correct one
      And "Peter Alder" confirms that the export status is "<current>"

      Then "Peter Alder" should be prompted to build and improve your Directory Profile

      Examples:
        | current                        |
        | Yes, in the last year          |
        | Yes, 1 to 2 years ago          |
        | Yes, but more than 2 years ago |
        | No, but we are preparing to    |


    @ED-1770
    @sso
    @fab
    @account
    Scenario: Suppliers with a standalone SSO/great.gov.uk account should be able to create a Directory profile
      Given "Peter Alder" has a verified standalone SSO/great.gov.uk account
      And "Peter Alder" is signed in to SSO/great.gov.uk account
      And "Peter Alder" selected an active company without a Directory Profile identified by an alias "Company X"

      When "Peter Alder" provides valid details of selected company
      And "Peter Alder" selects random sector the company is interested in working in
      And "Peter Alder" provides her full name which will be used to sent the verification letter
      And "Peter Alder" confirms the details which will be used to sent the verification letter

      Then "Peter Alder" should be on edit Company's Directory Profile page
      And "Peter Alder" should be told that her company has no description


    @ED-1758
    @fab
    @login
    Scenario: Suppliers with verified company profile should be able to logout and log back in
      Given "Peter Alder" has created and verified profile for randomly selected company "Y"
      And "Peter Alder" signed out from Find a Buyer service

      When "Peter Alder" signs in to Find a Buyer profile

      Then "Peter Alder" should be on edit Company's Directory Profile page
      And "Peter Alder" should be told that her company is published


    @ED-1760
    @fab
    @profile
    Scenario: Supplier should be able to update company's details
      Given "Annette Geissinger" has created and verified profile for randomly selected company "Y"

      When "Annette Geissinger" updates company's details
        | detail                      |
        | business name               |
        | website                     |
        | keywords                    |
        | number of employees         |
        | sector of interest          |

      Then "Annette Geissinger" should see new details on FAB Company's Directory Profile page
        | detail                      |
        | business name               |
        | website                     |
        | keywords                    |
        | number of employees         |
        | sector of interest          |


    @ED-1759
    @profile
    @logo
    Scenario Outline: Supplier should be able to upload an image to set company's logo
      Given "Peter Alder" has created and verified profile for randomly selected company "Y"

      When "Peter Alder" uploads "<valid_image>" as company's logo

      Then "Peter Alder" should see that logo on FAB Company's Directory Profile page
      And "Peter Alder" should see that logo on FAS Company's Directory Profile page

      Examples:
        | valid_image              |
        | Anfiteatro_El_Jem.jpeg   |
        | Kobe_Port_Tower.jpg      |
        | Wikipedia-logo-v2-en.png |


    @ED-1759
    @profile
    @logo
    Scenario Outline: Supplier should be able to replace an existing company's logo with a new one
      Given "Peter Alder" has created and verified profile for randomly selected company "Y"
      And "Peter Alder" has set "<original>" picture as company's logo
      And "Peter Alder" can see that logo on FAB Company's Directory Profile page

      When "Peter Alder" uploads "<new_picture>" as company's logo

      Then "Peter Alder" should see that logo on FAB Company's Directory Profile page
      And "Peter Alder" should see that logo on FAS Company's Directory Profile page

      Examples:
        | original               | new_picture         |
        | Anfiteatro_El_Jem.jpeg | Kobe_Port_Tower.jpg |


    @ED-1759
    @profile
    @logo
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
    @bug
    @ED-1833
    @fixme
    Scenario: Supplier should NOT be able to use invalid links to Online Profiles (social media URLs)
      Given "Peter Alder" has created and verified profile for randomly selected company "Y"

      When "Peter Alder" attempts to use invalid links to online profiles
        | online profile  |
        | Facebook        |
        | LinkedIn        |
        | Twitter         |

      Then "Peter Alder" should be told to provide valid links to all online profiles
