@gtm
@pixels
@allure.suite:PIR
Feature: PIR - Google Tag Manager

  Background:
    Given test authentication is done


  @allure.link:TT-1500
  Scenario Outline: GTM properties should be properly set on "PIR - <selected>" page
    When "Robert" goes to the "PIR - <selected>" page

    Then Google Tag Manager properties should be set to proper values
      | businessUnit   | loginStatus   | siteLanguage   | siteSection   | siteSubsection   | userId   |
      | <businessUnit> | <loginStatus> | <siteLanguage> | <siteSection> | <siteSubsection> | <userId> |

    Examples: Listing pages
      | selected | businessUnit | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Landing  | Invest       | False       | en-gb        | PerfectFit  | FormPage       | None   |
