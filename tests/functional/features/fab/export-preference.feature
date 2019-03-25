Feature: Export Preferences


  @deprecated
  @ED-1952
  @profile
  @export-preferences
  @fake-sso-email-verification
  Scenario Outline: Suppliers can select preferred countries of export from the given list and provide a list of other countries
    Given "Annette Geissinger" created an unverified business profile for randomly selected company "Y"

    When "Annette Geissinger" provides valid details of selected company
    And "Annette Geissinger" selects sector the company is in and "<preferred>" & "<other>" as other countries of export

    Then "Annette Geissinger" should be asked to decide how to verify her identity

    Examples:
      | preferred              | other                 |
      | 3 predefined countries | empty string          |
      | 5 predefined countries | Canada, Poland, Italy |


  @deprecated
  @ED-1952
  @profile
  @export-preferences
  @fake-sso-email-verification
  Scenario Outline: Suppliers have to provide preferred country of export when building up the profile
    Given "Annette Geissinger" created an unverified business profile for randomly selected company "Company X"

    When "Annette Geissinger" provides valid details of selected company
    And "Annette Geissinger" selects sector the company is in and "<preferred>" & "<other>" as other countries of export

    Then "Annette Geissinger" should see "<error>" message

    Examples:
      | preferred            | other           | error                                                        |
      | 1 predefined country | 1001 characters | Ensure this value has at most 1000 characters (it has 1001). |
      | none selected        | empty string    | This field is required.                                      |


  @deprecated
  @ED-1952
  @profile
  @export-preferences
  @bug
  @ED-2313
  @fixme
  @fake-sso-email-verification
  Scenario Outline: Suppliers have to use commas to separate other preferred countries of export when building up the profile
    Given "Annette Geissinger" created an unverified business profile for randomly selected company "Company X"

    When "Annette Geissinger" provides valid details of selected company
    And "Annette Geissinger" selects sector the company is in and "<preferred>" & "<other>" as other countries of export

    Then "Annette Geissinger" should see "<error>" message

    Examples:
      | preferred     | other                 | error                                  |
      | none selected | Canada; Poland; Italy | You can only enter letters and commas. |
      | none selected | Canada.Poland.Italy   | You can only enter letters and commas. |
