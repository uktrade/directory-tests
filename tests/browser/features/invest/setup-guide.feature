@uk-setup-guide
Feature: UK Setup Guide

  @CMS-161
  Scenario: Visitors should be able to see the "Invest UK Setup Guide" page
    Given "Robert" visits the "Invest - UK Setup Guide" page

    Then "Robert" should see following sections
      | Sections         |
      | Header           |
      | Beta bar         |
      | Hero             |
      | Introduction     |
      | Guides           |
      | Report this page |
      | Footer           |


  @CMS-161
  Scenario Outline: Overseas businesses should be able to learn how to Setup in the UK by reading the "<selected>" guide
    Given "Robert" visits the "Invest - UK Setup Guide" page

    When "Robert" decides to read "Invest - <selected> - guide" guide

    Then "Robert" should be on the "Invest - <selected> - guide" page
    And "Robert" should see content specific to "Invest - <selected> - guide" page

    Examples: UK Setup Guides
      | selected                                                |
      | Apply for a UK visa                                     |
      | Establish a base for business in the UK                 |
      | Hire skilled workers for your UK operations             |
      | Open a UK business bank account                         |
      | Set up a company in the UK                              |
      | Understand the UK's tax, incentives and legal framework |


  @CMS-161
  Scenario Outline: Visitors should be able to see all expected sections on "<selected>" guide page
    Given "Robert" visits the "Invest - <selected> - guide" page

    Then "Robert" should see following sections
      | Sections         |
      | Header           |
      | Beta bar         |
      | Hero             |
      | Content          |
      | Report this page |
      | Footer           |

    Examples: UK Setup Guides
      | selected                                                |
      | Apply for a UK visa                                     |
      | Establish a base for business in the UK                 |
      | Hire skilled workers for your UK operations             |
      | Open a UK business bank account                         |
      | Set up a company in the UK                              |
      | Understand the UK's tax, incentives and legal framework |
