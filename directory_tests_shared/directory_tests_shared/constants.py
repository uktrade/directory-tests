# -*- coding: utf-8 -*-
import os
from glob import glob

from envparse import env

#####################################################################
# Constants used across all of the test suites
#####################################################################
FORMS_API_MAILBOXES = {
    "DIT Enquiry unit": env.str("FORMS_API_SENDER_EMAIL_DIT_ENQUIRIES"),
    "Events mailbox": env.str("FORMS_API_SENDER_EMAIL_EVENTS"),
    "DSO mailbox": env.str("FORMS_API_SENDER_EMAIL_DSO"),
    "Invest mailbox": env.str("FORMS_API_SENDER_EMAIL_INVEST"),
    "Trade mailbox": env.str("FORMS_API_SENDER_EMAIL_TRADE"),
}
INVEST_CONTACT_CONFIRMATION_SUBJECT = env.str(
    "INVEST_CONTACT_CONFIRMATION_SUBJECT", default="Contact form user email subject"
)
HPO_ENQUIRY_CONFIRMATION_SUBJECT = env.str(
    "HPO_ENQUIRY_CONFIRMATION_SUBJECT",
    default="Your High Potential Opportunity Enquiry – UK Department for International Trade",
)
HPO_AGENT_EMAIL_ADDRESS = env.str("HPO_AGENT_EMAIL_ADDRESS", default="test@example.com")
HPO_AGENT_EMAIL_SUBJECT = env.str(
    "HPO_AGENT_EMAIL_SUBJECT", default="HPO Enquiry (Invest in GREAT Britain)"
)
HPO_PDF_URLS = [
    "https://directory-cms-public.s3.amazonaws.com/documents/A_High_Potential_Investment_Opportunity_in_UK_Rail.pdf",  # noqa
    "https://directory-cms-public.s3.amazonaws.com/documents/documents/A_High_Potential_Opportunity_in_High_Productivity_Food_Production.pdf",  # noqa
    "https://directory-cms-public.s3.amazonaws.com/documents/documents/A_HPO_in_Lightweight_Structures.pdf",  # noqa
    "https://directory-cms-public.s3.amazonaws.com/documents/documents/Homes_in_England_Investment_Opportunities_1_IOKOmjM_lvquoys.pdf",  # noqa
    "https://directory-cms-public.s3.amazonaws.com/documents/Homes_in_England_Investment_Opportunities_1_v6rnuyO.pdf",  # noqa
]
MD5_CHECKSUM_EIG_LOGO = env.str(
    "EIG_LOGO_MD5_CHECKSUM", default="8bc6134cffb3cdb134ad910e6a698fb8"
)
MD5_CHECKSUM_GREAT_LOGO = env.str(
    "GREAT_LOGO_MD5_CHECKSUM", default="6af76ffaffc1009edc9f92871ce73274"
)
MD5_CHECKSUM_EVENTS_BIG_HEADER_LOGO = env.str(
    "EVENTS_BIG_LOGO_MD5_CHECKSUM", default="cf06c747729c8515086b39a47f149fad"
)
MD5_CHECKSUM_EVENTS_BIG_FOOTER_LOGO = env.str(
    "EVENTS_BIG_FOOTER_LOGO_MD5_CHECKSUM", default="7efc18df0076a860835196f7ca39e437"
)
MD5_CHECKSUM_INVEST_IN_GREAT = env.str(
    "MD5_CHECKSUM_INVEST_IN_GREAT", default="b1cca6e547c89896f0b13632bc298168"
)
MD5_CHECKSUM_DIT_FAVICON = env.str(
    "DIT_FAVICON_MD5_CHECKSUM", default="93bd34ac9de2cb059c65c5e7931667a2"
)
EMAIL_VERIFICATION_CODE_SUBJECT = "Your confirmation code for great.gov.uk"
EMAIL_VERIFICATION_MSG_SUBJECT = "Confirm your email address"
EMAIL_ERP_PROGRESS_SAVED_MSG_SUBJECT = "We’ve saved your progress until"
FAS_MESSAGE_FROM_BUYER_SUBJECT = (
    "New message through your great.gov.uk business profile"
)
FAB_CONFIRM_COLLABORATION_SUBJECT = (
    "Confirm you’ve been added to {}’s Find a" " buyer profile"
)
FAB_TRANSFER_OWNERSHIP_SUBJECT = "Confirm ownership of {}’s Find a buyer " "profile"
SSO_PASSWORD_RESET_MSG_SUBJECT = "Reset your great.gov.uk password"
PROFILE_INVITATION_MSG_SUBJECT = (
    "You’ve been invited to join {company_title} on great.gov.uk"
)
NO_OF_EMPLOYEES = [
    "1-10",
    "11-50",
    "51-200",
    "201-500",
    "501-1000",
    "1001-10000",
    "10001+",
]
SECTORS = [
    "AEROSPACE",
    "ADVANCED_MANUFACTURING",
    "AIRPORTS",
    "AGRICULTURE_HORTICULTURE_AND_FISHERIES",
    "AUTOMOTIVE",
    "BIOTECHNOLOGY_AND_PHARMACEUTICALS",
    "BUSINESS_AND_CONSUMER_SERVICES",
    "CHEMICALS",
    "CLOTHING_FOOTWEAR_AND_FASHION",
    "COMMUNICATIONS",
    "CONSTRUCTION",
    "CREATIVE_AND_MEDIA",
    "EDUCATION_AND_TRAINING",
    "ELECTRONICS_AND_IT_HARDWARE",
    "ENVIRONMENT",
    "FINANCIAL_AND_PROFESSIONAL_SERVICES",
    "FOOD_AND_DRINK",
    "GIFTWARE_JEWELLERY_AND_TABLEWARE",
    "GLOBAL_SPORTS_INFRASTRUCTURE",
    "HEALTHCARE_AND_MEDICAL",
    "HOUSEHOLD_GOODS_FURNITURE_AND_FURNISHINGS",
    "LIFE_SCIENCES",
    "LEISURE_AND_TOURISM",
    "LEGAL_SERVICES",
    "MARINE",
    "MECHANICAL_ELECTRICAL_AND_PROCESS_ENGINEERING",
    "METALLURGICAL_PROCESS_PLANT",
    "METALS_MINERALS_AND_MATERIALS",
    "MINING",
    "OIL_AND_GAS",
    "PORTS_AND_LOGISTICS",
    "POWER",
    "RAILWAYS",
    "RENEWABLE_ENERGY",
    "RETAIL_AND_LUXURY",
    "SECURITY",
    "SOFTWARE_AND_COMPUTER_SERVICES",
    "TEXTILES_INTERIOR_TEXTILES_AND_CARPETS",
    "WATER",
]

