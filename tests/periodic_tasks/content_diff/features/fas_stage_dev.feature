Feature: Find content differences between Stage and Dev FAS environments

  Scenario Outline: Content on Dev page "<selected>" should be the same as on respective Production page
    When you look at the "main" section of the "<selected>" page on "FAS" "STAGE" and "DEV"

    Then there should be no differences

    Examples: home page
      | selected      |
      | /             |
      | ?lang=ar      |
      | ?lang=de      |
      | ?lang=en-gb   |
      | ?lang=es      |
      | ?lang=fr      |
      | ?lang=ja      |
      | ?lang=pt      |
      | ?lang=pt-br   |
      | ?lang=ru      |
      | ?lang=zh-hans |

    Examples: feedback page
      | selected               |
      | feedback/              |
      | feedback/?lang=ar      |
      | feedback/?lang=de      |
      | feedback/?lang=en-gb   |
      | feedback/?lang=es      |
      | feedback/?lang=fr      |
      | feedback/?lang=ja      |
      | feedback/?lang=pt      |
      | feedback/?lang=pt-br   |
      | feedback/?lang=ru      |
      | feedback/?lang=zh-hans |

    Examples: Industries page
      | selected                 |
      | industries/              |
      | industries/?lang=ar      |
      | industries/?lang=de      |
      | industries/?lang=en-gb   |
      | industries/?lang=es      |
      | industries/?lang=fr      |
      | industries/?lang=ja      |
      | industries/?lang=pt      |
      | industries/?lang=pt-br   |
      | industries/?lang=ru      |
      | industries/?lang=zh-hans |

    Examples: Industry pages
      | selected                                   |
      | industries/aerospace/                      |
      | industries/aerospace/?lang=ar              |
      | industries/aerospace/?lang=de              |
      | industries/aerospace/?lang=en-gb           |
      | industries/aerospace/?lang=es              |
      | industries/aerospace/?lang=fr              |
      | industries/aerospace/?lang=ja              |
      | industries/aerospace/?lang=pt              |
      | industries/aerospace/?lang=pt-br           |
      | industries/aerospace/?lang=ru              |
      | industries/aerospace/?lang=zh-hans         |
      | industries/agritech/                       |
      | industries/agritech/?lang=ar               |
      | industries/agritech/?lang=de               |
      | industries/agritech/?lang=en-gb            |
      | industries/agritech/?lang=es               |
      | industries/agritech/?lang=fr               |
      | industries/agritech/?lang=ja               |
      | industries/agritech/?lang=pt               |
      | industries/agritech/?lang=pt-br            |
      | industries/agritech/?lang=ru               |
      | industries/agritech/?lang=zh-hans          |
      | industries/consumer-retail/                |
      | industries/consumer-retail/?lang=ar        |
      | industries/consumer-retail/?lang=de        |
      | industries/consumer-retail/?lang=en-gb     |
      | industries/consumer-retail/?lang=es        |
      | industries/consumer-retail/?lang=fr        |
      | industries/consumer-retail/?lang=ja        |
      | industries/consumer-retail/?lang=pt        |
      | industries/consumer-retail/?lang=pt-br     |
      | industries/consumer-retail/?lang=ru        |
      | industries/consumer-retail/?lang=zh-hans   |
      | industries/creative-services/              |
      | industries/creative-services/?lang=ar      |
      | industries/creative-services/?lang=de      |
      | industries/creative-services/?lang=en-gb   |
      | industries/creative-services/?lang=es      |
      | industries/creative-services/?lang=fr      |
      | industries/creative-services/?lang=ja      |
      | industries/creative-services/?lang=pt      |
      | industries/creative-services/?lang=pt-br   |
      | industries/creative-services/?lang=ru      |
      | industries/creative-services/?lang=zh-hans |
      | industries/cyber-security/                 |
      | industries/cyber-security/?lang=ar         |
      | industries/cyber-security/?lang=de         |
      | industries/cyber-security/?lang=en-gb      |
      | industries/cyber-security/?lang=es         |
      | industries/cyber-security/?lang=fr         |
      | industries/cyber-security/?lang=ja         |
      | industries/cyber-security/?lang=pt         |
      | industries/cyber-security/?lang=pt-br      |
      | industries/cyber-security/?lang=ru         |
      | industries/cyber-security/?lang=zh-hans    |
      | industries/food-and-drink/                 |
      | industries/food-and-drink/?lang=ar         |
      | industries/food-and-drink/?lang=de         |
      | industries/food-and-drink/?lang=en-gb      |
      | industries/food-and-drink/?lang=es         |
      | industries/food-and-drink/?lang=fr         |
      | industries/food-and-drink/?lang=ja         |
      | industries/food-and-drink/?lang=pt         |
      | industries/food-and-drink/?lang=pt-br      |
      | industries/food-and-drink/?lang=ru         |
      | industries/food-and-drink/?lang=zh-hans    |
      | industries/healthcare/                     |
      | industries/healthcare/?lang=ar             |
      | industries/healthcare/?lang=de             |
      | industries/healthcare/?lang=en-gb          |
      | industries/healthcare/?lang=es             |
      | industries/healthcare/?lang=fr             |
      | industries/healthcare/?lang=ja             |
      | industries/healthcare/?lang=pt             |
      | industries/healthcare/?lang=pt-br          |
      | industries/healthcare/?lang=ru             |
      | industries/healthcare/?lang=zh-hans        |
      | industries/legal-services/                 |
      | industries/legal-services/?lang=ar         |
      | industries/legal-services/?lang=de         |
      | industries/legal-services/?lang=en-gb      |
      | industries/legal-services/?lang=es         |
      | industries/legal-services/?lang=fr         |
      | industries/legal-services/?lang=ja         |
      | industries/legal-services/?lang=pt         |
      | industries/legal-services/?lang=pt-br      |
      | industries/legal-services/?lang=ru         |
      | industries/legal-services/?lang=zh-hans    |
      | industries/life-sciences/                  |
      | industries/life-sciences/?lang=ar          |
      | industries/life-sciences/?lang=de          |
      | industries/life-sciences/?lang=en-gb       |
      | industries/life-sciences/?lang=es          |
      | industries/life-sciences/?lang=fr          |
      | industries/life-sciences/?lang=ja          |
      | industries/life-sciences/?lang=pt          |
      | industries/life-sciences/?lang=pt-br       |
      | industries/life-sciences/?lang=ru          |
      | industries/life-sciences/?lang=zh-hans     |
      | industries/sports-economy/                 |
      | industries/sports-economy/?lang=ar         |
      | industries/sports-economy/?lang=de         |
      | industries/sports-economy/?lang=en-gb      |
      | industries/sports-economy/?lang=es         |
      | industries/sports-economy/?lang=fr         |
      | industries/sports-economy/?lang=ja         |
      | industries/sports-economy/?lang=pt         |
      | industries/sports-economy/?lang=pt-br      |
      | industries/sports-economy/?lang=ru         |
      | industries/sports-economy/?lang=zh-hans    |
      | industries/technology/                     |
      | industries/technology/?lang=ar             |
      | industries/technology/?lang=de             |
      | industries/technology/?lang=en-gb          |
      | industries/technology/?lang=es             |
      | industries/technology/?lang=fr             |
      | industries/technology/?lang=ja             |
      | industries/technology/?lang=pt             |
      | industries/technology/?lang=pt-br          |
      | industries/technology/?lang=ru             |
      | industries/technology/?lang=zh-hans        |

    Examples: Industry article pages
      | selected                                                                 |
      | industry-articles/UK-agritech-strengths/                                 |
      | industry-articles/UK-agritech-strengths/?lang=ar                         |
      | industry-articles/UK-agritech-strengths/?lang=de                         |
      | industry-articles/UK-agritech-strengths/?lang=en-gb                      |
      | industry-articles/UK-agritech-strengths/?lang=es                         |
      | industry-articles/UK-agritech-strengths/?lang=fr                         |
      | industry-articles/UK-agritech-strengths/?lang=ja                         |
      | industry-articles/UK-agritech-strengths/?lang=pt                         |
      | industry-articles/UK-agritech-strengths/?lang=pt-br                      |
      | industry-articles/UK-agritech-strengths/?lang=ru                         |
      | industry-articles/UK-agritech-strengths/?lang=zh-hans                    |
      | industry-articles/a-global-centre-for-life-sciences/                     |
      | industry-articles/a-global-centre-for-life-sciences/?lang=ar             |
      | industry-articles/a-global-centre-for-life-sciences/?lang=de             |
      | industry-articles/a-global-centre-for-life-sciences/?lang=en-gb          |
      | industry-articles/a-global-centre-for-life-sciences/?lang=es             |
      | industry-articles/a-global-centre-for-life-sciences/?lang=fr             |
      | industry-articles/a-global-centre-for-life-sciences/?lang=ja             |
      | industry-articles/a-global-centre-for-life-sciences/?lang=pt             |
      | industry-articles/a-global-centre-for-life-sciences/?lang=pt-br          |
      | industry-articles/a-global-centre-for-life-sciences/?lang=ru             |
      | industry-articles/a-global-centre-for-life-sciences/?lang=zh-hans        |
      | industry-articles/highly-rated-primary-care/                             |
      | industry-articles/highly-rated-primary-care/?lang=ar                     |
      | industry-articles/highly-rated-primary-care/?lang=de                     |
      | industry-articles/highly-rated-primary-care/?lang=en-gb                  |
      | industry-articles/highly-rated-primary-care/?lang=es                     |
      | industry-articles/highly-rated-primary-care/?lang=fr                     |
      | industry-articles/highly-rated-primary-care/?lang=ja                     |
      | industry-articles/highly-rated-primary-care/?lang=pt                     |
      | industry-articles/highly-rated-primary-care/?lang=pt-br                  |
      | industry-articles/highly-rated-primary-care/?lang=ru                     |
      | industry-articles/highly-rated-primary-care/?lang=zh-hans                |
      | industry-articles/leading-the-world-in-cancer-care/                      |
      | industry-articles/leading-the-world-in-cancer-care/?lang=ar              |
      | industry-articles/leading-the-world-in-cancer-care/?lang=de              |
      | industry-articles/leading-the-world-in-cancer-care/?lang=en-gb           |
      | industry-articles/leading-the-world-in-cancer-care/?lang=es              |
      | industry-articles/leading-the-world-in-cancer-care/?lang=fr              |
      | industry-articles/leading-the-world-in-cancer-care/?lang=ja              |
      | industry-articles/leading-the-world-in-cancer-care/?lang=pt              |
      | industry-articles/leading-the-world-in-cancer-care/?lang=pt-br           |
      | industry-articles/leading-the-world-in-cancer-care/?lang=ru              |
      | industry-articles/leading-the-world-in-cancer-care/?lang=zh-hans         |
      | industry-articles/life-changing-artificial-intelligence-AI/              |
      | industry-articles/life-changing-artificial-intelligence-AI/?lang=ar      |
      | industry-articles/life-changing-artificial-intelligence-AI/?lang=de      |
      | industry-articles/life-changing-artificial-intelligence-AI/?lang=en-gb   |
      | industry-articles/life-changing-artificial-intelligence-AI/?lang=es      |
      | industry-articles/life-changing-artificial-intelligence-AI/?lang=fr      |
      | industry-articles/life-changing-artificial-intelligence-AI/?lang=ja      |
      | industry-articles/life-changing-artificial-intelligence-AI/?lang=pt      |
      | industry-articles/life-changing-artificial-intelligence-AI/?lang=pt-br   |
      | industry-articles/life-changing-artificial-intelligence-AI/?lang=ru      |
      | industry-articles/life-changing-artificial-intelligence-AI/?lang=zh-hans |
      | industry-articles/the-changing-face-of-visual-effects/                   |
      | industry-articles/the-changing-face-of-visual-effects/?lang=ar           |
      | industry-articles/the-changing-face-of-visual-effects/?lang=de           |
      | industry-articles/the-changing-face-of-visual-effects/?lang=en-gb        |
      | industry-articles/the-changing-face-of-visual-effects/?lang=es           |
      | industry-articles/the-changing-face-of-visual-effects/?lang=fr           |
      | industry-articles/the-changing-face-of-visual-effects/?lang=ja           |
      | industry-articles/the-changing-face-of-visual-effects/?lang=pt           |
      | industry-articles/the-changing-face-of-visual-effects/?lang=pt-br        |
      | industry-articles/the-changing-face-of-visual-effects/?lang=ru           |
      | industry-articles/the-changing-face-of-visual-effects/?lang=zh-hans      |
      | industry-articles/uk-centres-of-excellence/                              |
      | industry-articles/uk-centres-of-excellence/?lang=ar                      |
      | industry-articles/uk-centres-of-excellence/?lang=de                      |
      | industry-articles/uk-centres-of-excellence/?lang=en-gb                   |
      | industry-articles/uk-centres-of-excellence/?lang=es                      |
      | industry-articles/uk-centres-of-excellence/?lang=fr                      |
      | industry-articles/uk-centres-of-excellence/?lang=ja                      |
      | industry-articles/uk-centres-of-excellence/?lang=pt                      |
      | industry-articles/uk-centres-of-excellence/?lang=pt-br                   |
      | industry-articles/uk-centres-of-excellence/?lang=ru                      |
      | industry-articles/uk-centres-of-excellence/?lang=zh-hans                 |
      | industry-articles/uk-cyber-security-hubs/                                |
      | industry-articles/uk-cyber-security-hubs/?lang=ar                        |
      | industry-articles/uk-cyber-security-hubs/?lang=de                        |
      | industry-articles/uk-cyber-security-hubs/?lang=en-gb                     |
      | industry-articles/uk-cyber-security-hubs/?lang=es                        |
      | industry-articles/uk-cyber-security-hubs/?lang=fr                        |
      | industry-articles/uk-cyber-security-hubs/?lang=ja                        |
      | industry-articles/uk-cyber-security-hubs/?lang=pt                        |
      | industry-articles/uk-cyber-security-hubs/?lang=pt-br                     |
      | industry-articles/uk-cyber-security-hubs/?lang=ru                        |
      | industry-articles/uk-cyber-security-hubs/?lang=zh-hans                   |

    Examples: Contact us pages
      | selected                         |
      | industries/contact/              |
      | industries/contact/?lang=ar      |
      | industries/contact/?lang=de      |
      | industries/contact/?lang=en-gb   |
      | industries/contact/?lang=es      |
      | industries/contact/?lang=fr      |
      | industries/contact/?lang=ja      |
      | industries/contact/?lang=pt      |
      | industries/contact/?lang=pt-br   |
      | industries/contact/?lang=ru      |
      | industries/contact/?lang=zh-hans |

    Examples: Industry - Contact us pages
      | selected                                           |
      | industries/contact/aerospace/                      |
      | industries/contact/aerospace/?lang=ar              |
      | industries/contact/aerospace/?lang=de              |
      | industries/contact/aerospace/?lang=en-gb           |
      | industries/contact/aerospace/?lang=es              |
      | industries/contact/aerospace/?lang=fr              |
      | industries/contact/aerospace/?lang=ja              |
      | industries/contact/aerospace/?lang=pt              |
      | industries/contact/aerospace/?lang=pt-br           |
      | industries/contact/aerospace/?lang=ru              |
      | industries/contact/aerospace/?lang=zh-hans         |
      | industries/contact/agritech/                       |
      | industries/contact/agritech/?lang=ar               |
      | industries/contact/agritech/?lang=de               |
      | industries/contact/agritech/?lang=en-gb            |
      | industries/contact/agritech/?lang=es               |
      | industries/contact/agritech/?lang=fr               |
      | industries/contact/agritech/?lang=ja               |
      | industries/contact/agritech/?lang=pt               |
      | industries/contact/agritech/?lang=pt-br            |
      | industries/contact/agritech/?lang=ru               |
      | industries/contact/agritech/?lang=zh-hans          |
      | industries/contact/consumer-retail/                |
      | industries/contact/consumer-retail/?lang=ar        |
      | industries/contact/consumer-retail/?lang=de        |
      | industries/contact/consumer-retail/?lang=en-gb     |
      | industries/contact/consumer-retail/?lang=es        |
      | industries/contact/consumer-retail/?lang=fr        |
      | industries/contact/consumer-retail/?lang=ja        |
      | industries/contact/consumer-retail/?lang=pt        |
      | industries/contact/consumer-retail/?lang=pt-br     |
      | industries/contact/consumer-retail/?lang=ru        |
      | industries/contact/consumer-retail/?lang=zh-hans   |
      | industries/contact/creative-services/              |
      | industries/contact/creative-services/?lang=ar      |
      | industries/contact/creative-services/?lang=de      |
      | industries/contact/creative-services/?lang=en-gb   |
      | industries/contact/creative-services/?lang=es      |
      | industries/contact/creative-services/?lang=fr      |
      | industries/contact/creative-services/?lang=ja      |
      | industries/contact/creative-services/?lang=pt      |
      | industries/contact/creative-services/?lang=pt-br   |
      | industries/contact/creative-services/?lang=ru      |
      | industries/contact/creative-services/?lang=zh-hans |
      | industries/contact/cyber-security/                 |
      | industries/contact/cyber-security/?lang=ar         |
      | industries/contact/cyber-security/?lang=de         |
      | industries/contact/cyber-security/?lang=en-gb      |
      | industries/contact/cyber-security/?lang=es         |
      | industries/contact/cyber-security/?lang=fr         |
      | industries/contact/cyber-security/?lang=ja         |
      | industries/contact/cyber-security/?lang=pt         |
      | industries/contact/cyber-security/?lang=pt-br      |
      | industries/contact/cyber-security/?lang=ru         |
      | industries/contact/cyber-security/?lang=zh-hans    |
      | industries/contact/food-and-drink/                 |
      | industries/contact/food-and-drink/?lang=ar         |
      | industries/contact/food-and-drink/?lang=de         |
      | industries/contact/food-and-drink/?lang=en-gb      |
      | industries/contact/food-and-drink/?lang=es         |
      | industries/contact/food-and-drink/?lang=fr         |
      | industries/contact/food-and-drink/?lang=ja         |
      | industries/contact/food-and-drink/?lang=pt         |
      | industries/contact/food-and-drink/?lang=pt-br      |
      | industries/contact/food-and-drink/?lang=ru         |
      | industries/contact/food-and-drink/?lang=zh-hans    |
      | industries/contact/healthcare/                     |
      | industries/contact/healthcare/?lang=ar             |
      | industries/contact/healthcare/?lang=de             |
      | industries/contact/healthcare/?lang=en-gb          |
      | industries/contact/healthcare/?lang=es             |
      | industries/contact/healthcare/?lang=fr             |
      | industries/contact/healthcare/?lang=ja             |
      | industries/contact/healthcare/?lang=pt             |
      | industries/contact/healthcare/?lang=pt-br          |
      | industries/contact/healthcare/?lang=ru             |
      | industries/contact/healthcare/?lang=zh-hans        |
      | industries/contact/legal-services/                 |
      | industries/contact/legal-services/?lang=ar         |
      | industries/contact/legal-services/?lang=de         |
      | industries/contact/legal-services/?lang=en-gb      |
      | industries/contact/legal-services/?lang=es         |
      | industries/contact/legal-services/?lang=fr         |
      | industries/contact/legal-services/?lang=ja         |
      | industries/contact/legal-services/?lang=pt         |
      | industries/contact/legal-services/?lang=pt-br      |
      | industries/contact/legal-services/?lang=ru         |
      | industries/contact/legal-services/?lang=zh-hans    |
      | industries/contact/life-sciences/                  |
      | industries/contact/life-sciences/?lang=ar          |
      | industries/contact/life-sciences/?lang=de          |
      | industries/contact/life-sciences/?lang=en-gb       |
      | industries/contact/life-sciences/?lang=es          |
      | industries/contact/life-sciences/?lang=fr          |
      | industries/contact/life-sciences/?lang=ja          |
      | industries/contact/life-sciences/?lang=pt          |
      | industries/contact/life-sciences/?lang=pt-br       |
      | industries/contact/life-sciences/?lang=ru          |
      | industries/contact/life-sciences/?lang=zh-hans     |
      | industries/contact/sports-economy/                 |
      | industries/contact/sports-economy/?lang=ar         |
      | industries/contact/sports-economy/?lang=de         |
      | industries/contact/sports-economy/?lang=en-gb      |
      | industries/contact/sports-economy/?lang=es         |
      | industries/contact/sports-economy/?lang=fr         |
      | industries/contact/sports-economy/?lang=ja         |
      | industries/contact/sports-economy/?lang=pt         |
      | industries/contact/sports-economy/?lang=pt-br      |
      | industries/contact/sports-economy/?lang=ru         |
      | industries/contact/sports-economy/?lang=zh-hans    |
      | industries/contact/technology/                     |
      | industries/contact/technology/?lang=ar             |
      | industries/contact/technology/?lang=de             |
      | industries/contact/technology/?lang=en-gb          |
      | industries/contact/technology/?lang=es             |
      | industries/contact/technology/?lang=fr             |
      | industries/contact/technology/?lang=ja             |
      | industries/contact/technology/?lang=pt             |
      | industries/contact/technology/?lang=pt-br          |
      | industries/contact/technology/?lang=ru             |
      | industries/contact/technology/?lang=zh-hans        |
