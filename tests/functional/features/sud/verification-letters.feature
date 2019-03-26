Feature: Letter verification
  We would like to be sure that the letters we send to the newly registered
  users contain correct details (like links, address, company name etc.)

  @ED-3729
  @stannp
  @letter
  @verification
  Scenario: Check links
    Given "Peter Alder" sends a test verification letter via StanNP for randomly selected company

    When "Peter Alder" downloads the pdf with the verification letter

    Then "Peter Alder" should see correct details in the pdf with the verification letter
      | correct_details    |
      | company name       |
      | recipient name     |
      | recipient postcode |
      | address line 1     |
      | address line 2     |
      | verification code  |
      | verification link  |
      | contact us link    |
