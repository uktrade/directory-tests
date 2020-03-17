Feature: Find content differences between Pre-Production and UAT International environments

  Scenario Outline: Content on Pre-Production page "<selected>" should be the same as on respective UAT page
    When you look at the "main" section of the "<selected>" page on "International" "PREPROD" and "UAT"

    Then there should be no differences

    Examples: Landing
      | selected                                  |
      | /                                         |
      | ?lang=de                                  |
      | ?lang=es                                  |
      | ?lang=fr                                  |
      | ?lang=ja                                  |
      | ?lang=pt                                  |
      | ?lang=zh-hans                             |

    Examples: Industries - English
      | selected                                          |
      | content/industries/                               |
      | content/industries/aerospace/                     |
      | content/industries/automotive/                    |
      | content/industries/creative-industries/           |
      | content/industries/education/                     |
      | content/industries/engineering-and-manufacturing/ |
      | content/industries/financial-services/            |
      | content/industries/health-and-life-sciences/      |
      | content/industries/healthcare-and-life-sciences/  |
      | content/industries/legal-services/                |
      | content/industries/space/                         |
      | content/industries/technology/                    |

    Examples: Industries - German
      | selected                                                  |
      | content/industries/?lang=de                               |
      | content/industries/aerospace/?lang=de                     |
      | content/industries/automotive/?lang=de                    |
      | content/industries/creative-industries/?lang=de           |
      | content/industries/education/?lang=de                     |
      | content/industries/engineering-and-manufacturing/?lang=de |
      | content/industries/financial-services/?lang=de            |
      | content/industries/health-and-life-sciences/?lang=de      |
      | content/industries/healthcare-and-life-sciences/?lang=de  |
      | content/industries/legal-services/?lang=de                |
      | content/industries/space/?lang=de                         |
      | content/industries/technology/?lang=de                    |

    Examples: Industries - Spanish
      | selected                                                  |
      | content/industries/?lang=es                               |
      | content/industries/aerospace/?lang=es                     |
      | content/industries/automotive/?lang=es                    |
      | content/industries/creative-industries/?lang=es           |
      | content/industries/education/?lang=es                     |
      | content/industries/engineering-and-manufacturing/?lang=es |
      | content/industries/financial-services/?lang=es            |
      | content/industries/health-and-life-sciences/?lang=es      |
      | content/industries/healthcare-and-life-sciences/?lang=es  |
      | content/industries/legal-services/?lang=es                |
      | content/industries/space/?lang=es                         |
      | content/industries/technology/?lang=es                    |

    Examples: Industries - French
      | selected                                                  |
      | content/industries/?lang=fr                               |
      | content/industries/aerospace/?lang=fr                     |
      | content/industries/automotive/?lang=fr                    |
      | content/industries/creative-industries/?lang=fr           |
      | content/industries/education/?lang=fr                     |
      | content/industries/engineering-and-manufacturing/?lang=fr |
      | content/industries/financial-services/?lang=fr            |
      | content/industries/health-and-life-sciences/?lang=fr      |
      | content/industries/healthcare-and-life-sciences/?lang=fr  |
      | content/industries/legal-services/?lang=fr                |
      | content/industries/space/?lang=fr                         |
      | content/industries/technology/?lang=fr                    |

    Examples: Industries - Japanese
      | selected                                                  |
      | content/industries/?lang=ja                               |
      | content/industries/aerospace/?lang=ja                     |
      | content/industries/automotive/?lang=ja                    |
      | content/industries/creative-industries/?lang=ja           |
      | content/industries/education/?lang=ja                     |
      | content/industries/engineering-and-manufacturing/?lang=ja |
      | content/industries/financial-services/?lang=ja            |
      | content/industries/health-and-life-sciences/?lang=ja      |
      | content/industries/healthcare-and-life-sciences/?lang=ja  |
      | content/industries/legal-services/?lang=ja                |
      | content/industries/space/?lang=ja                         |
      | content/industries/technology/?lang=ja                    |

    Examples: Industries - Portuguese
      | selected                                                  |
      | content/industries/?lang=pt                               |
      | content/industries/aerospace/?lang=pt                     |
      | content/industries/automotive/?lang=pt                    |
      | content/industries/creative-industries/?lang=pt           |
      | content/industries/education/?lang=pt                     |
      | content/industries/engineering-and-manufacturing/?lang=pt |
      | content/industries/financial-services/?lang=pt            |
      | content/industries/health-and-life-sciences/?lang=pt      |
      | content/industries/healthcare-and-life-sciences/?lang=pt  |
      | content/industries/legal-services/?lang=pt                |
      | content/industries/space/?lang=pt                         |
      | content/industries/technology/?lang=pt                    |

    Examples: Industries - Chinese
      | selected                                                       |
      | content/industries/?lang=zh-hans                               |
      | content/industries/aerospace/?lang=zh-hans                     |
      | content/industries/automotive/?lang=zh-hans                    |
      | content/industries/creative-industries/?lang=zh-hans           |
      | content/industries/education/?lang=zh-hans                     |
      | content/industries/engineering-and-manufacturing/?lang=zh-hans |
      | content/industries/financial-services/?lang=zh-hans            |
      | content/industries/health-and-life-sciences/?lang=zh-hans      |
      | content/industries/healthcare-and-life-sciences/?lang=zh-hans  |
      | content/industries/legal-services/?lang=zh-hans                |
      | content/industries/space/?lang=zh-hans                         |
      | content/industries/technology/?lang=zh-hans                    |

    Examples: UK Setup Guide - English
      | selected                                                                      |
      | content/how-to-setup-in-the-uk/                                               |
      | content/how-to-setup-in-the-uk/access-finance-in-the-uk/                      |
      | content/how-to-setup-in-the-uk/establish-a-base-for-business-in-the-uk/       |
      | content/how-to-setup-in-the-uk/hire-skilled-workers-for-your-uk-operations/   |
      | content/how-to-setup-in-the-uk/open-a-uk-business-bank-account/               |
      | content/how-to-setup-in-the-uk/register-a-company-in-the-uk/                  |
      | content/how-to-setup-in-the-uk/research-and-development-rd-support-in-the-uk/ |
      | content/how-to-setup-in-the-uk/uk-tax-and-incentives/                         |
      | content/how-to-setup-in-the-uk/uk-visas-and-migration/                        |

    Examples: UK Setup Guide - German
      | selected                                                                              |
      | content/how-to-setup-in-the-uk/?lang=de                                               |
      | content/how-to-setup-in-the-uk/access-finance-in-the-uk/?lang=de                      |
      | content/how-to-setup-in-the-uk/establish-a-base-for-business-in-the-uk/?lang=de       |
      | content/how-to-setup-in-the-uk/hire-skilled-workers-for-your-uk-operations/?lang=de   |
      | content/how-to-setup-in-the-uk/open-a-uk-business-bank-account/?lang=de               |
      | content/how-to-setup-in-the-uk/register-a-company-in-the-uk/?lang=de                  |
      | content/how-to-setup-in-the-uk/research-and-development-rd-support-in-the-uk/?lang=de |
      | content/how-to-setup-in-the-uk/uk-tax-and-incentives/?lang=de                         |
      | content/how-to-setup-in-the-uk/uk-visas-and-migration/?lang=de                        |

    Examples: UK Setup Guide - Spanish
      | selected                                                                              |
      | content/how-to-setup-in-the-uk/?lang=es                                               |
      | content/how-to-setup-in-the-uk/access-finance-in-the-uk/?lang=es                      |
      | content/how-to-setup-in-the-uk/establish-a-base-for-business-in-the-uk/?lang=es       |
      | content/how-to-setup-in-the-uk/hire-skilled-workers-for-your-uk-operations/?lang=es   |
      | content/how-to-setup-in-the-uk/open-a-uk-business-bank-account/?lang=es               |
      | content/how-to-setup-in-the-uk/register-a-company-in-the-uk/?lang=es                  |
      | content/how-to-setup-in-the-uk/research-and-development-rd-support-in-the-uk/?lang=es |
      | content/how-to-setup-in-the-uk/uk-tax-and-incentives/?lang=es                         |
      | content/how-to-setup-in-the-uk/uk-visas-and-migration/?lang=es                        |

    Examples: UK Setup Guide - French
      | selected                                                                              |
      | content/how-to-setup-in-the-uk/?lang=fr                                               |
      | content/how-to-setup-in-the-uk/access-finance-in-the-uk/?lang=fr                      |
      | content/how-to-setup-in-the-uk/establish-a-base-for-business-in-the-uk/?lang=fr       |
      | content/how-to-setup-in-the-uk/hire-skilled-workers-for-your-uk-operations/?lang=fr   |
      | content/how-to-setup-in-the-uk/open-a-uk-business-bank-account/?lang=fr               |
      | content/how-to-setup-in-the-uk/register-a-company-in-the-uk/?lang=fr                  |
      | content/how-to-setup-in-the-uk/research-and-development-rd-support-in-the-uk/?lang=fr |
      | content/how-to-setup-in-the-uk/uk-tax-and-incentives/?lang=fr                         |
      | content/how-to-setup-in-the-uk/uk-visas-and-migration/?lang=fr                        |

    Examples: UK Setup Guide - Japanese
      | selected                                                                              |
      | content/how-to-setup-in-the-uk/?lang=ja                                               |
      | content/how-to-setup-in-the-uk/access-finance-in-the-uk/?lang=ja                      |
      | content/how-to-setup-in-the-uk/establish-a-base-for-business-in-the-uk/?lang=ja       |
      | content/how-to-setup-in-the-uk/hire-skilled-workers-for-your-uk-operations/?lang=ja   |
      | content/how-to-setup-in-the-uk/open-a-uk-business-bank-account/?lang=ja               |
      | content/how-to-setup-in-the-uk/register-a-company-in-the-uk/?lang=ja                  |
      | content/how-to-setup-in-the-uk/research-and-development-rd-support-in-the-uk/?lang=ja |
      | content/how-to-setup-in-the-uk/uk-tax-and-incentives/?lang=ja                         |
      | content/how-to-setup-in-the-uk/uk-visas-and-migration/?lang=ja                        |

    Examples: UK Setup Guide - Portuguese
      | selected                                                                              |
      | content/how-to-setup-in-the-uk/?lang=pt                                               |
      | content/how-to-setup-in-the-uk/access-finance-in-the-uk/?lang=pt                      |
      | content/how-to-setup-in-the-uk/establish-a-base-for-business-in-the-uk/?lang=pt       |
      | content/how-to-setup-in-the-uk/hire-skilled-workers-for-your-uk-operations/?lang=pt   |
      | content/how-to-setup-in-the-uk/open-a-uk-business-bank-account/?lang=pt               |
      | content/how-to-setup-in-the-uk/register-a-company-in-the-uk/?lang=pt                  |
      | content/how-to-setup-in-the-uk/research-and-development-rd-support-in-the-uk/?lang=pt |
      | content/how-to-setup-in-the-uk/uk-tax-and-incentives/?lang=pt                         |
      | content/how-to-setup-in-the-uk/uk-visas-and-migration/?lang=pt                        |

    Examples: UK Setup Guide - Chinese
      | selected                                                                                   |
      | content/how-to-setup-in-the-uk/?lang=zh-hans                                               |
      | content/how-to-setup-in-the-uk/access-finance-in-the-uk/?lang=zh-hans                      |
      | content/how-to-setup-in-the-uk/establish-a-base-for-business-in-the-uk/?lang=zh-hans       |
      | content/how-to-setup-in-the-uk/hire-skilled-workers-for-your-uk-operations/?lang=zh-hans   |
      | content/how-to-setup-in-the-uk/open-a-uk-business-bank-account/?lang=zh-hans               |
      | content/how-to-setup-in-the-uk/register-a-company-in-the-uk/?lang=zh-hans                  |
      | content/how-to-setup-in-the-uk/research-and-development-rd-support-in-the-uk/?lang=zh-hans |
      | content/how-to-setup-in-the-uk/uk-tax-and-incentives/?lang=zh-hans                         |
      | content/how-to-setup-in-the-uk/uk-visas-and-migration/?lang=zh-hans                        |
