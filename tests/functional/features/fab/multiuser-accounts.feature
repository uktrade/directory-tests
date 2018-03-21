@multi-user
Feature: Multi-user accounts


  @ED-3554
  @multi-user
  @add-collaborator
  Scenario Outline: Invited collaborator should receive an email with an invitation to collaborate to "<a>" company profile
    Given "Peter Alder" has created "<a>" profile for randomly selected company "Y"
    And "Annette Geissinger" "<has or does not have>" an SSO/great.gov.uk account

    When "Peter Alder" decides to add "Annette Geissinger" as a collaborator

    Then "Annette Geissinger" should receive an email with a request to confirm that she's been added to company "Y" Find a Buyer profile

    Examples:
      | a             | has or does not have |
      | a verified    | has                  |
      | a verified    | does not have        |
      | an unverified | has                  |
      | an unverified | does not have        |


  @ED-3555
  @multi-user
  @add-collaborator
  Scenario: Add "1" collaborator with an SSO/great.gov.uk account to a verified company
    Given "Peter Alder" has created and verified profile for randomly selected company "Y"
    And "Annette Geissinger" has a verified standalone SSO/great.gov.uk account
    And "Annette Geissinger" is signed in to SSO/great.gov.uk account
    And "Peter Alder" added "Annette Geissinger" as a collaborator
    And "Annette Geissinger" has received an email with a request to confirm that she's been added to company "Y" Find a Buyer profile

    When "Annette Geissinger" confirms that she wants to be added to the company "Y" Find a Buyer profile

    Then "Annette Geissinger" should see "FAB Company profile" page


  @ED-3556
  @multi-user
  @add-collaborator
  Scenario: Add "1" collaborator without an SSO/great.gov.uk account to a verified company
    Given "Peter Alder" has created and verified profile for randomly selected company "Y"
    And "Annette Geissinger" "does not have" an SSO/great.gov.uk account
    And "Peter Alder" added "Annette Geissinger" as a collaborator
    And "Annette Geissinger" has received an email with a request to confirm that she's been added to company "Y" Find a Buyer profile

    When "Annette Geissinger" opens the invitation from company "Y", creates a SSO/great.gov.uk account and confirms that he wants to be added to the FAB profile

    Then "Annette Geissinger" should see "FAB Company profile" page


  @ED-3557
  @multi-user
  @add-collaborator
  Scenario: Add "1" collaborator with an SSO/great.gov.uk account to a verified company
    Given "Peter Alder" has created and verified profile for randomly selected company "Y"
    And "Annette Geissinger" "has" an SSO/great.gov.uk account
    And "Peter Alder" added "Annette Geissinger" as a collaborator
    And "Annette Geissinger" has received an email with a request to confirm that she's been added to company "Y" Find a Buyer profile
    And "Annette Geissinger" decides to open the invitation from company "Y"
    And "Annette Geissinger" should be on "FAB confirm you want to be added to the profile" page

    When "Annette Geissinger" confirms that she wants to be added to the company "Y" Find a Buyer profile

    Then "Annette Geissinger" should see "FAB Company profile" page


  @ED-3558
  @multi-user
  @add-collaborator
  Scenario: Invited collaborators should receive an email with an invitation to collaborate
    Given "Peter Alder" has created "an unverified" profile for randomly selected company "Y"
    And "Annette Geissinger, Betty Jones, James Weir" "don't have" an SSO/great.gov.uk account

    When "Peter Alder" decides to add "Annette Geissinger, Betty Jones, James Weir" as a collaborator

    Then "Annette Geissinger, Betty Jones, James Weir" should receive an email with a request to confirm that they've been added to company "Y" Find a Buyer profile


  @wip
  @ED-3559
  @multi-user
  @add-collaborator
  Scenario: Add "3" collaborators with an SSO/great.gov.uk account to a verified company
    Given "Peter Alder" has created an unverified profile for randomly selected company "Y"
    And "Annette Geissinger" has a verified standalone SSO/great.gov.uk account
    And "Betty Jones" has a verified standalone SSO/great.gov.uk account
    And "James Weir" has a verified standalone SSO/great.gov.uk account
    And "Peter Alder" added "Annette Geissinger, Betty Jones, James Weir" as collaborators to company "Y"

    When "Annette Geissinger" confirms that she wants to be added as a collaborator
    And "Betty Jones" confirms that she wants to be added as a collaborator
    And "James Weir" confirms that he wants to be added as a collaborator

    Then "Annette Geissinger" should be on "Edit Company profile" page
    And "Betty Jones" should be on "Edit Company profile" page
    And "James Weir" should be on "Edit Company profile" page


  @wip
  @ED-3560
  @multi-user
  @add-collaborator
  Scenario: Collaborators should not be able to add/remove other collaborators or transfer account ownership
    Given "Peter Alder" has created an unverified profile for randomly selected company "Y"
    And "Peter Alder" added "Annette Geissinger" as a collaborator to company "Y"
    And "Annette Geissinger" is signed in to SSO/great.gov.uk account

    When "Annette Geissinger" goes to the SSO "Find a buyer" tab

    Then "Annette Geissinger" should not see options to manage account users on "SSO - Find a buyer" page


  @wip
  @ED-3561
  @multi-user
  @transfer-ownership
  Scenario Outline: New Account Owner should receive an email with a request to confirm account ownership
    Given "Peter Alder" has created "<a>" profile for randomly selected company "Y"
    And "Annette Geissinger" "<has or does not have>" a SSO/great.gov.uk account

    When "Peter Alder" decides to transfer the company "Y" account ownership to "Annette Geissinger"
    And "Peter Alder" confirms his password before transferring the ownership

    Then "Annette" should receive an email with a request for becoming the owner of the company "Y" profile

    Examples:
      | has or does not have | a             |
      | has                  | a verified    |
      | has                  | an unverified |
      | does not have        | a verified    |
      | does not have        | an unverified |


  @wip
  @ED-3562
  @multi-user
  @transfer-ownership
  Scenario Outline: Company account owner should be able to transfer the account ownership to a user who "has or does not have" an SSO/great.gov.uk account
    Given "Peter Alder" has created "<a>" profile for randomly selected company "Y"
    And "Annette Geissinger" "<has or does not have>" a SSO/great.gov.uk account

    When "Peter Alder" transfers the company "Y" account ownership to "Annette Geissinger"
    And "Annette Geissinger" accepts the request for becoming the owner of company "Y" profile

    Then "Annette Geissinger" should see options to manage account users on "SSO - Find a buyer" page
    And "Peter Alder" should not see options to manage account users on "SSO - Find a buyer" page

    Examples:
      | has or does not have | a             |
      | has                  | a verified    |
      | has                  | an unverified |
      | does not have        | a verified    |
      | does not have        | an unverified |


  @wip
  @ED-3564
  @multi-user
  @remove-collaborator
  @fake-sso-email-verification
  Scenario: Account owner should be able to remove one account collaborator
    Given "Peter Alder" has created an unverified profile for randomly selected company "Y"
    And "Peter Alder" added "Annette Geissinger" as a collaborator to company "Y"
    And "Annette Geissinger" accepted request for becoming a collaborator to company "Y"

    When "Peter Alder" removes "Annette Geissinger" from the list of collaborators to the company "Y"

    Then "Peter Alder" should not see "Annette Geissinger" on the list of collaborators to the company "Y"
    And "Annette Geissinger" should not be able to access "Edit profile" page


  @wip
  @ED-3565
  @multi-user
  @remove-collaborator
  @fake-sso-email-verification
  Scenario: Account owner should be able to remove multiple account collaborators
    Given "Peter Alder" has created a unverified profile for randomly selected company "Y"
    And "Peter Alder" added "Annette Geissinger, Betty Jones, James Weir" as collaborators to company "Y"
    And "Annette Geissinger, Betty Jones, James Weir" accepted request for becoming a collaborator to company "Y"

    When "Peter Alder" removes "Annette Geissinger, Betty Jones, James Weir" from the list of collaborators to the company "Y"

    Then "Peter Alder" should not see "Annette Geissinger, Betty Jones, James Weir" on the list of collaborators to the company "Y"
    And "Annette Geissinger" should not be able to access "Edit profile" page
    And "Betty Jones" should not be able to access "Edit profile" page
    And "James Weir" should not be able to access "Edit profile" page


  @wip
  @ED-3566
  @multi-user
  @transfer-ownership
  @verification
  @letter
  @fake-sso-email-verification
  Scenario: Collaborators should be able to verify company profile with verification code
    Given "Peter Alder" has created an unverified profile for randomly selected company "Y"
    And "Peter Alder" added "Annette Geissinger" as a collaborator to company "Y"
    And "Annette Geissinger" accepted request for becoming a collaborator to company "Y"

    When "Annette Geissinger" verifies the company with the verification code from the letter sent after Directory Profile was created

    Then "Annette Geissinger" should be on edit Company's Directory Profile page
    And "Annette Geissinger" should be told that her company is published


  @wip
  @ED-3567
  @multi-user
  @add-content
  @fake-sso-email-verification
  Scenario: Account collaborators should be able to update company's details
    Given "Peter Alder" has created a verified profile for randomly selected company "Y"
    And "Peter Alder" added "Annette Geissinger" as a collaborator to company "Y"
    And "Annette Geissinger" accepted request for becoming a collaborator to company "Y"

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


  @wip
  @ED-3568
  @multi-user
  @add-content
  @fake-sso-email-verification
  Scenario Outline: Account collaborators should be able to upload company's logo
    Given "Peter Alder" has created a verified profile for randomly selected company "Y"
    And "Peter Alder" added "Annette Geissinger" as a collaborator to company "Y"
    And "Annette Geissinger" accepted request for becoming a collaborator to company "Y"

    When "Annette Geissinger" uploads "<valid_image>" as company's logo

    Then "Annette Geissinger" should see that logo on FAB Company's Directory Profile page
    And "Annette Geissinger" should see a PNG logo thumbnail on FAS Company's Directory Profile page

    Examples:
      | valid_image            |
      | Anfiteatro_El_Jem.jpeg |


  @wip
  @ED-3569
  @multi-user
  @add-content
  @fake-sso-email-verification
  Scenario: Account collaborators should be able to add a case study
    Given "Peter Alder" has created a verified profile for randomly selected company "Y"
    And "Peter Alder" added "Annette Geissinger" as a collaborator to company "Y"
    And "Annette Geissinger" accepted request for becoming a collaborator to company "Y"

    When "Annette Geissinger" adds a complete case study called "no 1"

    Then "Annette Geissinger" should see all case studies on the FAB Company's Directory Profile page
    And "Annette Geissinger" should see all case studies on the FAS Company's Directory Profile page


  @wip
  @ED-3570
  @multi-user
  @edge-case
  @fake-sso-email-verification
  Scenario: New account owner should be able to transfer it back to the original owner
    Given "Peter Alder" has created an unverified profile for randomly selected company "Y"
    And "Peter Alder" transferred the company "Y" account ownership to "Annette Geissinger"
    And "Annette Geissinger" accepted request for becoming the owner of company "Y" profile

    When "Annette Geissinger" transfers the company "Y" account ownership to "Peter Alder"
    And "Peter Alder" accepts the request for becoming the owner of company "Y" profile

    Then "Peter Alder" should see options to manage account users on "SSO - Find a buyer" page
    And "Annette Geissinger" should not see options to manage account users on "SSO - Find a buyer" page


  @wip
  @ED-3571
  @multi-user
  @edge-case
  @fake-sso-email-verification
  Scenario: New account owner should be able to add the original owner as a collaborator to the company profile
    Given "Peter Alder" has created an unverified profile for randomly selected company "Y"
    And "Peter Alder" transferred the company "Y" account ownership to "Annette Geissinger"
    And "Annette Geissinger" accepted request for becoming the owner of company "Y" profile

    When "Annette Geissinger" adds "Peter Alder" as a collaborator
    And "Peter Alder" confirms that he wants to become a collaborator to company "Y" profile

    Then "Peter Alder" should be on "Edit Company profile" page


  @wip
  @ED-3572
  @multi-user
  @edge-case
  @fake-sso-email-verification
  Scenario: Supplier should receive an email with a request for becoming a collaborator despite already having a profile
    Given "Peter Alder" has created an unverified profile for randomly selected company "Y"
    And "Annette Geissinger" has created an unverified profile for randomly selected company "Z"

    When "Peter Alder" decides to add "Annette Geissinger" as a collaborator

    Then "Annette" should receive an email with a request for becoming a collaborator to company "Y" profile


  @wip
  @ED-3573
  @multi-user
  @edge-case
  @fake-sso-email-verification
  Scenario: Adding Collaborator which is already an owner of a different profile shouldn't work
    Given "Peter Alder" has created an unverified profile for randomly selected company "Y"
    And "Annette Geissinger" has created an unverified profile for randomly selected company "Z"
    And "Peter Alder" added "Annette Geissinger" as a collaborator
    And "Annette Geissinger" has received an email with a request for becoming a collaborator to company "Y" profile

    When "Annette Geissinger" confirms that she wants to become a collaborator to company "Y" profile

    Then "Annette Geissinger" should be on "Edit Company profile" page
