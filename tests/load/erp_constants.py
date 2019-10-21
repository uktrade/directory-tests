# -*- coding: utf-8 -*-
import json

from directory_constants import choices

UK_BUSINESS = "UK_BUSINESS"
UK_CONSUMER = "UK_CONSUMER"
DEVELOPING_COUNTRY_COMPANY = "DEVELOPING_COUNTRY_COMPANY"

INCREASE = "INCREASE"
DECREASE = "DECREASE"
QUOTA_CHANGE = "QUOTA_CHANGE"
OTHER = "OTHER"

ACTUAL = "ACTUAL"
EXPECTED = "EXPECTED"

GENERALISED_SYSTEM_OF_PERFERENCE_COUNTRIES = (
    "Afghanistan",
    "Angola",
    "Armenia",
    "Bangladesh",
    "Benin",
    "Bhutan",
    "Bolivia",
    "Burkina Faso",
    "Burma",
    "Burundi",
    "Cambodia",
    "Cameroon",
    "Cape Verde",
    "Central African Republic",
    "Chad",
    "Comoros",
    "Congo",
    "Cook Islands",
    "Djibouti",
    "East Timor",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Ethiopia",
    "Gambia (The)",
    "Georgia",
    "Ghana",
    "Guatemala",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Honduras",
    "India",
    "Indonesia",
    "Ivory Coast",
    "Jordan",
    "Kenya",
    "Kiribati",
    "Kosovo",
    "Kyrgyzstan",
    "Laos",
    "Lesotho",
    "Liberia",
    "Madagascar",
    "Malawi",
    "Mali",
    "Mauritania",
    "Micronesia",
    "Moldova",
    "Mongolia",
    "Morocco",
    "Mozambique",
    "Nauru",
    "Nepal",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "Niue",
    "Occupied Palestinian Territories",
    "Pakistan",
    "Papua New Guinea",
    "Philippines",
    "Rwanda",
    "Samoa",
    "Sao Tome and Principe",
    "Senegal",
    "Sierra Leone",
    "Solomon Islands",
    "Somalia",
    "South Sudan",
    "Sri Lanka",
    "Sudan",
    "Swaziland",
    "Syria",
    "Tajikistan",
    "Tanzania",
    "Togo",
    "Tonga",
    "Tunisia",
    "Tuvalu",
    "Uganda",
    "Ukraine",
    "Uzbekistan",
    "Vanuatu",
    "Vietnam",
    "Yemen",
    "Zambia",
    "Zimbabwe",
)

STEP_BUSINESS = "business"
STEP_CONSUMER_CHANGE = "consumer-change"
STEP_COUNTRIES_OF_IMPORT = "which-countries"
STEP_COUNTRY = "country"
STEP_EQUIVALANT_UK_GOODS = "equivalent-uk-goods"
STEP_IMPORT_FROM_OVERSEAS = "import-from-overseas"
STEP_IMPORTED_PRODUCTS_USAGE = "imported-products-usage"
STEP_MARKET_SIZE = "market-size"
STEP_MARKET_SIZE_AFTER_BREXIT = "market-size-after-brexit"
STEP_OTHER_CHANGES = "other-changes-after-brexit"
STEP_OTHER_INFOMATION = "other-information"
STEP_OUTCOME = "outcome"
STEP_PERSONAL = "personal"
STEP_PRODUCT = "product-search"
STEP_PRODUCT_DETAIL = "product-detail"
STEP_PRODUCTION_PERCENTAGE = "production-percentage"
STEP_SALES_AFTER_BREXIT = "sales-after-brexit"
STEP_SALES_REVENUE_BEFORE_BREXIT = "sales-revenue-before-brexit"
STEP_SALES_VOLUME_BEFORE_BREXIT = "sales-volume-before-brexit"
STEP_SUMMARY = "summary"
STEP_USER_TYPE = "user-type"
STEP_FINISHED = "finished"


INDUSTRY_CHOICES = [("", "Please select")] + choices.SECTORS + [("OTHER", "Other")]
INCOME_BRACKET_CHOICES = (
    ("", "Please select"),
    ("0-11.85k", "Up to £11,850"),
    ("11.85k-46.35k", "£11,851 to £46,350"),
    ("46.35k-150k", "£46,351 to £150,000"),
    ("150k+", "Over £150,000"),
)
TURNOVER_CHOICES = (
    ("", "Please select"),
    ("0-25k", "under £25,000"),
    ("25k-100k", "£25,000 - £100,000"),
    ("100k-1m", "£100,000 - £1,000,000"),
    ("1m-5m", "£1,000,000 - £5,000,000"),
    ("5m-25m", "£5,000,000 - £25,000,000"),
    ("25m-50m", "£25,000,000 - £50,000,000"),
    ("50m+", "£50,000,000+"),
)
SALES_VOLUME_UNIT_CHOICES = [
    ("KILOGRAM", "kilograms (kg)"),
    ("LITRE", "litres"),
    ("METERS", "meters"),
    ("UNITS", "units (number of items)"),
    (OTHER, "Other"),
]
COMPANY_TYPE_CHOICES = (
    ("LIMITED", "UK private or public limited company"),
    ("OTHER", "Other type of UK organisation"),
)
CHOICES_CHANGE_TYPE_VOLUME = (
    (ACTUAL, "Actual change in volume"),
    (EXPECTED, "Expected change in volume"),
)
CHOICES_CHANGE_TYPE_PRICE = (
    (ACTUAL, "Actual change in price"),
    (EXPECTED, "Expected change in price"),
)
CHOICES_CHANGE_TYPE = ((ACTUAL, "Actual change"), (EXPECTED, "Expected change"))
CHOICES_CHANGE_TYPE_CHOICE = (
    (ACTUAL, "Actual change in choice"),
    (EXPECTED, "Expected change in choice"),
)


