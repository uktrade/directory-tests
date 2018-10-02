@invest
@hpo
@pdf
Feature: HPO PDFs sent after


  @TT-444
  Scenario Outline: Check PDFs listed on "Thank you for your enquiry" page
    Given "Peter Alder" got in touch with us via "Invest - <selected> - HPO Contact Us" page
    And "Peter Alder" is on the "Invest - Thank you for your enquiry - HPO Contact us" page

    When "Peter Alder" downloads all visible PDFs

    Then "Peter Alder" should see correct details in every downloaded PDF
      | telephone number = +44(0) 207 000 9012    |
      | email address = enquiries@invest-trade.uk |
    And there should not be any dead links in every downloaded PDF

    Examples:
      | selected                          |
      | High productivity food production |

    @full
    Examples:
      | selected                          |
      | Lightweight structures            |
      | Rail infrastructure               |
