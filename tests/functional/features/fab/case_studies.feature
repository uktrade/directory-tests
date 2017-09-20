Feature: Case Studies


  @ED-2142
  @fab
  @case-study
  @profile
  Scenario: Supplier should not be able to use invalid values when adding a case study
    Given "Peter Alder" created an unverified profile for randomly selected company "Y"

    When "Peter Alder" attempts to add a case study using following values
      |field         |value type      |separator |error                                                                                |
      |title         |61 characters   |          |Ensure this value has at most 60 characters (it has 61).                             |
      |title         |empty string    |          |This field is required.                                                              |
      |summary       |201 characters  |          |Ensure this value has at most 200 characters (it has 201).                           |
      |summary       |empty string    |          |This field is required.                                                              |
      |description   |1001 characters |          |Ensure this value has at most 1000 characters (it has 1001).                         |
      |description   |empty string    |          |This field is required.                                                              |
      |sector        |invalid sector  |          |Select a valid choice. this is an invalid sector is not one of the available choices.|
      |website       |256 characters  |          |Enter a valid URL.                                                                   |
      |keywords      |book, keys, food|pipe      |You can only enter letters, numbers and commas.                                      |
      |keywords      |book, keys, food|semi-colon|You can only enter letters, numbers and commas.                                      |
      |keywords      |book, keys, food|colon     |You can only enter letters, numbers and commas.                                      |
      |keywords      |book, keys, food|full stop |You can only enter letters, numbers and commas.                                      |
      |keywords      |empty string    |          |This field is required.                                                              |
      |image_1       |invalid image   |          |Invalid image format, allowed formats: PNG, JPG, JPEG                                |
      |image_1       |no image        |          |This field is required.                                                              |
      |caption_1     |121 characters  |          |Ensure this value has at most 120 characters (it has 121).                           |
      |caption_1     |empty string    |          |This field is required.                                                              |
      |image_2       |invalid image   |          |Invalid image format, allowed formats: PNG, JPG, JPEG                                |
      |caption_2     |121 characters  |          |Ensure this value has at most 120 characters (it has 121).                           |
      |image_3       |invalid image   |          |Invalid image format, allowed formats: PNG, JPG, JPEG                                |
      |caption_3     |121 characters  |          |Ensure this value has at most 120 characters (it has 121).                           |
      |testimonial   |1001 characters |          |Ensure this value has at most 1000 characters (it has 1001).                         |
      |source_name   |256 characters  |          |Ensure this value has at most 255 characters (it has 256).                           |
      |source_job    |256 characters  |          |Ensure this value has at most 255 characters (it has 256).                           |
      |source_company|256 characters  |          |Ensure this value has at most 255 characters (it has 256).                           |

    Then "Peter Alder" should see expected case study error message


  @ED-2142
  @fab
  @case-study
  @profile
  @bug
  @ED-2248
  @fixme
  Scenario: Supplier should not be able to use invalid values when adding a case study
    Given "Peter Alder" created an unverified profile for randomly selected company "Y"

    When "Peter Alder" attempts to add a case study using following values
      |field         |value type      |separator |error             |
      |website       |invalid http    |          |Enter a valid URL.|
      |website       |invalid https   |          |Enter a valid URL.|

    Then "Peter Alder" should see expected case study error message