steps_data_common = {
    STEP_PRODUCT: {
        "commodity": json.dumps(
            {"commodity_code": ["010130", "00", "00"], "label": "Asses"}
        )
    },
    STEP_SALES_VOLUME_BEFORE_BREXIT: {
        "sales_volume_unit": "UNITS",
        "quarter_three_2019_sales_volume": 32019,
        "quarter_two_2019_sales_volume": 22019,
        "quarter_one_2019_sales_volume": 12019,
        "quarter_four_2018_sales_volume": 42018,
    },
    STEP_PRODUCT_DETAIL: {},
    STEP_SALES_REVENUE_BEFORE_BREXIT: {
        "quarter_three_2019_sales_revenue": 32019,
        "quarter_two_2019_sales_revenue": 22019,
        "quarter_one_2019_sales_revenue": 12019,
        "quarter_four_2018_sales_revenue": 42018,
    },
    STEP_SALES_AFTER_BREXIT: {"has_volume_changed": False, "has_price_changed": False},
    STEP_MARKET_SIZE_AFTER_BREXIT: {
        "has_market_size_changed": False,
        "has_market_price_changed": False,
    },
    STEP_OTHER_CHANGES: {"has_other_changes": False},
    STEP_MARKET_SIZE: {
        "market_size_known": True,
        "market_size_year": "2019",
        "market_size": 121232,
    },
    STEP_OTHER_INFOMATION: {"other_information": "Foo Bar"},
    STEP_OUTCOME: {"tariff_rate": DECREASE, "tariff_quota": DECREASE},
    STEP_SUMMARY: {"terms_agreed": True, "g-recaptcha-response": "PASSED"},
}

steps_data_business = {
    **steps_data_common,
    STEP_BUSINESS: {
        "company_type": "LIMITED",
        "company_name": "Jim Ham",
        "company_number": "1234567",
        "sector": INDUSTRY_CHOICES[1][0],
        "employees": choices.EMPLOYEES[1][0],
        "turnover": TURNOVER_CHOICES[1][0],
        "employment_regions": choices.EXPERTISE_REGION_CHOICES[0][0],
    },
    STEP_PERSONAL: {
        "given_name": "Jim",
        "family_name": "Example",
        "email": "jim@example.com",
    },
}

steps_data_consumer = {
    **steps_data_common,
    STEP_CONSUMER_CHANGE: {
        "has_consumer_price_changed": True,
        "has_consumer_choice_changed": False,
        "price_changed_type": ACTUAL,
        "price_change_comment": "bar",
    },
    STEP_PERSONAL: {
        "given_name": "Jim",
        "family_name": "Example",
        "email": "jim@example.com",
        "income_bracket": INCOME_BRACKET_CHOICES[1][0],
        "organisation_name": "Example corp",
        "consumer_regions": choices.EXPERTISE_REGION_CHOICES[0][0],
    },
}

steps_data_developing = {
    **steps_data_common,
    STEP_COUNTRY: {"country": GENERALISED_SYSTEM_OF_PERFERENCE_COUNTRIES[0]},
    STEP_BUSINESS: {
        "company_type": "LIMITED",
        "company_name": "Jim Ham",
        "company_number": "1234567",
        "sector": INDUSTRY_CHOICES[1][0],
        "employees": choices.EMPLOYEES[1][0],
        "turnover": TURNOVER_CHOICES[1][0],
        "employment_regions": choices.EXPERTISE_REGION_CHOICES[0][0],
    },
    STEP_PERSONAL: {
        "given_name": "Jim",
        "family_name": "Example",
        "email": "jim@example.com",
    },
}


steps_data_importer = {
    **steps_data_common,
    STEP_IMPORTED_PRODUCTS_USAGE: {"imported_goods_makes_something_else": False},
    STEP_PRODUCTION_PERCENTAGE: {
        "production_volume_percentage": 33,
        "production_cost_percentage": 23,
    },
    STEP_COUNTRIES_OF_IMPORT: {"import_countries": ["FR"]},
    STEP_EQUIVALANT_UK_GOODS: {"equivalent_uk_goods": "False"},
    STEP_BUSINESS: {
        "company_type": "LIMITED",
        "company_name": "Jim Ham",
        "company_number": "1234567",
        "sector": INDUSTRY_CHOICES[1][0],
        "employees": choices.EMPLOYEES[1][0],
        "turnover": TURNOVER_CHOICES[1][0],
        "employment_regions": choices.EXPERTISE_REGION_CHOICES[0][0],
    },
    STEP_PERSONAL: {
        "given_name": "Jim",
        "family_name": "Example",
        "email": "jim@example.com",
    },
}
