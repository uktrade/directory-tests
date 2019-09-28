Feature: Trade Profile


  @ED-2094
  @profile
  @verification
  @letter
  @captcha
  @dev-only
  @fake-sso-email-verification
  Scenario: Logged-in Supplier should be able to verify profile by using code and link from the letter
    Given "Annette Geissinger" created an unverified "LTD, PLC or Royal Charter" profile for randomly selected company "Company X"
    And "Annette Geissinger" set the company description
    And "Annette Geissinger" decided to verify her identity with a verification letter
    And "Annette Geissinger" received the letter with verification code

    When "Annette Geissinger" goes to the verification link from the letter as authenticated user
    And "Annette Geissinger" submits the verification code

    Then "Annette Geissinger" should be told that company has been verified

    When "Annette Geissinger" goes to "Profile - Business Profile" page
    Then "Annette Geissinger" should be told that business profile is ready to be published


  @ED-2094
  @profile
  @verification
  @letter
  @captcha
  @dev-only
  @fake-sso-email-verification
  Scenario: Logged-out Supplier should be able to verify profile by using code and link from the letter
    Given "Annette Geissinger" created an unverified "LTD, PLC or Royal Charter" profile for randomly selected company "Company X"
    And "Annette Geissinger" set the company description
    And "Annette Geissinger" decided to verify her identity with a verification letter
    And "Annette Geissinger" signed out from SSO/great.gov.uk account
    And "Annette Geissinger" received the letter with verification code

    When "Annette Geissinger" goes to the verification link from the letter as unauthenticated user
    And "Annette Geissinger" submits the verification code

    Then "Annette Geissinger" should be told that company has been verified

    When "Annette Geissinger" goes to "Profile - Business Profile" page
    Then "Annette Geissinger" should be told that business profile is ready to be published


  @overseas-company
  @profile
  Scenario: Users can't create profile for an "Overseas company"
    Given "Annette" decided to create an "Overseas company" profile for a random company "X"
    Then "Annette" should be on "Profile - Overseas business cannot create an account" page


  @wip
  @profile
  @individual
  @captcha
  @dev-only
  @fake-sso-email-verification
  Scenario Outline: Individuals should not see any business details on their Profile page
    Given "Annette" created an "<trade>" profile for a random company "X"

    When "Annette" goes to "Profile - Business Profile" page

    Then "Annette" should see "Create business profile" on the page

    Examples: business types
      | trade                 |
      | verified Individual   |
      | unverified Individual |


  @wip
  @profile
  @verification
  @letter
  @captcha
  @dev-only
  @fake-sso-email-verification
  Scenario Outline: Users should see "<expected business classification>" for their "<trade>" profile on "Profile - Business Profile" page
    Given "Annette" created an "<trade>" profile for a random company "X"

    When "Annette" goes to "Profile - Business Profile" page

    Then "Annette" should see "<expected business classification>" on the page

    Examples: business types
      | trade                                                                      | expected business classification              |
      | unpublished unverified LTD, PLC or Royal Charter                           | UK business registered in Companies House     |
      | unpublished unverified Sole trader                                         | UK business not registered in Companies House |
      | unpublished unverified Charity                                             | UK business not registered in Companies House |
      | unpublished unverified Partnership                                         | UK business not registered in Companies House |
      | unpublished unverified Other UK business not registered in Companies House | UK business not registered in Companies House |
      | unpublished unverified ISD only                                            | ISD Company                                   |
      | unpublished unverified ISD & Trade                                         | ISD Company                                   |
      | unpublished verified LTD, PLC or Royal Charter                             | UK business registered in Companies House     |
      | unpublished verified Sole trader                                           | UK business not registered in Companies House |
      | unpublished verified Charity                                               | UK business not registered in Companies House |
      | unpublished verified Partnership                                           | UK business not registered in Companies House |
      | unpublished verified Other UK business not registered in Companies House   | UK business not registered in Companies House |
      | unpublished verified ISD only                                              | ISD Company                                   |
      | unpublished verified ISD & Trade                                           | ISD Company                                   |
      | published LTD, PLC or Royal Charter                                        | UK business registered in Companies House     |
      | published Sole trader                                                      | UK business not registered in Companies House |
      | published Charity                                                          | UK business not registered in Companies House |
      | published Partnership                                                      | UK business not registered in Companies House |
      | published Other UK business not registered in Companies House              | UK business not registered in Companies House |
      | published ISD only                                                         | ISD Company                                   |
      | published ISD & Trade                                                      | ISD Company                                   |
      | unpublished ISD & published Trade                                          | ISD Company                                   |
