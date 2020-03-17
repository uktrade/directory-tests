Feature: Find content differences between Staging and DEV International environments

  Scenario Outline: Content on Staging page "<selected>" should be the same as on respective Dev page
    When you look at the "main" section of the "<selected>" page on "International" "STAGE" and "DEV"

    Then there should be no differences

    Examples: Landing
      | selected                                                                               |
      | /                                                                                      |
      | ?lang=de                                                                               |
      | ?lang=es                                                                               |
      | ?lang=en-gb                                                                            |
      | ?lang=fr                                                                               |
      | ?lang=ja                                                                               |
      | ?lang=pt                                                                               |
      | ?lang=zh-hans                                                                          |
      | about-uk/why-choose-uk/business-environment-guide/                                     |
      | campaigns/                                                                             |
      | content/campaigns/life-changing-artificial-intelligence-ai/                            |
      | content/trade/how-we-help-you-buy/                                                     |
      | contact/                                                                               |

    Examples: About UK
      | selected                                                                               |
      | content/about-uk/                                                                      |
      | content/about-uk/industries/                                                           |
      | content/about-uk/industries/?lang=de                                                   |
      | content/about-uk/industries/?lang=es                                                   |
      | content/about-uk/industries/?lang=fr                                                   |
      | content/about-uk/industries/?lang=ja                                                   |
      | content/about-uk/industries/?lang=pt                                                   |
      | content/about-uk/industries/?lang=zh-hans                                              |
      | content/about-uk/industries/creative-industries/                                       |
      | content/about-uk/industries/creative-industries/?lang=de                               |
      | content/about-uk/industries/creative-industries/?lang=es                               |
      | content/about-uk/industries/creative-industries/?lang=fr                               |
      | content/about-uk/industries/creative-industries/?lang=ja                               |
      | content/about-uk/industries/creative-industries/?lang=pt                               |
      | content/about-uk/industries/creative-industries/?lang=zh-hans                          |
      | content/about-uk/industries/engineering-and-manufacturing/                             |
      | content/about-uk/industries/engineering-and-manufacturing/?lang=de                     |
      | content/about-uk/industries/engineering-and-manufacturing/?lang=es                     |
      | content/about-uk/industries/engineering-and-manufacturing/?lang=fr                     |
      | content/about-uk/industries/engineering-and-manufacturing/?lang=ja                     |
      | content/about-uk/industries/engineering-and-manufacturing/?lang=pt                     |
      | content/about-uk/industries/engineering-and-manufacturing/?lang=zh-hans                |
      | content/about-uk/industries/financial-and-professional-services/                       |
      | content/about-uk/industries/financial-and-professional-services/?lang=de               |
      | content/about-uk/industries/financial-services/                                        |
      | content/about-uk/industries/financial-services/?lang=de                                |
      | content/about-uk/industries/financial-services/building-fintech-bridges/               |
      | content/about-uk/industries/financial-services/building-fintech-bridges/?lang=de       |
      | content/about-uk/industries/legal-services/                                            |
      | content/about-uk/industries/real-estate/                                               |
      | content/about-uk/industries/technology/                                                |
      | content/about-uk/industries/technology/?lang=de                                        |
      | content/about-uk/industries/technology/?lang=es                                        |
      | content/about-uk/industries/technology/?lang=fr                                        |
      | content/about-uk/industries/technology/?lang=pt                                        |
      | content/about-uk/industries/technology/?lang=zh-hans                                   |
      | content/about-uk/industries/technology/uk-ces-2019/                                    |
      | content/about-uk/regions/                                                              |
      | content/about-uk/why-choose-uk/                                                        |
      | content/about-uk/why-choose-uk/uk-infrastructure/                                      |
      | content/about-uk/why-choose-uk/uk-talent-and-labour/                                   |
      | content/about-uk/why-choose-uk/uk-tax-and-incentives/                                  |
      | content/about-us/                                                                      |

    Examples: Capital invest
      | selected                                                                               |
      | content/capital-invest/                                                                |
      | content/capital-invest/?lang=de                                                        |
      | content/capital-invest/?lang=es                                                        |
      | content/capital-invest/?lang=fr                                                        |
      | content/capital-invest/?lang=pt                                                        |
      | content/capital-invest/contact/                                                        |
      | content/capital-invest/how-we-help-you-invest-capital/                                 |

    Examples: How to setup in the UK
      | selected                                                                               |
      | content/how-to-setup-in-the-uk/                                                        |
      | content/how-to-setup-in-the-uk/?lang=de                                                |
      | content/how-to-setup-in-the-uk/?lang=en-gb                                             |
      | content/how-to-setup-in-the-uk/?lang=es                                                |
      | content/how-to-setup-in-the-uk/?lang=fr                                                |
      | content/how-to-setup-in-the-uk/?lang=ja                                                |
      | content/how-to-setup-in-the-uk/?lang=pt                                                |
      | content/how-to-setup-in-the-uk/?lang=zh-hans                                           |
      | content/how-to-setup-in-the-uk/access-finance-in-the-uk/                               |
      | content/how-to-setup-in-the-uk/brexit-readiness-webinars-for-eu-businesses/            |
      | content/how-to-setup-in-the-uk/establish-a-base-for-business-in-the-uk/                |
      | content/how-to-setup-in-the-uk/establish-a-base-for-business-in-the-uk/?lang=de        |
      | content/how-to-setup-in-the-uk/establish-a-base-for-business-in-the-uk/?lang=es        |
      | content/how-to-setup-in-the-uk/establish-a-base-for-business-in-the-uk/?lang=fr        |
      | content/how-to-setup-in-the-uk/establish-a-base-for-business-in-the-uk/?lang=ja        |
      | content/how-to-setup-in-the-uk/establish-a-base-for-business-in-the-uk/?lang=pt        |
      | content/how-to-setup-in-the-uk/establish-a-base-for-business-in-the-uk/?lang=zh-hans   |
      | content/how-to-setup-in-the-uk/global-entrepreneur-program/                            |
      | content/how-to-setup-in-the-uk/hire-skilled-workers-for-your-uk-operations/            |
      | content/how-to-setup-in-the-uk/open-a-uk-business-bank-account/                        |
      | content/how-to-setup-in-the-uk/register-a-company-in-the-uk/                           |
      | content/how-to-setup-in-the-uk/research-and-development-rd-support-in-the-uk/          |
      | content/how-to-setup-in-the-uk/uk-brexit-guidance-international-business/              |
      | content/how-to-setup-in-the-uk/uk-tax-and-incentives/                                  |
      | content/how-to-setup-in-the-uk/uk-visas-and-migration/                                 |

    Examples: Industries
      | selected                                                                               |
      | content/industries/                                                                    |
      | content/industries/aerospace/                                                          |
      | content/industries/aerospace/?lang=de                                                  |
      | content/industries/aerospace/?lang=es                                                  |
      | content/industries/aerospace/?lang=fr                                                  |
      | content/industries/aerospace/?lang=ja                                                  |
      | content/industries/aerospace/?lang=pt                                                  |
      | content/industries/aerospace/?lang=zh-hans                                             |
      | content/industries/agricultural-technology/                                            |
      | content/industries/agricultural-technology/uk-agritech-strengths/                      |
      | content/industries/automotive/                                                         |
      | content/industries/automotive/?lang=de                                                 |
      | content/industries/automotive/?lang=es                                                 |
      | content/industries/automotive/?lang=fr                                                 |
      | content/industries/automotive/?lang=ja                                                 |
      | content/industries/automotive/?lang=pt                                                 |
      | content/industries/automotive/?lang=zh-hans                                            |
      | content/industries/health-and-life-sciences/                                           |
      | content/industries/technology/                                                         |

    Examples: Invest
      | selected                                                                               |
      | invest/                                                                                |
      | invest/#high-potential-opportunities                                                   |
      | invest/?lang=ar                                                                        |
      | invest/?lang=de                                                                        |
      | invest/?lang=es                                                                        |
      | invest/?lang=fr                                                                        |
      | invest/?lang=ja                                                                        |
      | invest/?lang=pt                                                                        |
      | invest/?lang=zh-hans                                                                   |
      | invest/contact/                                                                        |
      | invest/contact/?lang=de                                                                |
      | invest/contact/?lang=en-gb                                                             |
      | invest/contact/?lang=es                                                                |
      | invest/contact/?lang=fr                                                                |
      | invest/contact/?lang=ja                                                                |
      | invest/contact/?lang=pt                                                                |
      | invest/contact/?lang=zh-hans                                                           |
      | content/invest/high-potential-opportunities/contact/                                   |
      | content/invest/high-potential-opportunities/food-production/                           |
      | content/invest/high-potential-opportunities/lightweight-structures/                    |
      | content/invest/high-potential-opportunities/rail-infrastructure/                       |
      | content/invest/how-to-setup-in-the-uk/                                                 |
      | content/invest/how-to-setup-in-the-uk/?lang=de                                         |
      | content/invest/how-to-setup-in-the-uk/?lang=es                                         |
      | content/invest/how-to-setup-in-the-uk/?lang=fr                                         |
      | content/invest/how-to-setup-in-the-uk/?lang=pt                                         |
      | content/invest/how-to-setup-in-the-uk/?lang=zh-hans                                    |
      | content/invest/how-to-setup-in-the-uk/access-finance-in-the-uk/                        |
      | content/invest/how-to-setup-in-the-uk/access-finance-in-the-uk/?lang=de                |
      | content/invest/how-to-setup-in-the-uk/access-finance-in-the-uk/?lang=es                |
      | content/invest/how-to-setup-in-the-uk/access-finance-in-the-uk/?lang=fr                |
      | content/invest/how-to-setup-in-the-uk/access-finance-in-the-uk/?lang=pt                |
      | content/invest/how-to-setup-in-the-uk/access-finance-in-the-uk/?lang=zh-hans           |
      | content/invest/how-to-setup-in-the-uk/hire-skilled-workers-for-your-uk-operations/     |
      | content/invest/how-to-setup-in-the-uk/open-a-uk-business-bank-account/                 |
      | content/invest/how-to-setup-in-the-uk/open-a-uk-business-bank-account/?lang=es         |
      | content/invest/how-to-setup-in-the-uk/open-a-uk-business-bank-account/?lang=fr         |
      | content/invest/how-to-setup-in-the-uk/open-a-uk-business-bank-account/?lang=pt         |
      | content/invest/how-to-setup-in-the-uk/open-a-uk-business-bank-account/?lang=zh-hans    |
      | content/invest/how-to-setup-in-the-uk/uk-tax-and-incentives/                           |
      | content/invest/how-we-help-you-expand/                                                 |
      | content/invest/uk-regions/midlands/                                                    |
      | content/invest/uk-regions/midlands/?lang=es                                            |
      | content/invest/uk-regions/midlands/?lang=fr                                            |
      | content/invest/uk-regions/midlands/?lang=pt                                            |
      | content/invest/uk-regions/midlands/?lang=zh-hans                                       |
      | content/invest/uk-regions/north-england/                                               |
      | content/invest/uk-regions/north-england/?lang=de                                       |
      | content/invest/uk-regions/north-england/?lang=es                                       |
      | content/invest/uk-regions/north-england/?lang=fr                                       |
      | content/invest/uk-regions/north-england/?lang=ja                                       |
      | content/invest/uk-regions/north-england/?lang=pt                                       |
      | content/invest/uk-regions/north-england/?lang=zh-hans                                  |
      | content/invest/uk-regions/northern-ireland/                                            |
      | content/invest/uk-regions/northern-ireland/?lang=de                                    |
      | content/invest/uk-regions/northern-ireland/?lang=es                                    |
      | content/invest/uk-regions/northern-ireland/?lang=fr                                    |
      | content/invest/uk-regions/northern-ireland/?lang=ja                                    |
      | content/invest/uk-regions/northern-ireland/?lang=pt                                    |
      | content/invest/uk-regions/northern-ireland/?lang=zh-hans                               |
      | content/invest/uk-regions/scotland/                                                    |
      | content/invest/uk-regions/scotland/?lang=de                                            |
      | content/invest/uk-regions/scotland/?lang=es                                            |
      | content/invest/uk-regions/scotland/?lang=fr                                            |
      | content/invest/uk-regions/scotland/?lang=ja                                            |
      | content/invest/uk-regions/scotland/?lang=pt                                            |
      | content/invest/uk-regions/scotland/?lang=zh-hans                                       |
      | content/invest/uk-regions/south-england/                                               |
      | content/invest/uk-regions/south-england/?lang=de                                       |
      | content/invest/uk-regions/south-england/?lang=es                                       |
      | content/invest/uk-regions/south-england/?lang=fr                                       |
      | content/invest/uk-regions/south-england/?lang=ja                                       |
      | content/invest/uk-regions/south-england/?lang=pt                                       |
      | content/invest/uk-regions/south-england/?lang=zh-hans                                  |
      | content/invest/uk-regions/wales/                                                       |
      | content/invest/uk-regions/wales/?lang=de                                               |
      | content/invest/uk-regions/wales/?lang=es                                               |
      | content/invest/uk-regions/wales/?lang=fr                                               |
      | content/invest/uk-regions/wales/?lang=ja                                               |
      | content/invest/uk-regions/wales/?lang=pt                                               |
      | content/invest/uk-regions/wales/?lang=zh-hans                                          |

    Examples: Opportunities
      | selected                                                                               |
      | content/opportunities/                                                                 |
      | content/opportunities/?page=1                                                          |
      | content/opportunities/?page=2                                                          |
      | content/opportunities/?page=3                                                          |
      | content/opportunities/?page=4                                                          |
      | content/opportunities/?page=5                                                          |
      | content/opportunities/?page=6                                                          |
      | content/opportunities/real-estate-advanced-manufacturing-innovation-district-scotland/ |
      | content/opportunities/real-estate-axiom-regional-shopping-centre/                      |
      | content/opportunities/real-estate-bargate-quarter/                                     |
      | content/opportunities/real-estate-belfast-waterside/                                   |
      | content/opportunities/real-estate-bexhill-enterprise-park/                             |
      | content/opportunities/real-estate-bicester-motion/                                     |
      | content/opportunities/real-estate-camro/                                               |
      | content/opportunities/real-estate-central-quay/                                        |
      | content/opportunities/real-estate-corporation-street-and-tomb-street-belfast/          |
      | content/opportunities/real-estate-dundee-waterfront/                                   |
      | content/opportunities/real-estate-edinburgh-bioquarter/                                |
      | content/opportunities/real-estate-edinburgh-international-business-gateway/            |
      | content/opportunities/real-estate-fawley-waterside/                                    |
      | content/opportunities/real-estate-festival-park/                                       |
      | content/opportunities/real-estate-follingsby-max/                                      |
      | content/opportunities/real-estate-forrest-park/                                        |
      | content/opportunities/real-estate-future-carrington/                                   |
      | content/opportunities/real-estate-future-park/                                         |
      | content/opportunities/real-estate-gateshead-quays/                                     |
      | content/opportunities/real-estate-george-street-complex/                               |
      | content/opportunities/real-estate-island-site/                                         |
      | content/opportunities/real-estate-kimmerfields/                                        |
      | content/opportunities/real-estate-kirkstall-forge/                                     |
      | content/opportunities/real-estate-liverpool-waters/                                    |
      | content/opportunities/real-estate-magenta/                                             |
      | content/opportunities/real-estate-mediacityuk/                                         |
      | content/opportunities/real-estate-milford-waterfront/                                  |
      | content/opportunities/real-estate-mira-technology-park-southern-manufacturing-sector/  |
      | content/opportunities/real-estate-mku/                                                 |
      | content/opportunities/real-estate-nells-point-barry-island/                            |
      | content/opportunities/real-estate-north-essex-garden-communities/                      |
      | content/opportunities/real-estate-norwich-union-house/                                 |
      | content/opportunities/real-estate-otterpool-park/                                      |
      | content/opportunities/real-estate-paddington-village/                                  |
      | content/opportunities/real-estate-pall-mall-exchange/                                  |
      | content/opportunities/real-estate-penrhos-coastal-holiday-resort/                      |
      | content/opportunities/real-estate-perth-west/                                          |
      | content/opportunities/real-estate-queen-street/                                        |
      | content/opportunities/real-estate-sixth-building-royal-avenue-belfast/                 |
      | content/opportunities/real-estate-stafford-gateway-north/                              |
      | content/opportunities/real-estate-stockport-exchange/                                  |
      | content/opportunities/real-estate-swansea-central-phase-2/                             |
      | content/opportunities/real-estate-titanic-quarter-belfast/                             |
      | content/opportunities/real-estate-trafford-waters/                                     |
      | content/opportunities/real-estate-uk-central-hub-and-hs2-interchange/                  |
      | content/opportunities/real-estate-unity/                                               |
      | content/opportunities/real-estate-waterside/                                           |
      | content/opportunities/real-estate-weavers-cross/                                       |
      | content/opportunities/real-estate-winter-gardens/                                      |
      | content/opportunities/real-estate-wirral-waters/                                       |
      | content/opportunities/real-estate-wisbech-garden-town/                                 |
      | content/opportunities/real-estate-york-central/                                        |

    Examples: ISD
      | selected                                                                               |
      | investment-support-directory/                                                          |
      | investment-support-directory/?verbose=true                                             |
      | investment-support-directory/search/                                                   |

    Examples: FAS
      | selected                                                                               |
      | trade/                                                                                 |
      | trade/?lang=de                                                                         |
      | trade/?lang=es                                                                         |
      | trade/?lang=fr                                                                         |
      | trade/?lang=ja                                                                         |
      | trade/?lang=pt                                                                         |
      | trade/?lang=zh-hans                                                                    |
      | trade/contact/                                                                         |
      | trade/contact/?lang=ar                                                                 |
      | trade/contact/?lang=de                                                                 |
      | trade/contact/?lang=es                                                                 |
      | trade/contact/?lang=fr                                                                 |
      | trade/contact/?lang=ja                                                                 |
      | trade/contact/?lang=pt                                                                 |
      | trade/contact/?lang=zh-hans
