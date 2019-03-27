import os
from random import choice, randint

FILES_DIR = os.path.abspath(os.path.join("tests", "functional", "files"))

with open(os.path.join(FILES_DIR, "rare.txt"), "r") as words_file:
    RARE_WORDS = words_file.read().split()

SECTORS = [
    "AEROSPACE", "ADVANCED_MANUFACTURING", "AIRPORTS",
    "AGRICULTURE_HORTICULTURE_AND_FISHERIES", "AUTOMOTIVE",
    "BIOTECHNOLOGY_AND_PHARMACEUTICALS", "BUSINESS_AND_CONSUMER_SERVICES",
    "CHEMICALS", "CLOTHING_FOOTWEAR_AND_FASHION", "COMMUNICATIONS",
    "CONSTRUCTION", "CREATIVE_AND_MEDIA", "EDUCATION_AND_TRAINING",
    "ELECTRONICS_AND_IT_HARDWARE", "ENVIRONMENT",
    "FINANCIAL_AND_PROFESSIONAL_SERVICES", "FOOD_AND_DRINK",
    "GIFTWARE_JEWELLERY_AND_TABLEWARE", "GLOBAL_SPORTS_INFRASTRUCTURE",
    "HEALTHCARE_AND_MEDICAL", "HOUSEHOLD_GOODS_FURNITURE_AND_FURNISHINGS",
    "LIFE_SCIENCES", "LEISURE_AND_TOURISM", "LEGAL_SERVICES", "MARINE",
    "MECHANICAL_ELECTRICAL_AND_PROCESS_ENGINEERING",
    "METALLURGICAL_PROCESS_PLANT", "METALS_MINERALS_AND_MATERIALS",
    "MINING", "OIL_AND_GAS", "PORTS_AND_LOGISTICS", "POWER", "RAILWAYS",
    "RENEWABLE_ENERGY", "RETAIL_AND_LUXURY", "SECURITY",
    "SOFTWARE_AND_COMPUTER_SERVICES", "TEXTILES_INTERIOR_TEXTILES_AND_CARPETS",
    "WATER"
]

PRODUCT_CATEGORIES = [
    "Home & Garden", "Animals & Pet Supplies", "Food, Beverages & Tobacco"
    "Bay & Toddler", "Toys & Games", "Sporting Goods", "Hardware", "Clothing & Accessories",
    "Vehicles & Parts", "Electronics", "Arts & Entertainment", "Business & Industrial",
    "Office Supplies", "Cameras & Optics"
]


OPERATING_COUNTRIES = [
    "China", "Japan", "India", "United States",
    "Australia", "New Zealand", "Finland", "Canada",
    "France", "Germany", "Austria", "Russia", "Zimbabwe", "Belgium"
]


def rare_word(*, min_length: int = 9, max_length: int = 20) -> str:
    """Get a random rare english word.

    NOTE:
    min_length is set to 9, because all words in RARE_WORDS are at least 9
    characters long
    """
    assert min_length < max_length
    word = ""
    while min_length >= len(word) <= max_length:
        word = choice(RARE_WORDS)
    return word


def random_company_number() -> str:
    return str(randint(0, 9999999)).zfill(8)


def random_sector() -> str:
    return choice(SECTORS)


def random_product_categories() -> str:
    return choice(PRODUCT_CATEGORIES)


def random_operating_countries() -> str:
    return choice(OPERATING_COUNTRIES)