@hpo
Feature: High Potential Opportunities

  Background:
    Given basic authentication is done for "Invest - Home" page

  @TT-442
  Scenario Outline: Investors should be able to view "HPO - <selected>" page
    Given "Annette Geissinger" visits the "Invest - <selected> - HPO" page

    Then "Annette Geissinger" should see following sections
      | Sections               |
#      | Header                 |
#      | Beta bar               |
      | Hero                   |
      | Contact us             |
      | Proposition one        |
      | Opportunity list       |
      | Proposition two        |
      | Competitive advantages |
#      | Testimonial            |  # this is not present on these 2 pages
      | Case studies           |
      | Other opportunities    |
      | Error reporting        |
      | Footer                 |
    And "Annette Geissinger" should not see following section
      | section          |
      | Breadcrumbs      |

    Examples: HPO pages
      | selected                 |
      | Advanced food production |
      | Lightweight structures   |


  @TT-442
  Scenario Outline: Investors should be able to view "HPO - <selected>" page
    Given "Annette Geissinger" visits the "Invest - <selected> - HPO" page

    Then "Annette Geissinger" should see following sections
      | Sections               |
#      | Header                 |
#      | Beta bar               |
      | Hero                   |
      | Contact us             |
      | Proposition one        |
      | Opportunity list       |
      | Proposition two        |
      | Competitive advantages |
      | Testimonial            |
      | Case studies           |
      | Other opportunities    |
      | Error reporting        |
      | Footer                 |
    And "Annette Geissinger" should not see following section
      | section          |
      | Breadcrumbs      |

    Examples: HPO pages
      | selected               |
      | Rail infrastructure    |


  @TT-442
  @contact-us
  Scenario Outline: Investors should be able to reach "Contact us" page from "HPO - <selected>" page
    Given "Annette Geissinger" visits the "Invest - <selected> - HPO" page

    When "Annette Geissinger" decides to "Get in touch"

    Then "Annette Geissinger" should be on the "Invest - Contact us - HPO Contact us" page
    And "Annette Geissinger" should see that "<selected> checkbox" in the form is "selected"
    And "Annette Geissinger" should see following sections
      | sections         |
#      | Beta Bar         |
      | Form             |
      | Error reporting  |

    Examples: HPO pages
      | selected                 |
      | Advanced food production |

    @full
    Examples: HPO pages
      | selected                 |
      | Lightweight structures   |
      | Rail infrastructure      |


  @bug
  @TT-518
  @fixme
  @TT-442
  Scenario Outline: Investors should not see breadcrumbs on "HPO - <selected>" page
    Given "Annette Geissinger" visits the "Invest - <selected> - HPO Contact Us" page

    Then "Annette Geissinger" should not see following section
      | section          |
      | Breadcrumbs      |

    Examples: HPO Contact Us pages
      | selected                 |
      | Advanced food production |

    @full
    Examples: HPO Contact Us pages
      | selected                 |
      | Lightweight structures   |
      | Rail infrastructure      |


  @TT-442
  @related-opportunities
  Scenario Outline: Investors should be able to view "Other investment opportunities" from "HPO - <selected>" page
    Given "Annette Geissinger" visits the "Invest - <selected> - HPO" page

    When "Annette Geissinger" decides to use "<specific> opportunity" link

    Then "Annette Geissinger" should be on the "Invest - <expected opportunity> - HPO" page

    Examples: HPO pages
      | selected                 | specific | expected opportunity     |
      | Advanced food production | first    | Lightweight structures   |
      | Lightweight structures   | second   | Rail infrastructure      |
      | Rail infrastructure      | first    | Advanced food production |

    @full
    Examples: HPO pages
      | selected                 | specific | expected opportunity     |
      | Advanced food production | second   | Rail infrastructure      |
      | Lightweight structures   | first    | Advanced food production |
      | Rail infrastructure      | second   | Lightweight structures   |


  @bug
  @TT-879
  @fixed
  @TT-443
  @dev-only
  @captcha
  @contact-us
  Scenario Outline: Investors should be able to contact us via "<selected>" HPO page
    Given "Annette Geissinger" visits the "Invest - <selected> - HPO Contact Us" page

    When "Annette Geissinger" fills out and submits the form

    Then "Annette Geissinger" should be on the "Invest - Thank you for your enquiry - HPO Contact us" page
    And "Annette Geissinger" should see following sections
      | Sections         |
#      | Beta bar         |
      | Confirmation     |
      | Documents        |
      | Error reporting  |
    And "Annette Geissinger" should receive HPO enquiry confirmation email
    And HPO Agent should receive HPO enquiry email from "Annette Geissinger"

    Examples: HPO pages
      | selected                 |
      | Advanced food production |

    @full
    Examples: HPO pages
      | selected                 |
      | Lightweight structures   |
      | Rail infrastructure      |


  @bug
  @TT-879
  @fixed
  @bug
  @TT-518
  @fixme
  @TT-443
  @contact-us
  @dev-only
  @captcha
  Scenario Outline: Investors should not see breadcrumbs on the "Thank you for your enquiry" page
    Given "Annette Geissinger" visits the "Invest - <selected> - HPO Contact Us" page

    When "Annette Geissinger" fills out and submits the form

    Then "Annette Geissinger" should be on the "Invest - Thank you for your enquiry - HPO Contact us" page
    Then "Annette Geissinger" should not see following section
      | section          |
      | Breadcrumbs      |

    Examples: HPO pages
      | selected                 |
      | Advanced food production |

    @full
    Examples: HPO pages
      | selected                 |
      | Lightweight structures   |
      | Rail infrastructure      |
