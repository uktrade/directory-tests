@guidance
Feature: Guidance articles

  @wip
  @ED-2463
  @home-page
  @articles
  Scenario Outline: Any Exporter should get to a relevant article list from Guidance section on the homepage
    Given "Robert" is interested in "<guidance_category>" guidance

    When "Robert" goes to the relevant "<guidance_category>" link in the Guidance section on the homepage

    Then "Robert" should see an ordered list of all articles  selected for "<guidance_category>" + "next category"
    And "Robert" should see a Articles Read counter, Total number of Articles and Time to complete remaining chapters
    And "Robert" should see a link to the next Guidance category

    Examples:
      | guidance_category |
      | Market research   |
      | Customer insight  |
      | Finance           |
      | Business planning |
      | Getting paid      |


  @wip
  @ED-2464
  @home-page
  @articles
  Scenario Outline: Any Exporter should see article read count for each tile in the Guidance section on the homepage
    Given "Robert" visits the home page

    When "Robert" sees "<guidance_category>" tile in the Guidance section on the homepage

    Then "Robert" should see an article read count for the "<guidance_category>"

    Examples:
      | guidance_category |
      | Market research   |
      | Customer insight  |
      | Finance           |
      | Business planning |
      | Getting paid      |


  @wip
  @ED-2465
  @personalised-page
  @articles
  Scenario Outline: Regular Exporter should see article read count for each tile in the Guidance section on the personalised page
    Given "Nadia" visits the personalised page

    When "Nadia" sees "<guidance_category>" tile in the Guidance section on the homepage

    Then "Nadia" should see an article read count for the "<guidance_category>"

    Examples:
      | guidance_category |
      | Market research   |
      | Customer insight  |
      | Finance           |
      | Business planning |
      | Getting paid      |


  @wip
  @ED-2466
  @personalised-page
  @articles
  Scenario Outline: Regular Exporter should get to a relevant article list from Guidance section on the personalised page
    Given "Nadia" is interested in "<guidance_category>" guidance

    When "Nadia" goes to the relevant "<guidance_category>" link in the Guidance section on the personalised page

    Then "Nadia" should see an ordered list of all articles  selected for "<guidance_category>" + "next category"
    And "Nadia" should see a Articles Read counter, Total number of Articles and Time to complete remaining chapters
    And "Nadia" should see a link to the next Guidance category

    Examples:
      | guidance_category |
      | Market research   |
      | Customer insight  |
      | Finance           |
      | Business planning |
      | Getting paid      |


  @wip
  @ED-2467
  @banner
  Scenario Outline: Guidance Banner should be visible when on Guidance Article List
    Given "Robert" accessed "<guidance_category>" guidance articles using "<guidance_menu_location>"

    Then "Robert" should see the Guidance Category Banner
    And "Robert" should see that the banner tile for "guidance_category" category is highlighted

    Examples:
      | guidance_category | guidance_menu_location |
      | Market research   | header menu            |
      | Customer insight  | home page              |
      | Finance           | personalised page      |
      | Business planning | footer links           |
      | Getting paid      | ....                   |

