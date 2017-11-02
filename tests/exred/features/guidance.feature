@guidance
Feature: Guidance articles

  @ED-2463
  @home-page
  @articles
  @<specific>
  Scenario Outline: Any Exporter should get to a "<specific>" article list from Guidance section on the home page
    Given "Robert" visits the "Home" page for the first time

    When "Robert" goes to the "<specific>" Guidance articles via "home page"

    Then "Robert" should see an ordered list of all articles selected for "<specific>" category
    And "Robert" should see on the Guidance Articles page "Articles Read counter, Total number of Articles, Time to complete remaining chapters"
    And "Robert" should see a link to the "<next>" Guidance category

    Examples: Guidance categories
      | specific          | next              |
      | Market research   | Customer insight  |
      | Customer insight  | Finance           |
      | Finance           | Business planning |
      | Business planning | Getting paid      |
      | Getting paid      | last              |


  @ED-2464
  @home-page
  @articles
  Scenario Outline: Any Exporter should see article read count for "<specific>" Guidance category when accessed via home page
    Given "Robert" visits the "Home" page for the first time

    When "Robert" goes to the "<specific>" Guidance articles via "home page"

    Then "Robert" should see an article read counter for the "<specific>" Guidance category set to "0"
    And "Robert" should see total number of articles for the "<specific>" Guidance category

    Examples:
      | specific          |
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


  @ED-2467
  @banner
  @<category>
  @<location>
  Scenario Outline: Guidance Banner should be visible when on "<category>" Guidance Article List accessed via "<location>"
    Given "Robert" accessed "<category>" guidance articles using "<location>"

    Then "Robert" should see the Guidance Navigation Ribbon
    And "Robert" should see that the banner tile for "<category>" category is highlighted

    Examples: header menu
      | category                  | location    |
      | Market research           | header menu |
      | Customer insight          | header menu |
      | Finance                   | header menu |
      | Business planning         | header menu |
      | Getting paid              | header menu |
      | Operations and Compliance | header menu |

    Examples: footer links
      | category                  | location     |
      | Market research           | footer links |
      | Customer insight          | footer links |
      | Finance                   | footer links |
      | Business planning         | footer links |
      | Getting paid              | footer links |
      | Operations and Compliance | footer links |

    Examples: home page
      | category                  | location  |
      | Market research           | home page |
      | Customer insight          | home page |
      | Finance                   | home page |
      | Business planning         | home page |
      | Getting paid              | home page |
      | Operations and Compliance | home page |
