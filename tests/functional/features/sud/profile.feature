Feature: SUD (Profile) pages


  @ED-2265
  @sso
  @account
  @no-sso-email-verification-required
  Scenario: Users should be able to view SUD Landing page without authentication
    Given "Peter Alder" is an unauthenticated supplier

    When "Peter Alder" goes to "SUD Landing" page

    Then "Peter Alder" should see "SUD Landing" page


  @ED-2266
  @sso
  @account
  @no-sso-email-verification-required
  Scenario Outline: Users who visited SUD landing page should not be able to view "<other SUD>" page without authentication
    Given "Peter Alder" is an unauthenticated supplier

    When "Peter Alder" goes to "SUD Landing" page
    And "Peter Alder" goes to "<other SUD>" page

    Then "Peter Alder" should see "<expected>" page

    Examples: SUD pages
      |other SUD                  | expected        |
      |SUD Export Opportunities   | SSO Login       |
      |Profile - Find a Buyer     | Profile - Enrol |
      |SUD Selling Online Overseas| SSO Login       |


  @ED-2266
  @sso
  @account
  @bug
  @ED-2268
  @fixed
  @no-sso-email-verification-required
  Scenario Outline: Users who visit "<SUD>" page for the first time should be redirected to SSO Login page
    Given "Peter Alder" is an unauthenticated supplier

    When "Peter Alder" goes to "<SUD>" page

    Then "Peter Alder" should see "<expected>" page

    Examples: SUD pages
      |SUD                        | expected        |
      |SUD Export Opportunities   | SSO Login       |
      |profile - Find a Buyer     | Profile - Enrol |
      |SUD Selling Online Overseas| SSO Login       |


  # I've been told that on non-prod envs ExOpps doesn't keep synced state
  # between different services and thus ExOpps page on SUD displays
  # different content based on user ID
  @ED-2267
  @sso
  @account
  @fake-sso-email-verification
  Scenario: Authenticated Users should be able to view SUD sub-pages
    Given "Peter Alder" has a verified standalone SSO/great.gov.uk account

    When "Peter Alder" goes to specific pages
      |page name                  |
      |SUD Export Opportunities   |
      |Profile - Find a Buyer     |
      |SUD Selling Online Overseas|

    Then "Peter Alder" should be able to see all selected pages


  @ED-2141
  @profile
  @dev-only
  @fake-sso-email-verification
  Scenario: Supplier should not be able to update business details using invalid values
    Given "Annette Geissinger" created an unverified business profile for randomly selected company "Company X"

    When "Annette Geissinger" attempts to change business details
      | trading name   | website         | size       | industry | error                  |
      | empty string   | empty string    | 1-10       | random   | This field is required |
      | unchanged      | invalid http    | 11-50      | random   | Enter a valid URL      |
      | unchanged      | invalid https   | 51-200     | random   | Enter a valid URL      |
      | unchanged      | 2048 characters | 201-500    | random   | Enter a valid URL      |
      | unchanged      | empty string    | unset      | random   | This field is required |
      | unchanged      | empty string    | 501-1000   | unset    | This field is required |
      | unchanged      | empty string    | 1001-10000 | unset    | This field is required |

    Then "Annette Geissinger" should see expected error messages


  @bug
  @TT-1289
  @fixme
  @ED-2141
  @profile
  @dev-only
  @fake-sso-email-verification
  Scenario: Supplier should not be able to update business details using invalid values (too long name)
    Given "Annette Geissinger" created an unverified business profile for randomly selected company "Company X"

    When "Annette Geissinger" attempts to change business details
      | trading name   | website         | size       | industry | error                  |
      | 256 characters | empty string    | 10001+     | random   | Ensure this field has no more than 255 characters |

    Then "Annette Geissinger" should see expected error messages


  @ED-2141
  @profile
  @dev-only
  @fake-sso-email-verification
  Scenario: Supplier should not be able to use other characters than alphanumerics and commas to define products and services offered by the company
    Given "Annette Geissinger" created an unverified business profile for randomly selected company "Company X"

    When "Annette Geissinger" attempts to change products and services offered by the company
      | keywords          | separator  | error                                                       |
      | empty string      | comma      | This field is required                                      |
      | book, keys, food  | pipe       | You can only enter letters, numbers and commas              |
      | sky, sea, blues   | semi-colon | You can only enter letters, numbers and commas              |
      | sand, dunes, bird | colon      | You can only enter letters, numbers and commas              |
      | bus, ferry, plane | full stop  | You can only enter letters, numbers and commas              |
      | 1001 characters   | comma      | Ensure this value has at most 1000 characters (it has 1001) |

    Then "Annette Geissinger" should see expected error messages


  @ED-1727
  @publish
  @FAS
  @dev-only
  @fake-sso-email-verification
  Scenario: Once verified Company's Business Profile should be published on FAS
    Given "Peter Alder" has created verified and published business profile for randomly selected company "Y"

    When "Peter Alder" decides to view published Business Profile

    Then "Peter Alder" should be on "Y"'s FAS Business Profile page


  @ED-1769
  @login
  @fab
  @dev-only
  @fake-sso-email-verification
  Scenario: Suppliers with unverified company profile should be able to logout and log back in
    Given "Annette Geissinger" created an unverified business profile for randomly selected company "Company X"
    And "Annette Geissinger" signed out from SSO/great.gov.uk account

    When "Annette Geissinger" signs in to SSO/great.gov.uk account from "FAB Landing"

    Then "Annette Geissinger" should be on "Profile - edit company profile" page


  @ED-1758
  @fab
  @login
  @dev-only
  @fake-sso-email-verification
  Scenario: Suppliers with verified company profile should be able to logout and log back in
    Given "Peter Alder" has created verified and published business profile for randomly selected company "Y"
    And "Peter Alder" signed out from SSO/great.gov.uk account

    When "Peter Alder" signs in to SSO/great.gov.uk account from "FAB Landing"

    Then "Peter Alder" should be on "Profile - edit company profile" page


  @ED-1760
  @ED-1766
  @fab
  @bug
  @ED-3151
  @fixed
  @profile
  @fake-sso-email-verification
  Scenario: Supplier should be able to update company's details
    Given "Annette Geissinger" has created verified and published business profile for randomly selected company "Y"

    When "Annette Geissinger" updates company's details
      | detail                      |
      | trading name                |
      | website                     |
      | number of employees         |
      | sector of interest          |
      | keywords                    |

    Then "Annette Geissinger" should see new details on "Profile - edit company profile" page
      | detail                      |
      | trading name                |
      | website                     |
      | number of employees         |
      | sector of interest          |
      | keywords                    |
    And "Annette Geissinger" should see new details on "FAS - company profile" page
      | detail                      |
      | trading name                |
      | website                     |
      | number of employees         |
      | sector of interest          |
      | keywords                    |


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
