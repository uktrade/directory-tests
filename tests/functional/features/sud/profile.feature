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
      |Profile - Find a Buyer           | Profile - Enrol |
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
