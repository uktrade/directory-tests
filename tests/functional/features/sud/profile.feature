Feature: SUD (Profile) pages


    @ED-2265
    @sso
    @account
    Scenario: Users should be able to view SUD Landing page without authentication
      Given "Peter Alder" is an unauthenticated supplier

      When "Peter Alder" goes to "SUD Landing" page

      Then "Peter Alder" should see "SUD Landing" page


    @ED-2265
    @sso
    @account
    Scenario Outline: Users should be able to view SUD Landing page without authentication
      Given "Peter Alder" is an unauthenticated supplier

      When "Peter Alder" goes to "<SUD>" page

      Then "Peter Alder" should see "<Landing>" page

      Examples: SUD pages
      |SUD                        |Landing      |
      |SUD Selling Online Overseas|SUD About    |
      |SUD Export Opportunities   |SUD About    |
      |SUD Find a Buyer           |SSO Login    |
