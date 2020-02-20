@contact-us
@no-sso-email-verification-required
@allure.suite:International
Feature: FAS - Contact us

  Background:
    Given basic authentication is done for "International - Landing" page
    And basic authentication is done for "Domestic - Home" page


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


  @allure.link:ED-4246
  Scenario Outline: Buyers should be able to get to the "<expected>" page from the "Find a Supplier - Landing" page
    Given "Robert" visits the "Find a Supplier - Landing" page

    When "Robert" decides to "<contact_us>"

    Then "Robert" should be on the "<expected>" page

    Examples: links
      | contact_us        | expected                                                |
      | Contact us        | International - Find a UK business partner - Contact us |
      | Contact us footer | Domestic - Contact us                                   |


  @allure.link:ED-4247
  @captcha
  @dev-only
  Scenario: Buyers should be able to contact DIT from the "Find a Supplier - Landing" page
    Given "Robert" visits the "International - Find a UK business partner - Contact us" page

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "International - Find a UK business partner - Thank you" page
    And "Robert" should see following sections
      | Sections          |
      | Header            |
      | Content           |
      | Footer            |
    And "Robert" should receive an "Thank you for your Buying from the UK enquiry" confirmation email


  @next-steps
  Scenario Outline: Buyers who want to learn more on how to "<buy or invest>" should be taken to "<expected>" page from "<specific> Industry" page
    Given "Robert" visits the "International - <specific> - industry" page

    When "Robert" decides to "<buy or invest>"

    Then "Robert" should be on the "<expected>" page

    Examples: common industries
      | specific                      | buy or invest              | expected                                                |
      | Creative industries           | I want to invest in the UK | Invest - Contact us                                     |
      | Engineering and manufacturing | I want to buy from the UK  | International - Find a UK business partner - Contact us |

    @full
    @dev-only
    Examples: promoted industries
      | specific                     | buy or invest              | expected                                                |
      | Automotive                   | I want to invest in the UK | Invest - Contact us                                     |
      | Aerospace                    | I want to invest in the UK | Invest - Contact us                                     |
      | Education                    | I want to invest in the UK | Invest - Contact us                                     |
      | Healthcare and Life Sciences | I want to invest in the UK | Invest - Contact us                                     |
      | Legal services               | I want to buy from the UK  | International - Find a UK business partner - Contact us |
      | Real Estate                  | I want to buy from the UK  | International - Find a UK business partner - Contact us |
      | Space                        | I want to buy from the UK  | International - Find a UK business partner - Contact us |
      | Technology                   | I want to buy from the UK  | International - Find a UK business partner - Contact us |

    @full
    @stage-only
    Examples: promoted industries
      | specific                            | buy or invest              | expected                                                |
      | Financial and professional services | I want to invest in the UK | Invest - Contact us                                     |
      | Legal services                      | I want to buy from the UK  | International - Find a UK business partner - Contact us |
      | Technology                          | I want to buy from the UK  | International - Find a UK business partner - Contact us |


  @report-this-page
  Scenario Outline: Buyers should be able to get to "Domestic - Feedback" form in order to report a problem with "<specific> Industry" page
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


  @allure.link:TT-942
  @captcha
  @dev-only
  @contact-us
  Scenario: Contact requests from certain senders should not be forwarded to us
    Given "Robert" was barred from contacting us
    And "Robert" visits the "International - Find a UK business partner - Contact us" page

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "International - Find a UK business partner - Thank you" page
    And "Robert" should not receive a confirmation email
#    @bug
#    @allure.issue:TT-1777
#    @fixme
#    And an email notification about "Robert"'s enquiry should NOT be send to "Trade mailbox"


  @bug
  @allure.issue:TT-277
  @fixed
  @full
  @contact-us
  Scenario: Buyers shouldn't be able to submit the contact us form without passing captcha
    Given "Robert" visits the "International - Find a UK business partner - Contact us" page

    When "Robert" fills out and submits the form
      | field   | value     |
      | captcha | unchecked |

    Then "Robert" should be on the "International - Find a UK business partner - Contact us" page
