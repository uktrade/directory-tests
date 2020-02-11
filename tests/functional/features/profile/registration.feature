@profile
@allure.suite:Profile
Feature: Trade Profile


  @allure.link:ED-2094
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


  @allure.link:ED-2094
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
  Scenario Outline: Users with an "<trade>" should not be able to view their business details instead they should be redirected to enrolment page
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
  Scenario Outline: Users should see "<an option to publish profile>" for their "<trade>" profile on "Profile - Business Profile" page
    Given "Annette" created an "<trade>" profile for a random company "X"

    When "Annette" goes to "Profile - Business Profile" page

    Then "Annette" should see "<expected business classification>" on the page
    And "Annette" should see "<an option to publish profile>" on the page

    Examples: business types
      | trade                                                                    | expected business classification              | an option to publish profile  |
      | unpublished verified LTD, PLC or Royal Charter                           | UK business registered in Companies House     | Publish your business profile |
      | unpublished verified Sole trader                                         | UK business not registered in Companies House | Publish your business profile |
      | unpublished verified Charity                                             | UK business not registered in Companies House | Publish your business profile |
      | unpublished verified Partnership                                         | UK business not registered in Companies House | Publish your business profile |
      | unpublished verified Other UK business not registered in Companies House | UK business not registered in Companies House | Publish your business profile |

    @wip
    Examples: ISD business accounts
      | trade                                                                    | expected business classification              | an option to publish profile  |
      | unpublished verified ISD only                                            | ISD Company                                   | Publish your business profile |
      | unpublished verified ISD & Trade                                         | ISD Company                                   | Publish your business profile |
      | unpublished ISD & published Trade                                        | ISD Company                                   | Publish your business profile |


  @allure.link:TT-2027
  @published
  @verified
  @captcha
  @dev-only
  @fake-sso-email-verification
  Scenario Outline: An owner of a "<trade>" profile should be able to view their profile on "Find a Supplier" service
    Given "Annette" created an "<trade>" profile for a random company "X"

    When "Annette" goes to "Profile - Business Profile" page
    Then "Annette" should see "View Find a Supplier profile" on the page

    When "Annette" decides to view published FAS Business Profile
    Then "Annette" should be on "X"'s FAS Business Profile page

    Examples: business types
      | trade                                                         |
      | published LTD, PLC or Royal Charter                           |
      | published Sole trader                                         |
      | published Charity                                             |
      | published Partnership                                         |
      | published Other UK business not registered in Companies House |

    @wip
    Examples: ISD business accounts
      | trade                                                         |
      | published ISD only                                            |
      | published ISD & Trade                                         |


  @allure.link:TT-2033
  @unpublish
  @published
  @verified
  @captcha
  @dev-only
  @fake-sso-email-verification
  Scenario Outline: An owner of a "<trade>" profile should be able to remove (unpublish) their profile from "Find a Supplier" service
    Given "Annette" created an "<trade>" profile for a random company "X"

    When "Annette" decides to unpublish profile from Find a Supplier service
    And "Annette" decides to view unpublished profile on Find a Supplier service

    Then "Annette" should be on "Generic - This page cannot be found" page

    Examples: business types
      | trade                                                         |
      | published LTD, PLC or Royal Charter                           |
      | published Sole trader                                         |
      | published Charity                                             |
      | published Partnership                                         |
      | published Other UK business not registered in Companies House |

    @wip
    Examples: ISD business accounts
      | trade                                                         |
      | published ISD only                                            |
      | published ISD & Trade                                         |


  @allure.link:TT-2034
  @unpublished
  @unverified
  @captcha
  @dev-only
  @fake-sso-email-verification
  Scenario Outline: An owner of a "<trade>" profile should receive an email notification when they request a verification
    Given "Annette" created an "<trade>" profile for a random company "X"

    When "Annette" requests to verify her company profile

    Then "Annette" should receive an email notification with subject "We’ve received your verification request"

    Examples: business types
      | trade                                                                      |
      | unpublished unverified Sole trader                                         |
      | unpublished unverified Charity                                             |
      | unpublished unverified Partnership                                         |
      | unpublished unverified Other UK business not registered in Companies House |
