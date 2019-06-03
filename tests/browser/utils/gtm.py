from selenium.webdriver.remote.webdriver import WebDriver


def replace_string_representations(dictionary: dict) -> dict:
    result = {}
    for key, value in dictionary.items():
        if value == "None":
            result[key] = None
        elif value == "True":
            result[key] = True
        elif value == "False":
            result[key] = False
        elif value.lower() == "empty string":
            result[key] = ''
        else:
            result[key] = value
    return result


def get_gtm_datalayer_properties(driver: WebDriver) -> dict:
    """
    WebDriver returns datalayer properties formatted like so:
    [
     {
      'event': 'gtm.js',
      'gtm.start': 1559324711826
     },
     {
      'businessUnit': 'International',
      'loginStatus': 'False',
      'siteLanguage': 'en-gb',
      'siteSection': 'Topic',
      'siteSubsection': 'ListingPage',
      'userId': 'None'
     }
    ]
    We're only interested in the seconds item.

    In order to make the result easier to work with, some extra parsing is done.
    Only if a value contains string representation of boolean & None type.
    """
    script_result = driver.execute_script('return window.dataLayer;')

    datalayer_raw = {
        key: value
        for item in script_result
        for key, value in item.items()
        if 'businessUnit' in item
    }

    return replace_string_representations(datalayer_raw)
