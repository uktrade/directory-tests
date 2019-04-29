@invest
@hpo
@pdf
Feature: HPO PDFs sent after

  Background:
    Given basic authentication is done for "Invest - Home" page

  @TT-444
  @dev-only
  @captcha
  Scenario Outline: Check PDFs listed on "Thank you for your enquiry" page for "<selected>" HPO
    Given "Peter Alder" got in touch with us via "Invest - <selected> - HPO Contact Us" page
      | field                    | value     |
      | Advanced food production | checked   |
      | Lightweight structures   | unchecked |
      | Rail infrastructure      | unchecked |
    And "Peter Alder" is on the "Invest - Thank you for your enquiry - HPO Contact us" page

    When "Peter Alder" downloads all visible PDFs

    Then "Peter Alder" should see correct details in every downloaded PDF
      | telephone number = +44(0) 207 000 9012    |
      | email address = enquiries@invest-trade.uk |
    And there should not be any dead links in every downloaded PDF

    Examples:
      | selected                 |
      | Advanced food production |


  @TT-444
  @dev-only
  @captcha
  Scenario Outline: Check PDFs listed on "Thank you for your enquiry" page for "<selected>" HPO
    Given "Peter Alder" got in touch with us via "Invest - <selected> - HPO Contact Us" page
      | field                    | value     |
      | Advanced food production | unchecked |
      | Lightweight structures   | checked   |
      | Rail infrastructure      | unchecked |
    And "Peter Alder" is on the "Invest - Thank you for your enquiry - HPO Contact us" page

    When "Peter Alder" downloads all visible PDFs

    Then "Peter Alder" should see correct details in every downloaded PDF
      | telephone number = +44(0) 207 000 9012    |
      | email address = enquiries@ukti.gsi.gov.uk |
    And there should not be any dead links in every downloaded PDF

    Examples:
      | selected               |
      | Lightweight structures |


  @TT-444
  @dev-only
  @captcha
  Scenario Outline: Check PDFs listed on "Thank you for your enquiry" page for "<selected>" HPO
    Given "Peter Alder" got in touch with us via "Invest - <selected> - HPO Contact Us" page
      | field                    | value     |
      | Advanced food production | unchecked |
      | Lightweight structures   | unchecked |
      | Rail infrastructure      | checked   |
    And "Peter Alder" is on the "Invest - Thank you for your enquiry - HPO Contact us" page

    When "Peter Alder" downloads all visible PDFs

    Then "Peter Alder" should see correct details in every downloaded PDF
      | telephone number = +44(0) 207 000 9012    |
      | email address = enquiries@invest-trade.uk |
    And there should not be any dead links in every downloaded PDF

    Examples:
      | selected            |
      | Rail infrastructure |