SECTORS_WITH_LABELS = {
    "AEROSPACE": "Aerospace",
    "ADVANCED_MANUFACTURING": "Advanced manufacturing",
    "AIRPORTS": "Airports",
    "AGRICULTURE_HORTICULTURE_AND_FISHERIES": "Agriculture, horticulture and fisheries",
    "AUTOMOTIVE": "Automotive",
    "BIOTECHNOLOGY_AND_PHARMACEUTICALS": "Biotechnology and pharmaceuticals",
    "BUSINESS_AND_CONSUMER_SERVICES": "Business and consumer services",
    "CHEMICALS": "Chemicals",
    "CLOTHING_FOOTWEAR_AND_FASHION": "Clothing, footwear and fashion",
    "COMMUNICATIONS": "Communications",
    "CONSTRUCTION": "Construction",
    "CREATIVE_AND_MEDIA": "Creative and media",
    "EDUCATION_AND_TRAINING": "Education and training",
    "ELECTRONICS_AND_IT_HARDWARE": "Electronics and IT hardware",
    "ENVIRONMENT": "Environment",
    "FINANCIAL_AND_PROFESSIONAL_SERVICES": "Financial and professional services",
    "FOOD_AND_DRINK": "Food and drink",
    "GIFTWARE_JEWELLERY_AND_TABLEWARE": "Giftware, jewellery and tableware",
    "GLOBAL_SPORTS_INFRASTRUCTURE": "Global sports infrastructure",
    "HEALTHCARE_AND_MEDICAL": "Healthcare and medical",
    "HOUSEHOLD_GOODS_FURNITURE_AND_FURNISHINGS": "Household goods, furniture and furnishings",
    "LIFE_SCIENCES": "Life sciences",
    "LEISURE_AND_TOURISM": "Leisure and tourism",
    "LEGAL_SERVICES": "Legal services",
    "MARINE": "Marine",
    "MECHANICAL_ELECTRICAL_AND_PROCESS_ENGINEERING": "Mechanical electrical and process engineering",
    "METALLURGICAL_PROCESS_PLANT": "Metallurgical process plant",
    "METALS_MINERALS_AND_MATERIALS": "Metals, minerals and materials",
    "MINING": "Mining",
    "OIL_AND_GAS": "Oil and gas",
    "PORTS_AND_LOGISTICS": "Ports and logistics",
    "POWER": "Power",
    "RAILWAYS": "Railways",
    "RENEWABLE_ENERGY": "Renewable energy",
    "RETAIL_AND_LUXURY": "Retail and luxury",
    "SECURITY": "Security",
    "SOFTWARE_AND_COMPUTER_SERVICES": "Software and computer services",
    "TEXTILES_INTERIOR_TEXTILES_AND_CARPETS": "Textiles, interior textiles and carpets",
    "WATER": "Water",
}

