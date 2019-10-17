@profile
Feature: Trade Profile


  @ED-2094
  @verification
  @letter
  @captcha
  @dev-only
  @fake-sso-email-verification
  Scenario: Logged-in Supplier should be able to verify profile by using code and link from the letter
    Given "Annette Geissinger" created an "unpublished unverified LTD, PLC or Royal Charter" profile for a random company "Company X"
    And "Annette Geissinger" set the company description
    And "Annette Geissinger" decided to verify her identity with a verification letter
    And "Annette Geissinger" received the letter with verification code

    When "Annette Geissinger" goes to the verification link from the letter as authenticated user
    And "Annette Geissinger" submits the verification code

    Then "Annette Geissinger" should be told that company has been verified

    When "Annette Geissinger" goes to "Profile - Business Profile" page
    Then "Annette Geissinger" should be told that business profile is ready to be published


  @ED-2094
  @verification
  @letter
  @captcha
  @dev-only
  @fake-sso-email-verification
  Scenario: Logged-out Supplier should be able to verify profile by using code and link from the letter
    Given "Annette Geissinger" created an "unpublished unverified LTD, PLC or Royal Charter" profile for a random company "Company X"
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
  Scenario: Users can't create profile for an "Overseas company"
    Given "Annette" decided to create an "Overseas company" profile for a random company "X"
    Then "Annette" should be on "Profile - Overseas business cannot create an account" page


  @individual
  @verified
  @captcha
  @dev-only
  @fake-sso-email-verification
  Scenario Outline: "<trade>" should not see any business details on their Profile page and options to manage profile
    Given "Annette" decided to create an "<trade>" profile

    When "Annette" goes to "Profile - Business Profile" page

    Then "Annette" should be on "Profile - Business Profile (get a profile)" page
    And "Annette" should not see options to manage profile

    Examples: business types
      | trade                 |
      | verified Individual   |


  @individual
  @unverified
  @captcha
  @dev-only
  @fake-sso-email-verification
  Scenario Outline: "<trade>" should not be able to sign in and get to their profile
    Given "Annette" decided to create an "<trade>" profile

    When "Annette" attempts to sign in to SSO/great.gov.uk account

    Then "Annette" should be on "SSO - Verify your email" page

    Examples: business types
      | trade                 |
      | unverified Individual |


  @unverified
  @captcha
  @dev-only
  @fake-sso-email-verification
  Scenario Outline: Users with "<trade>" profile should not be able to view their business details but should be redirected to enrolment page
    Given "Annette" decided to create an "<trade>" profile

    When "Annette" goes to "Profile - Business Profile" page

    Then "Annette" should be on "Profile - Enrol" page

    Examples: business types
      | trade                                                                                       |
      | unverified SSO/great.gov.uk account for LTD, PLC or Royal Charter                           |
      | unverified SSO/great.gov.uk account for Sole trader                                         |
      | unverified SSO/great.gov.uk account for Charity                                             |
      | unverified SSO/great.gov.uk account for Partnership                                         |
      | unverified SSO/great.gov.uk account for Other UK business not registered in Companies House |

    @wip
    Examples: ISD business accounts
      | trade                                                                                       |
      | unverified SSO/great.gov.uk account for ISD only                                            |
      | unverified SSO/great.gov.uk account for ISD & Trade                                         |


  @unpublished
  @unverified
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

    @wip
    Examples: ISD business accounts
      | trade                                                                      | expected business classification              |
      | unpublished unverified ISD only                                            | ISD Company                                   |
      | unpublished unverified ISD & Trade                                         | ISD Company                                   |


  @unpublished
  @verified
  @captcha
  @dev-only
  @fake-sso-email-verification
  Scenario Outline: Users should see "<expected business classification>" for their "<trade>" profile on "Profile - Business Profile" page
    Given "Annette" created an "<trade>" profile for a random company "X"

    When "Annette" goes to "Profile - Business Profile" page

    Then "Annette" should see "<expected business classification>" on the page
    And "Annette" should not see "<option to verify>" on the page

    Examples: business types
      | trade                                                                    | expected business classification              | option to verify      |
      | unpublished verified LTD, PLC or Royal Charter                           | UK business registered in Companies House     | Confirm your identity |
      | unpublished verified Sole trader                                         | UK business not registered in Companies House | Request to verify     |
      | unpublished verified Charity                                             | UK business not registered in Companies House | Request to verify     |
      | unpublished verified Partnership                                         | UK business not registered in Companies House | Request to verify     |
      | unpublished verified Other UK business not registered in Companies House | UK business not registered in Companies House | Request to verify     |

    @wip
    Examples: ISD business accounts
      | trade                                                                      | expected business classification              |
      | unpublished verified ISD only                                              | ISD Company                                   |
      | unpublished verified ISD & Trade                                           | ISD Company                                   |
      | unpublished ISD & published Trade                                          | ISD Company                                   |


  @published
  @verified
  @captcha
  @dev-only
  @fake-sso-email-verification
  Scenario Outline: Users should see "<expected business classification>" for their "<trade>" profile on "Profile - Business Profile" page
    Given "Annette" created an "<trade>" profile for a random company "X"

    When "Annette" goes to "Profile - Business Profile" page

    Then "Annette" should see "<expected business classification>" on the page
    And "Annette" should not see "<option to verify>" on the page

    Examples: business types
      | trade                                                                      | expected business classification              | option to verify      |
      | published LTD, PLC or Royal Charter                                        | UK business registered in Companies House     | Confirm your identity |

    @bug
    @TT-1933
    @fixed
    Examples: business types
      | trade                                                                      | expected business classification              | option to verify      |
      | published Sole trader                                                      | UK business not registered in Companies House | Request to verify     |
      | published Charity                                                          | UK business not registered in Companies House | Request to verify     |
      | published Partnership                                                      | UK business not registered in Companies House | Request to verify     |
      | published Other UK business not registered in Companies House              | UK business not registered in Companies House | Request to verify     |

    @wip
    Examples: ISD business accounts
      | trade                                                                      | expected business classification              |
      | published ISD only                                                         | ISD Company                                   |
      | published ISD & Trade                                                      | ISD Company                                   |
