@fixme
@bug
@TT-1057
@fixed
@multi-user
Feature: Multi-user accounts


  @ED-3554
  @captcha
  @dev-only
  @multi-user
  @add-collaborator
  Scenario Outline: Invited collaborator which "<has or does not have>" a company profile should receive an email with an invitation to collaborate to "<a>" company profile
    Given "Peter Alder" created an "<specific> LTD, PLC or Royal Charter" profile for a random company "Y"
    And "Annette Geissinger" "<has or does not have>" an SSO/great.gov.uk account

    When "Peter Alder" decides to add "Annette Geissinger" as an "editor" collaborator

    Then "Annette Geissinger" should receive an email with a request to confirm that she's been added to company "Y" Find a Buyer profile

    Examples:
      | specific               | has or does not have |
      | unpublished verified   | has                  |
      | unpublished verified   | does not have        |
      | unpublished unverified | has                  |
      | unpublished unverified | does not have        |


  @ED-3555
  @captcha
  @dev-only
  @multi-user
  @add-collaborator
  Scenario: Add "1" collaborator with an SSO/great.gov.uk account to a verified company
    Given "Peter Alder" created a "published LTD, PLC or Royal Charter" profile for a random company "Y"
    And "Annette Geissinger" created a "verified Individual" profile
    And "Peter Alder" added "Annette Geissinger" as an "editor" collaborator
    And "Annette Geissinger" has received an email with a request to confirm that she's been added to company "Y" Find a Buyer profile

    When "Annette Geissinger" confirms that she wants to be added to the company "Y" Find a Buyer profile

    Then "Annette Geissinger" should see "Profile - edit company profile" page


  @ED-3556
  @captcha
  @dev-only
  @multi-user
  @add-collaborator
  Scenario: Add "1" collaborator without an SSO/great.gov.uk account to a verified company
    Given "Peter Alder" created a "published LTD, PLC or Royal Charter" profile for a random company "Y"
    And "Annette Geissinger" "does not have" an SSO/great.gov.uk account
    And "Peter Alder" added "Annette Geissinger" as an "editor" collaborator
    And "Annette Geissinger" has received an email with a request to confirm that she's been added to company "Y" Find a Buyer profile

    When "Annette Geissinger" opens the invitation from company "Y", creates a SSO/great.gov.uk account and confirms that he wants to be added to the FAB profile

    Then "Annette Geissinger" should see "Profile - edit company profile" page


  @ED-3558
  @captcha
  @dev-only
  @multi-user
  @add-collaborator
  Scenario: Invited collaborators should receive an email with an invitation to collaborate
    Given "Peter Alder" created an "unpublished unverified LTD, PLC or Royal Charter" profile for a random company "Y"
    And "Annette Geissinger, Betty Jones, James Weir" "don't have" an SSO/great.gov.uk account

    When "Peter Alder" decides to add "Annette Geissinger, Betty Jones, James Weir" as an "editor" collaborator

    Then "Annette Geissinger, Betty Jones, James Weir" should receive an email with a request to confirm that they've been added to company "Y" Find a Buyer profile


  @ED-3559
  @captcha
  @dev-only
  @multi-user
  @add-collaborator
  Scenario: Add "3" collaborators with an SSO/great.gov.uk account to a verified company
    Given "Peter Alder" created an "unpublished unverified LTD, PLC or Royal Charter" profile for a random company "Y"
    And "Annette Geissinger, Betty Jones, James Weir" "have" an SSO/great.gov.uk account
    And "Peter Alder" added "Annette Geissinger, Betty Jones, James Weir" as an "editor" collaborator
    And "Annette Geissinger, Betty Jones, James Weir" has received an email with a request to confirm that she's been added to company "Y" Find a Buyer profile

    When "Annette Geissinger" confirms that she wants to be added to the company "Y" Find a Buyer profile
    Then "Annette Geissinger" should see "Profile - edit company profile" page

    When "Betty Jones" confirms that she wants to be added to the company "Y" Find a Buyer profile
    Then "Betty Jones" should see "Profile - edit company profile" page

    When "James Weir" confirms that he wants to be added to the company "Y" Find a Buyer profile
    Then "James Weir" should see "Profile - edit company profile" page


  @ED-3560
  @captcha
  @multi-user
  @add-collaborator
  @bug
  @ED-2268
  Scenario: Find a Buyer profile owners should see options to manage account users on SSO - Profile
    Given "Peter Alder" created an "unpublished unverified LTD, PLC or Royal Charter" profile for a random company "Y"

    Then "Peter Alder" should see options to manage Find a Buyer profile users on SSO Profile


  @bug
  @TT-217
  @fixed
  @ED-3560
  @captcha
  @dev-only
  @multi-user
  @add-collaborator
  @bug
  @ED-2268
  Scenario: Collaborators should not be able to add/remove other collaborators or transfer account ownership
    Given "Peter Alder" created an "unpublished unverified LTD, PLC or Royal Charter" profile for a random company "Y"
    And "Annette Geissinger" created a "verified Individual" profile
    And "Peter Alder" added "Annette Geissinger" as an "editor" collaborator
    And "Annette Geissinger" has received an email with a request to confirm that she's been added to company "Y" Find a Buyer profile
    And "Annette Geissinger" confirmed that she wants to be added to the company "Y" Find a Buyer profile

    Then "Annette Geissinger" should not see options to manage Find a Buyer profile users on SSO Profile


  @ED-3561
  @captcha
  @dev-only
  @multi-user
  @transfer-ownership
  Scenario Outline: New Account Owner which "<has or does not have>" a SSO/great.gov.uk account should receive an email with a request for becoming the owner of "<a>" company profile
    Given "Peter Alder" created an "<specific> LTD, PLC or Royal Charter" profile for a random company "Y"
    And "Annette Geissinger" "<has or does not have>" an SSO/great.gov.uk account

    When "Peter Alder" decides to transfer the ownership of company's "Y" Find a Buyer profile to "Annette Geissinger"

    Then "Annette Geissinger" should receive an email with a request for becoming the owner of the company "Y" profile

    Examples:
      | has or does not have | specific               |
      | has                  | unpublished verified   |
      | has                  | unpublished unverified |
      | does not have        | unpublished verified   |
      | does not have        | unpublished unverified |


  @ED-3562
  @multi-user
  @transfer-ownership
  @bug
  @TT-1764
  @fixme
  @bug
  @TT-217
  @fixed
  @bug
  @ED-2268
  @captcha
  @dev-only
  Scenario Outline: Company account owner should be able to transfer the ownership of "<a>" profile to a user who "<has or does not have>" an SSO/great.gov.uk account
    Given "Peter Alder" created an "<specific> LTD, PLC or Royal Charter" profile for a random company "Y"
    And "Annette Geissinger" "<has or does not have>" an SSO/great.gov.uk account

    When "Peter Alder" transfers the ownership of company's "Y" Find a Buyer profile to "Annette Geissinger"

    Then "Annette Geissinger" should see options to manage Find a Buyer profile users on SSO Profile
    And "Peter Alder" should not see options to manage Find a Buyer profile users on SSO Profile

    Examples:
      | specific               | has or does not have |
      | unpublished verified   | has                  |
      | unpublished verified   | does not have        |
      | unpublished unverified | has                  |
      | unpublished unverified | does not have        |


  @ED-3564
  @captcha
  @dev-only
  @multi-user
  @remove-collaborator
  @fake-sso-email-verification
  Scenario: Account owner should be able to remove one account collaborator
    Given "Peter Alder" created an "unpublished unverified LTD, PLC or Royal Charter" profile for a random company "Y"
    And "Annette Geissinger" created a "verified Individual" profile
    And "Peter Alder" added "Annette Geissinger" as an "editor" collaborator
    And "Annette Geissinger" has received an email with a request to confirm that she's been added to company "Y" Find a Buyer profile
    And "Annette Geissinger" confirmed that she wants to be added to the company "Y" Find a Buyer profile

    When "Peter Alder" removes "Annette Geissinger" from the list of collaborators to the company "Y"

    Then "Peter Alder" should not see "Annette Geissinger" among the users associated with company's profile
    And "Annette Geissinger" should not be able to access "Profile - edit company profile" page


  @ED-3565
  @captcha
  @dev-only
  @multi-user
  @remove-collaborator
  @fake-sso-email-verification
  Scenario: Account owner should be able to remove multiple account collaborators
    Given "Peter Alder" created an "unpublished unverified LTD, PLC or Royal Charter" profile for a random company "Y"
    And "Annette Geissinger, Betty Jones, James Weir" "have" an SSO/great.gov.uk account
    And "Peter Alder" added "Annette Geissinger, Betty Jones, James Weir" as an "editor" collaborator
    And "Annette Geissinger" has received an email with a request to confirm that she's been added to company "Y" Find a Buyer profile
    And "Betty Jones" has received an email with a request to confirm that she's been added to company "Y" Find a Buyer profile
    And "James Weir" has received an email with a request to confirm that she's been added to company "Y" Find a Buyer profile
    And "Annette Geissinger" confirmed that she wants to be added to the company "Y" Find a Buyer profile
    And "Betty Jones" confirmed that she wants to be added to the company "Y" Find a Buyer profile
    And "James Weir" confirmed that he wants to be added to the company "Y" Find a Buyer profile

    When "Peter Alder" removes "Annette Geissinger, Betty Jones, James Weir" from the list of collaborators to the company "Y"

    Then "Peter Alder" should not see "Annette Geissinger, Betty Jones, James Weir" among the users associated with company's profile
    And "Annette Geissinger" should not be able to access "Profile - edit company profile" page
    And "Betty Jones" should not be able to access "Profile - edit company profile" page
    And "James Weir" should not be able to access "Profile - edit company profile" page


  @ED-3566
  @captcha
  @dev-only
  @multi-user
  @transfer-ownership
  @verification
  @letter
  @fake-sso-email-verification
  Scenario: Collaborators should be able to set the company description and verify company profile with verification code
    Given "Peter Alder" created an "unpublished unverified LTD, PLC or Royal Charter" profile for a random company "Y"
    And "Annette Geissinger" created a "verified Individual" profile
    And "Peter Alder" added "Annette Geissinger" as an "editor" collaborator
    And "Annette Geissinger" has received an email with a request to confirm that she's been added to company "Y" Find a Buyer profile
    And "Annette Geissinger" confirmed that she wants to be added to the company "Y" Find a Buyer profile
    And "Annette Geissinger" set the company description

    When "Annette Geissinger" verifies the company with the verification code from the letter sent after Directory Profile was created

    Then "Annette Geissinger" should be on "Profile - edit company profile" page
    And "Annette Geissinger" should be told that business profile is ready to be published


  @ED-3567
  @captcha
  @dev-only
  @multi-user
  @add-content
  @fake-sso-email-verification
  Scenario: Account collaborators should be able to update company's details
    Given "Peter Alder" created an "unpublished verified LTD, PLC or Royal Charter" profile for a random company "Y"
    And "Annette Geissinger" created a "verified Individual" profile
    And "Peter Alder" added "Annette Geissinger" as an "editor" collaborator
    And "Annette Geissinger" has received an email with a request to confirm that she's been added to company "Y" Find a Buyer profile
    And "Annette Geissinger" confirmed that she wants to be added to the company "Y" Find a Buyer profile

    When "Annette Geissinger" updates company's details
      | detail                      |
      | trading name                |
      | website                     |
      | keywords                    |
      | number of employees         |
      | sector of interest          |
      | countries to export to      |

    Then "Annette Geissinger" should see new details on "Profile - edit company profile" page
      | detail                      |
      | trading name                |
      | website                     |
      | keywords                    |
      | number of employees         |
      | sector of interest          |
    And "Annette Geissinger" should see new details on "Find a Supplier - Company's business profile" page
      | detail                      |
      | trading name                |
      | website                     |
      | number of employees         |
      | sector of interest          |