COUNTRIES = {
    "China": "CN",
    "Germany": "DE",
    "India": "IN",
    "Japan": "JP",
    "United States": "US",
}

POSTCODES = [
    "LE4 9HA",
    # "WC1N 3AX",
    "E13 0LD",
    "HP10 9AS",
    "IV30 5YE",
    "ML11 8AG",
    "RG26 5NW",
    "CB5 8SW",
    "W1W 7LJ",
    "LL69 9YN",
    "TN20 6HN",
]

# Absolute path to a directory with test images
test_files_path_current_dir = os.path.abspath(os.path.join(".", "files"))
test_files_path_browser_tests = os.path.abspath(os.path.join("..", "files"))
test_files_path_other_tests = os.path.abspath(os.path.join("tests", "files"))
if os.path.isdir(test_files_path_current_dir):
    TEST_IMAGES_DIR = test_files_path_current_dir
elif os.path.isdir(test_files_path_browser_tests):
    TEST_IMAGES_DIR = test_files_path_browser_tests
elif os.path.isdir(test_files_path_other_tests):
    TEST_IMAGES_DIR = test_files_path_other_tests
else:
    raise FileNotFoundError

# lists of absolute paths to test images of specific type
PNGs = glob(os.path.join(TEST_IMAGES_DIR, "*.png"))
JPGs = glob(os.path.join(TEST_IMAGES_DIR, "*.jpg"))
JPEGs = glob(os.path.join(TEST_IMAGES_DIR, "*.jpeg"))
BMPs = glob(os.path.join(TEST_IMAGES_DIR, "*.bmp"))
JP2s = glob(os.path.join(TEST_IMAGES_DIR, "*.jp2"))  # noqa
WEBPs = glob(os.path.join(TEST_IMAGES_DIR, "*.webp"))

"""
Load a list of rare english words.
This list was compiled using:
a) Wictionary top 100,000 most frequently-used English words
  -> https://gist.github.com/h3xx/1976236
b) 20000 most common English words in order of frequency, as determined by
  n-gram frequency analysis of the Google's Trillion Word Corpus
  -> https://github.com/first20hours/google-10000-english/blob/master/20k.txt

The selection process was as follows:
1) delete first 30000 lines from a)
2) select words with a least 9 characters: if len(w) > 8
3) skip all words that contain non-ASCII characters: len(w) == len(w.encode())
4) skip all words that contain non-latin alphabet characters, like: ',."@$ etc
   skip = ["'", "\"", "`", ",", ".", ";", ":", "!", "#", "@", "$", "%", "^",
           "&", "*", "(", ")", "-", "=", "+", "_", "{", "[", "]", "}", "?",
           ">", "<"]
   all(e not in w for e in skip)
5) make all words lower case: w.lower()
6) remove all duplicates: set(words)
7) sort
8) remove from selected words all words present in b)
   grep -v -x -f 100k.txt 20k.txt > rare.txt

Steps 2-7:
with open("./100k.txt") as f:
   words = f.read().split()

skip = ["'", "\"", "`", ",", ".", ";", ":", "!", "#", "@", "$", "%", "^", "&",
        "*", "(", ")", "-", "=", "+", "_", "{", "[", "]", "}", "?", ">", "<"]
nine = sorted(set([w.lower() for w in words
                   if len(w) > 8
                   and len(w) == len(w.encode())
                   and all(e not in w for e in skip)]))
"""
with open(os.path.join(TEST_IMAGES_DIR, "rare.txt"), "r") as f:
    RARE_WORDS = f.read().split()

