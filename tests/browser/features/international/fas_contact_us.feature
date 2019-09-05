@contact-us
@no-sso-email-verification-required
Feature: Find a Supplier - Contact us

  Background:
    Given basic authentication is done for "International - Landing" page


  @captcha
  @dev-only
  Scenario: Buyers should be able to send a query to supplier and see correct header & footer on "Find a Supplier - Thank you for contacting supplier" page
    Given "Robert" searched for companies using "food" keyword in "any" sector

    When "Robert" decides to view "random" company profile
    Then "Robert" should be on the "Find a Supplier - Company profile" page

    When "Robert" decides to "Contact company"
    Then "Robert" should be on the "Find a Supplier - Contact supplier" page

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Find a Supplier - Thank you for contacting supplier" page
    And "Robert" should see following sections
      | Sections |
      | Header   |
      | Footer   |


  @ED-4246
  Scenario Outline: Buyers should be able to get to the "<expected>" page from the "Find a Supplier - Landing" page
    Given "Robert" visits the "Find a Supplier - Landing" page

    When "Robert" decides to "<contact_us>"

    Then "Robert" should be on the "<expected>" page

    Examples: links
      | contact_us        | expected                                                |
      | Contact us        | International - Find a UK business partner - Contact us |
      | Contact us footer | Domestic - Contact us                                   |


  @ED-4247
  @captcha
  @dev-only
  Scenario: Buyers should be able to contact DIT from the "Find a Supplier - Landing" page
    Given "Robert" visits the "International - Find a UK business partner - Contact us" page

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "International - Find a UK business partner - Thank you for your message" page
    And "Robert" should see following sections
      | Sections          |
      | Header            |
      | Content           |
      | Footer            |


  @next-steps
  Scenario Outline: Buyers should be able to report a problem with the "<specific> Industry" page
    Given "Robert" visits the "International - <specific> - industry" page

    When "Robert" decides to "<buy or invest>"

    Then "Robert" should be on the "International - <expected>" page

    Examples: common industries
      | specific                      | buy or invest    | expected                    |
      | Creative industries           | invest in the UK | Contact the investment team |
      | Engineering and manufacturing | buy from the UK  | Find a UK business partner  |

    @full
    @dev-only
    Examples: promoted industries
      | specific                            | buy or invest    | expected                    |
      | Automotive                          | invest in the UK | Contact the investment team |
      | Aerospace                           | invest in the UK | Contact the investment team |
      | Education                           | invest in the UK | Contact the investment team |
      | Healthcare and Life Sciences        | invest in the UK | Contact the investment team |
      | Legal services                      | buy from the UK  | Find a UK business partner  |
      | Real Estate                         | buy from the UK  | Find a UK business partner  |
      | Space                               | buy from the UK  | Find a UK business partner  |
      | Technology                          | buy from the UK  | Find a UK business partner  |

    @full
    @stage-only
    Examples: promoted industries
      | specific                            | buy or invest    | expected                    |
      | Financial and professional services | invest in the UK | Contact the investment team |
      | Legal services                      | buy from the UK  | Find a UK business partner  |
      | Technology                          | buy from the UK  | Find a UK business partner  |

    @wip
    @dev-only
    Examples: missing content
      | specific                            | buy or invest    | expected                    |
      | Energy                              | invest in the UK | Contact the investment team |


  @report-this-page
  Scenario Outline: Buyers should be able to report a problem with the "<specific> Industry" page
    Given "Robert" visits the "International - <specific> - industry" page

    When "Robert" decides to "report a problem with the page"

    Then "Robert" should be on the "Domestic - Feedback" page

    Examples: common industries
      | specific                            |
      | Creative industries                 |

    @full
    @dev-only
    Examples: promoted industries
      | specific                            |
      | Automotive                          |
      | Aerospace                           |
      | Education                           |
      | Engineering and manufacturing       |
      | Healthcare and Life Sciences        |
      | Legal services                      |
      | Real Estate                         |
      | Space                               |
      | Technology                          |

    @full
    @stage-only
    Examples: promoted industries
      | specific                            |
      | Engineering and manufacturing       |
      | Financial and professional services |
      | Legal services                      |
      | Technology                          |

    @wip
    @dev-only
    Examples: missing content
      | specific                            |
      | Energy                              |


  @captcha
  @report-this-page
  Scenario Outline: Buyers should be able to report a problem with the "<specific> Industry" page
    Given "Robert" visits the "International - <specific> - industry" page
    And "Robert" decided to "report a problem with the page"
    And "Robert" is on the "Domestic - Feedback" page

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Domestic - Thank you for your feedback" page

    Examples: common industries
      | specific                            |
      | Creative industries                 |


  @bug
  @TT-1777
  @TT-942
  @captcha
  @dev-only
  @contact-us
  Scenario: Contact requests from certain senders should not be forwarded to us
    Given "Robert" was barred from contacting us
    And "Robert" visits the "International - Find a UK business partner - Contact us" page

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "International - Find a UK business partner - Thank you for your message" page
    And "Robert" should not receive a confirmation email
# Please uncomment this step and delete next scenario once TT-1777 is fixed
#    And an email notification about "Robert"'s enquiry should NOT be send to "Trade mailbox"


  @bug
  @TT-1777
  @fixme
  @TT-942
  @captcha
  @dev-only
  @contact-us
  Scenario: Contact requests from certain senders should not be forwarded to us
    Given "Robert" was barred from contacting us
    And "Robert" visits the "International - Find a UK business partner - Contact us" page

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "International - Find a UK business partner - Thank you for your message" page
    And "Robert" should not receive a confirmation email
    And an email notification about "Robert"'s enquiry should NOT be send to "Trade mailbox"


  @bug
  @TT-277
  @fixed
  @full
  @contact-us
  Scenario: Buyers shouldn't be able to submit the contact us form without passing captcha
    Given "Robert" visits the "International - Find a UK business partner - Contact us" page

    When "Robert" fills out and submits the contact us form without passing captcha

    Then "Robert" should be on the "International - Find a UK business partner - Contact us" page
