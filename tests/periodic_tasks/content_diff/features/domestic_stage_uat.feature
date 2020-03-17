Feature: Find content differences between UAT and Staging Domestic environments

  Scenario Outline: Content on Staging page "<selected>" should be the same as on respective UAT page
    When you look at the "main" section of the "<selected>" page on "Domestic" "STAGE" and "UAT"

    Then there should be no differences

    Examples: Misc
      | selected                                                                                          |
      | /                                                                                                 |
      | ?lang=en-gb                                                                                       |
      | community/                                                                                        |
      | triage/                                                                                           |

    Examples: Advice
      | selected                                                                                          |
      | advice/                                                                                           |
      | advice/create-an-export-plan/                                                                     |
      | advice/create-an-export-plan/                                                                     |
      | advice/find-an-export-market/                                                                     |
      | advice/define-route-to-market/                                                                    |
      | advice/get-export-finance-and-funding/                                                            |
      | advice/manage-payment-for-export-orders/                                                          |
      | advice/prepare-to-do-business-in-a-foreign-country/                                               |
      | advice/manage-legal-and-ethical-compliance/                                                       |
      | advice/prepare-for-export-procedures-and-logistics/                                               |
      | advice/create-an-export-plan/how-to-create-an-export-plan/                                        |
      | advice/find-an-export-market/plan-export-market-research/                                         |
      | advice/find-an-export-market/define-export-market-potential/                                      |
      | advice/find-an-export-market/field-research-in-export-markets/                                    |
      | advice/find-an-export-market/trade-shows/                                                         |
      | advice/define-route-to-market/routes-to-market/                                                   |
      | advice/define-route-to-market/sell-overseas-directly/                                             |
      | advice/define-route-to-market/export-agents/                                                      |
      | advice/define-route-to-market/export-distributors/                                                |
      | advice/define-route-to-market/create-a-licensing-agreement/                                       |
      | advice/define-route-to-market/create-a-franchise-agreement/                                       |
      | advice/define-route-to-market/create-a-joint-venture-agreement/                                   |
      | advice/define-route-to-market/set-up-a-business-abroad/                                           |
      | advice/get-export-finance-and-funding/choose-the-right-finance/                                   |
      | advice/get-export-finance-and-funding/get-export-finance/                                         |
      | advice/get-export-finance-and-funding/raise-money-by-borrowing/                                   |
      | advice/get-export-finance-and-funding/borrow-against-assets/                                      |
      | advice/get-export-finance-and-funding/raise-money-with-investment/                                |
      | advice/manage-payment-for-export-orders/how-to-create-an-export-invoice/                          |
      | advice/manage-payment-for-export-orders/payment-methods-for-exporters/                            |
      | advice/manage-payment-for-export-orders/decide-when-to-get-paid-for-export-orders/                |
      | advice/manage-payment-for-export-orders/insure-against-non-payment/                               |
      | advice/prepare-to-do-business-in-a-foreign-country/understand-the-business-culture-in-the-market/ |
      | advice/prepare-to-do-business-in-a-foreign-country/internationalise-your-website/                 |
      | advice/manage-legal-and-ethical-compliance/understand-business-risks-in-overseas-markets/         |
      | advice/manage-legal-and-ethical-compliance/report-corruption-and-human-rights-violations/         |
      | advice/manage-legal-and-ethical-compliance/anti-bribery-and-corruption-training/                  |
      | advice/manage-legal-and-ethical-compliance/protect-your-intellectual-property-when-exporting/     |
      | advice/prepare-for-export-procedures-and-logistics/plan-logistics-for-exporting/                  |
      | advice/prepare-for-export-procedures-and-logistics/get-your-export-documents-right/               |
      | advice/prepare-for-export-procedures-and-logistics/use-a-freight-forwarder-to-export/             |
      | advice/prepare-for-export-procedures-and-logistics/use-incoterms-in-contracts/                    |

    Examples: Case Studies
      | selected                                                                                          |
      | story/online-marketplaces-propel-freestyle-xtreme-sales/                                          |
      | story/hello-babys-rapid-online-growth/                                                            |
      | story/york-bag-retailer-goes-global-via-e-commerce/                                               |

    Examples: Markets
      | selected                                                                                          |
      | markets/                                                                                          |
      | markets/brazil/                                                                                   |
      | markets/china/                                                                                    |
      | markets/germany/                                                                                  |
      | markets/italy/                                                                                    |
      | markets/south-korea/                                                                              |
      | markets/netherlands/                                                                              |

    Examples: UKEF
      | selected                                                                                          |
      | get-finance/                                                                                      |
      | get-finance/contact/                                                                              |

    Examples: Performance dashboard
      | selected                                                                                          |
      | performance-dashboard/                                                                            |
      | performance-dashboard/export-opportunities/                                                       |
      | performance-dashboard/guidance-notes/                                                             |
      | performance-dashboard/invest/                                                                     |
      | performance-dashboard/selling-online-overseas/                                                    |
      | performance-dashboard/trade-profiles/                                                             |

    Examples: Privacy, T&Cs
      | selected                                                                                          |
      | about/                                                                                            |
      | privacy-and-cookies/                                                                              |
      | privacy-and-cookies/fair-processing-notice-export-opportunities/                                  |
      | privacy-and-cookies/fair-processing-notice-export-readiness/                                      |
      | privacy-and-cookies/fair-processing-notice-for-smart-survey/                                      |
      | privacy-and-cookies/fair-processing-notice-invest-in-great-britain/                               |
      | privacy-and-cookies/fair-processing-notice-selling-online-overseas/                               |
      | privacy-and-cookies/fair-processing-notice-trade-profiles-find-a-buyer-fab-find-a-supplier-fas/   |
      | privacy-and-cookies/fair-processing-notice-zendesk/                                               |
      | terms-and-conditions/                                                                             |