"""
This list
PS.
a) 20000 most common English words in order of frequency, as determined by
  -> https://github.com/first20hours/google-10000-english/blob/master/google-10000-english-usa-no-swears-medium.txt
"""
with open(os.path.join(TEST_IMAGES_DIR, "english-4k.txt"), "r") as f:
    POPULAR_ENGLISH_WORDS = f.read().split()

SEARCHABLE_CASE_STUDY_DETAILS = [
    "title",
    "summary",
    "description",
    # "keywords",
    "caption_1",
    "caption_2",
    "caption_3",
    # "testimonial",
    "slug",
    # "source_name",
    # "source_job",
    "source_company",
    "website",
]

FAS_LOGO_PLACEHOLDER_IMAGE = "/static/images/placeholder.fc5114289e5b.png"

SEPARATORS = {
    "pipe": "|",
    "semi-colon": ";",
    "colon": ":",
    "full stop": ".",
    "comma": ",",
}

# these user credentials are hard-coded in `directory-sso`. The users
# are created when `manage.py create_test_users` is ran on sso.
USERS = {
    "verified": {
        "username": env.str("SSO_USER_USERNAME"),
        "password": env.str("SSO_USER_PASSWORD"),
        "token": env.str("SSO_USER_TOKEN"),
        "sso_id": env.int("SSO_USER_SSO_ID"),
    },
    "unverified": {"token": env.str("SSO_UNVERIFIED_USER_TOKEN")},
}

COMPANIES = {
    "not_active": env.str("SSO_COMPANY_NOT_ACTIVE", default="06542942"),
    "already_registered": env.str("SSO_COMPANY_ALREADY_REGISTERED", default="10416664"),
    "active_not_registered": env.str(
        "SSO_COMPANY_ACTIVE_NOT_REGISTERED", default="01624297"
    ),
}

LOAD_TESTS_USER_AGENT = {"User-Agent": "locust - load tests"}

PRODUCT_CATEGORIES = [
    1,
    8,
    537,
    111,
    141,
    166,
    222,
    412,
    436,
    632,
    469,
    536,
    5181,
    772,
    783,
    922,
    5605,
    2092,
    988,
    1239,
    888,
]

OPERATING_COUNTRIES = [
    60,
    61,
    62,
    64,
    65,
    344,
    69,
    70,
    73,
    74,
    75,
    77,
    78,
    79,
    80,
    81,
    83,
    84,
    86,
    87,
    343,
    90,
    94,
    95,
    96,
    342,
    98,
    99,
    100,
    101,
    102,
    104,
    341,
    109,
    110,
    111,
    114,
    115,
    116,
    340,
    120,
    121,
    122,
    124,
    125,
    126,
    127,
    128,
    339,
    131,
    132,
    133,
    134,
    338,
    136,
    137,
    138,
    141,
    142,
    144,
    148,
    151,
    152,
    153,
    155,
    157,
    160,
    161,
    162,
    163,
    164,
    166,
    168,
    169,
    170,
    171,
    172,
    173,
    328,
    175,
    176,
    177,
    178,
    179,
    180,
    181,
    182,
    183,
    184,
    185,
    186,
    189,
    190,
    191,
    192,
    193,
    194,
    195,
    196,
    197,
    337,
    199,
    200,
    201,
    202,
    203,
    204,
    205,
    207,
    208,
    211,
    212,
    213,
    336,
    214,
    215,
    217,
    218,
    220,
    221,
    222,
    223,
    225,
    226,
    227,
    228,
    233,
    234,
    236,
    237,
    238,
    239,
    240,
    241,
    242,
    243,
    245,
    247,
    249,
    251,
    252,
    253,
    255,
    256,
    334,
    258,
    259,
    260,
    263,
    265,
    266,
    268,
    269,
    270,
    271,
    272,
    274,
    275,
    276,
    277,
    335,
    280,
    282,
    283,
    333,
    286,
    287,
    288,
    289,
    291,
    292,
    293,
    329,
    330,
    295,
    297,
    332,
    299,
    300,
    301,
    303,
    305,
    306,
    331,
    326,
    307,
    308,
    312,
    313,
    314,
    315,
    316,
    321,
    324,
    325,
]