#      | keywords                    |  SEE TT-1329


  @bug
  @TT-1537
  @fixed
  @ED-3568
  @captcha
  @dev-only
  @multi-user
  @add-content
  @fake-sso-email-verification
  Scenario Outline: Account collaborators should be able to upload "<valid_image>" as company's logo
    Given "Peter Alder" created an "unpublished verified LTD, PLC or Royal Charter" profile for a random company "Y"
    And "Annette Geissinger" created a "verified Individual" profile
    And "Peter Alder" added "Annette Geissinger" as an "editor" collaborator
    And "Annette Geissinger" has received an email with a request to confirm that she's been added to company "Y" Find a Buyer profile
    And "Annette Geissinger" confirmed that she wants to be added to the company "Y" Find a Buyer profile

    When "Annette Geissinger" uploads "<valid_image>" as company's logo

    Then "Annette Geissinger" should see that logo on FAB Company's Directory Profile page
    And "Annette Geissinger" should see a PNG logo thumbnail on FAS Company's Directory Profile page

    Examples:
      | valid_image            |
      | Anfiteatro_El_Jem.jpeg |


  @ED-3569
  @captcha
  @dev-only
  @multi-user
  @add-content
  @fake-sso-email-verification
  Scenario: Account collaborators should be able to add a case study
    Given "Peter Alder" created an "unpublished verified LTD, PLC or Royal Charter" profile for a random company "Y"
    And "Annette Geissinger" created a "verified Individual" profile
    And "Peter Alder" added "Annette Geissinger" as an "editor" collaborator
    And "Annette Geissinger" has received an email with a request to confirm that she's been added to company "Y" Find a Buyer profile
    And "Annette Geissinger" confirmed that she wants to be added to the company "Y" Find a Buyer profile

    When "Annette Geissinger" adds a complete case study called "no 1"

    Then "Annette Geissinger" should see all case studies on the edit Business Profile page
    And "Annette Geissinger" should see all case studies on the FAS Business Profile page


  @bug
  @TT-1764
  @fixme
  @bug
  @TT-217
  @fixed
  @bug
  @ED-3882
  @fixed
  @ED-3570
  @captcha
  @dev-only
  @multi-user
  @edge-case
  @fake-sso-email-verification
  Scenario: New account owner should be able to transfer it back to the original owner
    Given "Peter Alder" created an "unpublished unverified LTD, PLC or Royal Charter" profile for a random company "Y"
    And "Annette Geissinger" created a "verified Individual" profile

    When "Peter Alder" transfers the ownership of company's "Y" Find a Buyer profile to "Annette Geissinger"
    Then "Annette Geissinger" should see options to manage Find a Buyer profile users on SSO Profile
    And "Peter Alder" should not see options to manage Find a Buyer profile users on SSO Profile

    When "Annette Geissinger" transfers the ownership of company's "Y" Find a Buyer profile to "Peter Alder"
    Then "Peter Alder" should see options to manage Find a Buyer profile users on SSO Profile
    And "Annette Geissinger" should not see options to manage Find a Buyer profile users on SSO Profile


  @bug
  @ED-3882
  @fixme
  @ED-3571
  @captcha
  @dev-only
  @multi-user
  @edge-case
  @fake-sso-email-verification
  Scenario: New account owner should be able to add the original owner as an "editor" collaborator to the company profile
    Given "Peter Alder" created an "unpublished unverified LTD, PLC or Royal Charter" profile for a random company "Y"
    And "Annette Geissinger" created a "verified Individual" profile
    And "Peter Alder" transferred the ownership of company's "Y" Find a Buyer profile to "Annette Geissinger"

    When "Annette Geissinger" decides to add "Peter Alder" as an "editor" collaborator
    When "Peter Alder" confirms that he wants to be added to the company "Y" Find a Buyer profile

    Then "Peter Alder" should see "Profile - edit company profile" page


  @bug
  @ED-3852
  @fixme
  @ED-3572
  @captcha
  @dev-only
  @multi-user
  @edge-case
  @fake-sso-email-verification
  Scenario: Suppliers should not be able to add collaborators which already have a Find a Buyer profile
    Given "Peter Alder" created an "unpublished unverified LTD, PLC or Royal Charter" profile for a random company "Alpha"
    And "Annette Geissinger" created an "unpublished unverified LTD, PLC or Royal Charter" profile for a random company "Omega"

    When "Peter Alder" decides to add "Annette Geissinger" as an "editor" collaborator

    Then "Peter Alder" should see "Can't add this user" message
