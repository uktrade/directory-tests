Feature: Case Studies


  @ED-2142
  @fab
  @case-study
  @profile
  Scenario: Supplier should not be able to use invalid values when adding a case study
    Given "Peter Alder" created an unverified profile for randomly selected company "Y"

    When "Peter Alder" attempts to add a case study using following values
      |field         |value type      |separator |error                                                   |
      |title         |61 characters   |          |Ensure this value has at most 60 characters (it has 61).|
      |summary       |51 words        |          |Ensure this value has at most 60 characters (it has 61).|
      |description   |101 characters  |          |Ensure this value has at most 60 characters (it has 61).|
      |sector        |invalid sector  |          |Ensure this value has at most 60 characters (it has 61).|
      |website       |invalid http    |          |Ensure this value has at most 60 characters (it has 61).|
      |keywords      |book, keys, food|pipe      |Ensure this value has at most 60 characters (it has 61).|
      |keywords      |book, keys, food|semi-colon|Ensure this value has at most 60 characters (it has 61).|
      |keywords      |book, keys, food|colon     |Ensure this value has at most 60 characters (it has 61).|
      |keywords      |book, keys, food|full stop |Ensure this value has at most 60 characters (it has 61).|
      |keywords      |empty string    |          |Ensure this value has at most 60 characters (it has 61).|
      |image_1       |invalid image   |          |Ensure this value has at most 60 characters (it has 61).|
      |caption_1     |999 characters  |          |Ensure this value has at most 60 characters (it has 61).|
      |caption_1     |empty string    |          |Ensure this value has at most 60 characters (it has 61).|
      |image_2       |invalid image   |          |Ensure this value has at most 60 characters (it has 61).|
      |caption_2     |999 characters  |          |Ensure this value has at most 60 characters (it has 61).|
      |image_3       |invalid image   |          |Ensure this value has at most 60 characters (it has 61).|
      |caption_3     |999 characters  |          |Ensure this value has at most 60 characters (it has 61).|
      |testimonial   |999 characters  |          |Ensure this value has at most 60 characters (it has 61).|
      |source_name   |999 characters  |          |Ensure this value has at most 60 characters (it has 61).|
      |source_job    |999 characters  |          |Ensure this value has at most 60 characters (it has 61).|
      |source_company|999 characters  |          |Ensure this value has at most 60 characters (it has 61).|

    Then "Peter Alder" should see expected case study error message