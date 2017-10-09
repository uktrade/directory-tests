Feature: Export Preferences


  @ED-1952
  @profile
  @export-preferences
  Scenario Outline: Suppliers can select preferred countries of export from the given list and provide a list of other countries
    Given "Annette Geissinger" is an unauthenticated supplier
    And "Annette Geissinger" created a SSO/great.gov.uk account associated with randomly selected company "Company X"
    And "Annette Geissinger" confirmed her email address

    When "Annette Geissinger" provides valid details of selected company
    And "Annette Geissinger" selects sector the company is in and "<preferred>" & "<other>" countries of export

    Then "Annette Geissinger" should be asked to decide how to verify her identity

    Examples:
      | preferred                                   | other                 |
      | China, Germany, India, Japan, United States | empty string          |
      | China, Germany, India, Japan, United States | Canada, Poland, Italy |


  @ED-1952b
  @profile
  @export-preferences
  Scenario Outline: Suppliers have to provide preferred country of export when building up the profile
    Given "Annette Geissinger" is an unauthenticated supplier
    And "Annette Geissinger" created a SSO/great.gov.uk account associated with randomly selected company "Company X"
    And "Annette Geissinger" confirmed her email address

    When "Annette Geissinger" provides valid details of selected company
    And "Annette Geissinger" selects sector the company is in and "<preferred>" & "<other>" countries of export

    Then "Annette Geissinger" should see "<error>" message

    Examples:
      | preferred     | other           | error                                                        |
      | China         | 1001 characters | Ensure this value has at most 1000 characters (it has 1001). |
      | none selected | empty string    | This field is required.                                      |


  @wip
  @ED-1952c
  @profile
  @export-preferences
  Scenario Outline: Suppliers have to use commas to separate other preferred countries of export when building up the profile
    Given "Annette Geissinger" is an unauthenticated supplier
    And "Annette Geissinger" created a SSO/great.gov.uk account associated with randomly selected company "Company X"
    And "Annette Geissinger" confirmed her email address

    When "Annette Geissinger" provides valid details of selected company
    And "Annette Geissinger" selects sector the company is in and "<preferred>" & "<other>" countries of export

    Then "Annette Geissinger" should see "<error>" message

    Examples:
      | preferred     | other                 | error                   |
      | none selected | Canada; Poland; Italy | Enter 3 maximum         |
      | none selected | Canada.Poland.Italy   | Enter 3 maximum         |

