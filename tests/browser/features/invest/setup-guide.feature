@wip
@uk-setup-guide
Feature: UK Setup Guide

  Scenario: Visitors should be able to see the "Invest UK Setup Guide" page
    Given "Robert" visits the "Invest - UK Setup Guide" page

    Then "Robert" should see following sections
      | Header       |
      | Beta bar     |
      | Hero         |
      | Introdcution |
      | Guides       |
      | Footer       |


  Scenario Outline: Overseas businesses should be able to learn how to Setup in the UK by reading the "<selected>" guide
    Given "Robert" visits the "Invest UK Setup Guide" page

    When "Robert" decides to find out out more about "<selected>" guide

    Then "Robert" should be on the "Invest UK Setup Guide" page
    And "Robert" should see content specific to "Invest - <selected> guide" page

    Examples: UK Setup Guides
      | selected                                                         |
      | Apply for a UK visa                                     |
      | Establish a base for business in the UK                 |
      | Hire skilled workers for your UK operations             |
      | Open a UK business bank account                         |
      | Set up a company in the UK                              |
      | Understand the UK's tax, incentives and legal framework |


  Scenario Outline: Visitors should be able to see all expected sections on "<selected>" guide page
    Given "Robert" visits the "Invest - <selected> guide" page

    Then "Robert" should see expected page sections
      | Header       |
      | Beta bar     |
      | Hero         |
      | Content      |
      | Footer       |

    Examples: UK Setup Guides
      | selected                                                         |
      | Apply for a UK visa                                     |
      | Establish a base for business in the UK                 |
      | Hire skilled workers for your UK operations             |
      | Open a UK business bank account                         |
      | Set up a company in the UK                              |
      | Understand the UK's tax, incentives and legal framework |
