@decommissioned
@top-importers
Feature: Top importers

  Background:
    Given hawk cookie is set on "Export Readiness - Home" page

  @new-triage
  @ED-2697
  @triage
  @personalised-page
  @services
  Scenario: Service Exporter should NOT see the Top Importer Banner and Top 10 Importers table
    Given "Robert" exports "services"
    And "Robert" answered triage questions

    When "Robert" decides to create his personalised journey page

    Then "Robert" should not see the Top Importer banner and Top 10 Importers table for their sector


  @wip
  @out-of-scope
  @bug
  @ED-3702
  @fixed
  @new-triage
  @ED-2699
  @triage
  @personalised-page
  Scenario Outline: Exporters should NOT see the Top Importer Banner and Top 10 Importers table after changing from exporting "Goods" to Services
    Given "Robert" exports "goods"
    And "Robert" answered triage questions
    And "Robert" decided to create her personalised journey page
    And "Robert" selected the goods category he'd like to export
    And "Robert" can see "Top 10" section on "personalised journey" page

    When "Robert" decides to change the sector to "<specific>" service
    And "Robert" goes through triage again

    Then "Robert" should not see the Top Importer banner and Top 10 Importers table for their sector

    Examples: service sectors
      | specific                                      |
      | Transportation                                |
      | Travel                                        |
      | Communications services                       |
      | Construction services                         |
      | Insurance services                            |
      | Financial services                            |
      | Computer and information services             |
      | Royalties and license fees                    |
      | Other business services                       |
      | Personal, cultural, and recreational services |
      | Government services, n.i.e.                   |


  @out-of-scope
  @bug
  @ED-3702
  @fixed
  @new-triage
  @wip
  @long
  @ED-2696
  @triage
  @personalised-page
  Scenario Outline: Any Exporter should see a Banner and Top importers for their "<specific>" Goods sector
    Given "Robert" exports "goods"
    And "Robert" answered triage questions

    When "Robert" decides to create his personalised journey page
    And "Robert" selects "<specific>" as the goods category he'd like to export

    Then "Robert" should see a Banner and Top importers table for their sector on personalised journey page

    Examples: sectors
      | specific                                                                                                                                                                                                                                  |
      | Animals; live                                                                                                                                                                                                                             |
      | Meat and edible meat offal                                                                                                                                                                                                                |
      | Fish and crustaceans, molluscs and other aquatic invertebrates                                                                                                                                                                            |
      | Dairy produce; birds\' eggs; natural honey; edible products of                                                                                                                                                                            |
      | animal origin, not elsewhere specified or included                                                                                                                                                                                        |
      | Animal originated products; not elsewhere specified or included                                                                                                                                                                           |
      | Trees and other plants, live; bulbs, roots and the like; cut flowers and ornamental foliage                                                                                                                                               |
      | Vegetables and certain roots and tubers; edible                                                                                                                                                                                           |
      | Fruit and nuts, edible; peel of citrus fruit or melons                                                                                                                                                                                    |
      | Coffee, tea, mate and spices                                                                                                                                                                                                              |
      | Cereals                                                                                                                                                                                                                                   |
      | Products of the milling industry; malt, starches, inulin, wheat gluten                                                                                                                                                                    |
      | Oil seeds and oleaginous fruits; miscellaneous grains, seeds and fruit, industrial or medicinal plants; straw and fodder                                                                                                                  |
      | Lac; gums, resins and other vegetable saps and extracts                                                                                                                                                                                   |
      | Vegetable plaiting materials; vegetable products not elsewhere specified or included                                                                                                                                                      |
      | Animal or vegetable fats and oils and their cleavage products; prepared animal fats; animal or vegetable waxes                                                                                                                            |
      | Meat, fish or crustaceans, molluscs or other aquatic invertebrates; preparations thereof                                                                                                                                                  |
      | Sugars and sugar confectionery                                                                                                                                                                                                            |
      | Cocoa and cocoa preparations                                                                                                                                                                                                              |
      | Preparations of cereals, flour, starch or milk; pastrycooks' products                                                                                                                                                                     |
      | Preparations of vegetables, fruit, nuts or other parts of plants                                                                                                                                                                          |
      | Miscellaneous edible preparations                                                                                                                                                                                                         |
      | Beverages, spirits and vinegar                                                                                                                                                                                                            |
      | Food industries, residues and wastes thereof; prepared animal fodder                                                                                                                                                                      |
      | Tobacco and manufactured tobacco substitutes                                                                                                                                                                                              |
      | Salt; sulphur; earths, stone; plastering materials, lime and cement                                                                                                                                                                       |
      | Ores, slag and ash                                                                                                                                                                                                                        |
      | Mineral fuels, mineral oils and products of their distillation; bituminous substances; mineral waxes                                                                                                                                      |
      | Inorganic chemicals; organic and inorganic compounds of precious metals; of rare earth metals, of radio-active elements and of isotopes                                                                                                   |
      | Organic chemicals                                                                                                                                                                                                                         |
      | Pharmaceutical products                                                                                                                                                                                                                   |
      | Fertilizers                                                                                                                                                                                                                               |
      | Tanning or dyeing extracts; tannins and their derivatives; dyes, pigments and other colouring matter; paints, varnishes; putty, other mastics; inks                                                                                       |
      | Essential oils and resinoids; perfumery, cosmetic or toilet preparations                                                                                                                                                                  |
      | Soap, organic surface-active agents; washing, lubricating, polishing or scouring preparations; artificial or prepared waxes, candles and similar articles, modelling pastes, dental waxes and dental preparations with a basis of plaster |
      | Albuminoidal substances; modified starches; glues; enzymes                                                                                                                                                                                |
      | Explosives; pyrotechnic products; matches; pyrophoric alloys; certain combustible preparations                                                                                                                                            |
      | Photographic or cinematographic goods                                                                                                                                                                                                     |
      | Chemical products n.e.c.                                                                                                                                                                                                                  |
      | Plastics and articles thereof                                                                                                                                                                                                             |
      | Rubber and articles thereof                                                                                                                                                                                                               |
      | Raw hides and skins (other than furskins) and leather                                                                                                                                                                                     |
      | Articles of leather; saddlery and harness; travel goods, handbags and similar containers; articles of animal gut (other than silk-worm gut)                                                                                               |
      | Furskins and artificial fur; manufactures thereof                                                                                                                                                                                         |
      | Wood and articles of wood; wood charcoal                                                                                                                                                                                                  |
      | Cork and articles of cork                                                                                                                                                                                                                 |
      | Manufactures of straw, esparto or other plaiting materials; basketware and wickerwork                                                                                                                                                     |
      | Pulp of wood or other fibrous cellulosic material; recovered (waste and scrap) paper or paperboard                                                                                                                                        |
      | Paper and paperboard; articles of paper pulp, of paper or paperboard                                                                                                                                                                      |
      | Printed books, newspapers, pictures and other products of the printing industry; manuscripts, typescripts and plans                                                                                                                       |
      | Silk                                                                                                                                                                                                                                      |
      | Wool, fine or coarse animal hair; horsehair yarn and woven fabric                                                                                                                                                                         |
      | Cotton                                                                                                                                                                                                                                    |
      | Vegetable textile fibres; paper yarn and woven fabrics of paper yarn                                                                                                                                                                      |
      | Man-made filaments; strip and the like of man-made textile materials                                                                                                                                                                      |
      | Man-made staple fibres                                                                                                                                                                                                                    |
      | Wadding, felt and nonwovens, special yarns; twine, cordage, ropes and cables and articles thereof                                                                                                                                         |
      | Carpets and other textile floor coverings                                                                                                                                                                                                 |
      | Fabrics; special woven fabrics, tufted textile fabrics, lace, tapestries, trimmings, embroidery                                                                                                                                           |
      | Textile fabrics; impregnated, coated, covered or laminated; textile articles of a kind suitable for industrial use                                                                                                                        |
      | Fabrics; knitted or crocheted                                                                                                                                                                                                             |
      | Apparel and clothing accessories; knitted or crocheted                                                                                                                                                                                    |
      | Apparel and clothing accessories; not knitted or crocheted                                                                                                                                                                                |
      | Textiles, made up articles; sets; worn clothing and worn textile articles; rags                                                                                                                                                           |
      | Footwear; gaiters and the like; parts of such articles                                                                                                                                                                                    |
      | Headgear and parts thereof                                                                                                                                                                                                                |
      | Umbrellas, sun umbrellas, walking-sticks, seat sticks, whips, riding crops; and parts thereof                                                                                                                                             |
      | Feathers and down, prepared; and articles made of feather or of down; artificial flowers; articles of human hair                                                                                                                          |
      | Stone, plaster, cement, asbestos, mica or similar materials; articles thereof                                                                                                                                                             |
      | Ceramic products                                                                                                                                                                                                                          |
      | Glass and glassware                                                                                                                                                                                                                       |
      | Natural, cultured pearls; precious, semi-precious stones; precious metals, metals clad with precious metal, and articles thereof; imitation jewellery; coin                                                                               |
      | Iron and steel                                                                                                                                                                                                                            |
      | Iron or steel articles                                                                                                                                                                                                                    |
      | Copper and articles thereof                                                                                                                                                                                                               |
      | Nickel and articles thereof                                                                                                                                                                                                               |
      | Aluminium and articles thereof                                                                                                                                                                                                            |
      | Lead and articles thereof                                                                                                                                                                                                                 |
      | Zinc and articles thereof                                                                                                                                                                                                                 |
      | Tin; articles thereof                                                                                                                                                                                                                     |
      | Metals; n.e.c., cermets and articles thereof                                                                                                                                                                                              |
      | Tools, implements, cutlery, spoons and forks, of base metal; parts thereof, of base metal                                                                                                                                                 |
      | Metal; miscellaneous products of base metal                                                                                                                                                                                               |
      | Nuclear reactors, boilers, machinery and mechanical appliances; parts thereof                                                                                                                                                             |
      | Electrical machinery and equipment and parts thereof; sound recorders and reproducers; television image and sound recorders and reproducers, parts and accessories of such articles                                                       |
      | Railway, tramway locomotives, rolling-stock and parts thereof; railway or tramway track fixtures and fittings and parts thereof; mechanical (including electro-mechanical) traffic signalling equipment of all kinds                      |
      | Vehicles; other than railway or tramway rolling stock, and parts and accessories thereof                                                                                                                                                  |
      | Aircraft, spacecraft and parts thereof                                                                                                                                                                                                    |
      | Ships, boats and floating structures                                                                                                                                                                                                      |
      | Optical, photographic, cinematographic, measuring, checking, medical or surgical instruments and apparatus; parts and accessories                                                                                                         |
      | Clocks and watches and parts thereof                                                                                                                                                                                                      |
      | Musical instruments; parts and accessories of such articles                                                                                                                                                                               |
      | Furniture; bedding, mattresses, mattress supports, cushions and similar stuffed furnishings; lamps and lighting fittings, n.e.c.; illuminated signs, illuminated name-plates and the like; prefabricated buildings                        |
      | Toys, games and sports requisites; parts and accessories thereof                                                                                                                                                                          |
      | Miscellaneous manufactured articles                                                                                                                                                                                                       |
      | Works of art; collectors' pieces and antiques                                                                                                                                                                                             |
      | Commodities not specified according to kind                                                                                                                                                                                               |


  @out-of-scope
  @bug
  @ED-3702
  @fixed
  @new-triage
  @wip
  @long
  @ED-2698
  @triage
  @personalised-page
  Scenario Outline: Exporters should see appropriate Banner and Top importers for their sector after updating their Triage preferences
    Given "Robert" exports "services"
    And "Robert" answered triage questions
    And "Robert" decided to create her personalised journey page
    And "Robert" cannot see the Top Importer banner and Top 10 Importers table for their sector

    When "Robert" decides to change the sector to "<specific>" good
    And "Robert" goes through triage again
    And "Robert" selects "<specific>" as the goods category he'd like to export

    Then "Robert" should see a Banner and Top importers table for their sector on personalised journey page

    Examples: sectors
      | specific                                                                                                                                                                                                                                  |
      | Animals; live                                                                                                                                                                                                                             |
      | Meat and edible meat offal                                                                                                                                                                                                                |
      | Fish and crustaceans, molluscs and other aquatic invertebrates                                                                                                                                                                            |
      | Dairy produce; birds\' eggs; natural honey; edible products of                                                                                                                                                                            |
      | animal origin, not elsewhere specified or included                                                                                                                                                                                        |
      | Animal originated products; not elsewhere specified or included                                                                                                                                                                           |
      | Trees and other plants, live; bulbs, roots and the like; cut flowers and ornamental foliage                                                                                                                                               |
      | Vegetables and certain roots and tubers; edible                                                                                                                                                                                           |
      | Fruit and nuts, edible; peel of citrus fruit or melons                                                                                                                                                                                    |
      | Coffee, tea, mate and spices                                                                                                                                                                                                              |
      | Cereals                                                                                                                                                                                                                                   |
      | Products of the milling industry; malt, starches, inulin, wheat gluten                                                                                                                                                                    |
      | Oil seeds and oleaginous fruits; miscellaneous grains, seeds and fruit, industrial or medicinal plants; straw and fodder                                                                                                                  |
      | Lac; gums, resins and other vegetable saps and extracts                                                                                                                                                                                   |
      | Vegetable plaiting materials; vegetable products not elsewhere specified or included                                                                                                                                                      |
      | Animal or vegetable fats and oils and their cleavage products; prepared animal fats; animal or vegetable waxes                                                                                                                            |
      | Meat, fish or crustaceans, molluscs or other aquatic invertebrates; preparations thereof                                                                                                                                                  |
      | Sugars and sugar confectionery                                                                                                                                                                                                            |
      | Cocoa and cocoa preparations                                                                                                                                                                                                              |
      | Preparations of cereals, flour, starch or milk; pastrycooks\' products                                                                                                                                                                    |
      | Preparations of vegetables, fruit, nuts or other parts of plants                                                                                                                                                                          |
      | Miscellaneous edible preparations                                                                                                                                                                                                         |
      | Beverages, spirits and vinegar                                                                                                                                                                                                            |
      | Food industries, residues and wastes thereof; prepared animal fodder                                                                                                                                                                      |
      | Tobacco and manufactured tobacco substitutes                                                                                                                                                                                              |
      | Salt; sulphur; earths, stone; plastering materials, lime and cement                                                                                                                                                                       |
      | Ores, slag and ash                                                                                                                                                                                                                        |
      | Mineral fuels, mineral oils and products of their distillation; bituminous substances; mineral waxes                                                                                                                                      |
      | Inorganic chemicals; organic and inorganic compounds of precious metals; of rare earth metals, of radio-active elements and of isotopes                                                                                                   |
      | Organic chemicals                                                                                                                                                                                                                         |
      | Pharmaceutical products                                                                                                                                                                                                                   |
      | Fertilizers                                                                                                                                                                                                                               |
      | Tanning or dyeing extracts; tannins and their derivatives; dyes, pigments and other colouring matter; paints, varnishes; putty, other mastics; inks                                                                                       |
      | Essential oils and resinoids; perfumery, cosmetic or toilet preparations                                                                                                                                                                  |
      | Soap, organic surface-active agents; washing, lubricating, polishing or scouring preparations; artificial or prepared waxes, candles and similar articles, modelling pastes, dental waxes and dental preparations with a basis of plaster |
      | Albuminoidal substances; modified starches; glues; enzymes                                                                                                                                                                                |
      | Explosives; pyrotechnic products; matches; pyrophoric alloys; certain combustible preparations                                                                                                                                            |
      | Photographic or cinematographic goods                                                                                                                                                                                                     |
      | Chemical products n.e.c.                                                                                                                                                                                                                  |
      | Plastics and articles thereof                                                                                                                                                                                                             |
      | Rubber and articles thereof                                                                                                                                                                                                               |
      | Raw hides and skins (other than furskins) and leather                                                                                                                                                                                     |
      | Articles of leather; saddlery and harness; travel goods, handbags and similar containers; articles of animal gut (other than silk-worm gut)                                                                                               |
      | Furskins and artificial fur; manufactures thereof                                                                                                                                                                                         |
      | Wood and articles of wood; wood charcoal                                                                                                                                                                                                  |
      | Cork and articles of cork                                                                                                                                                                                                                 |
      | Manufactures of straw, esparto or other plaiting materials; basketware and wickerwork                                                                                                                                                     |
      | Pulp of wood or other fibrous cellulosic material; recovered (waste and scrap) paper or paperboard                                                                                                                                        |
      | Paper and paperboard; articles of paper pulp, of paper or paperboard                                                                                                                                                                      |
      | Printed books, newspapers, pictures and other products of the printing industry; manuscripts, typescripts and plans                                                                                                                       |
      | Silk                                                                                                                                                                                                                                      |
      | Wool, fine or coarse animal hair; horsehair yarn and woven fabric                                                                                                                                                                         |
      | Cotton                                                                                                                                                                                                                                    |
      | Vegetable textile fibres; paper yarn and woven fabrics of paper yarn                                                                                                                                                                      |
      | Man-made filaments; strip and the like of man-made textile materials                                                                                                                                                                      |
      | Man-made staple fibres                                                                                                                                                                                                                    |
      | Wadding, felt and nonwovens, special yarns; twine, cordage, ropes and cables and articles thereof                                                                                                                                         |
      | Carpets and other textile floor coverings                                                                                                                                                                                                 |
      | Fabrics; special woven fabrics, tufted textile fabrics, lace, tapestries, trimmings, embroidery                                                                                                                                           |
      | Textile fabrics; impregnated, coated, covered or laminated; textile articles of a kind suitable for industrial use                                                                                                                        |
      | Fabrics; knitted or crocheted                                                                                                                                                                                                             |
      | Apparel and clothing accessories; knitted or crocheted                                                                                                                                                                                    |
      | Apparel and clothing accessories; not knitted or crocheted                                                                                                                                                                                |
      | Textiles, made up articles; sets; worn clothing and worn textile articles; rags                                                                                                                                                           |
      | Footwear; gaiters and the like; parts of such articles                                                                                                                                                                                    |
      | Headgear and parts thereof                                                                                                                                                                                                                |
      | Umbrellas, sun umbrellas, walking-sticks, seat sticks, whips, riding crops; and parts thereof                                                                                                                                             |
      | Feathers and down, prepared; and articles made of feather or of down; artificial flowers; articles of human hair                                                                                                                          |
      | Stone, plaster, cement, asbestos, mica or similar materials; articles thereof                                                                                                                                                             |
      | Ceramic products                                                                                                                                                                                                                          |
      | Glass and glassware                                                                                                                                                                                                                       |
      | Natural, cultured pearls; precious, semi-precious stones; precious metals, metals clad with precious metal, and articles thereof; imitation jewellery; coin                                                                               |
      | Iron and steel                                                                                                                                                                                                                            |
      | Iron or steel articles                                                                                                                                                                                                                    |
      | Copper and articles thereof                                                                                                                                                                                                               |
      | Nickel and articles thereof                                                                                                                                                                                                               |
      | Aluminium and articles thereof                                                                                                                                                                                                            |
      | Lead and articles thereof                                                                                                                                                                                                                 |
      | Zinc and articles thereof                                                                                                                                                                                                                 |
      | Tin; articles thereof                                                                                                                                                                                                                     |
      | Metals; n.e.c., cermets and articles thereof                                                                                                                                                                                              |
      | Tools, implements, cutlery, spoons and forks, of base metal; parts thereof, of base metal                                                                                                                                                 |
      | Metal; miscellaneous products of base metal                                                                                                                                                                                               |
      | Nuclear reactors, boilers, machinery and mechanical appliances; parts thereof                                                                                                                                                             |
      | Electrical machinery and equipment and parts thereof; sound recorders and reproducers; television image and sound recorders and reproducers, parts and accessories of such articles                                                       |
      | Railway, tramway locomotives, rolling-stock and parts thereof; railway or tramway track fixtures and fittings and parts thereof; mechanical (including electro-mechanical) traffic signalling equipment of all kinds                      |
      | Vehicles; other than railway or tramway rolling stock, and parts and accessories thereof                                                                                                                                                  |
      | Aircraft, spacecraft and parts thereof                                                                                                                                                                                                    |
      | Ships, boats and floating structures                                                                                                                                                                                                      |
      | Optical, photographic, cinematographic, measuring, checking, medical or surgical instruments and apparatus; parts and accessories                                                                                                         |
      | Clocks and watches and parts thereof                                                                                                                                                                                                      |
      | Musical instruments; parts and accessories of such articles                                                                                                                                                                               |
      | Furniture; bedding, mattresses, mattress supports, cushions and similar stuffed furnishings; lamps and lighting fittings, n.e.c.; illuminated signs, illuminated name-plates and the like; prefabricated buildings                        |
      | Toys, games and sports requisites; parts and accessories thereof                                                                                                                                                                          |
      | Miscellaneous manufactured articles                                                                                                                                                                                                       |
      | Works of art; collectors\' pieces and antiques                                                                                                                                                                                            |
      | Commodities not specified according to kind                                                                                                                                                                                               |
