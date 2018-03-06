import os
from glob import glob

__auto_retry = os.environ.get("AUTO_RETRY", "true")
AUTO_RETRY = (True
              if __auto_retry
              and __auto_retry.lower() in ["true", "1", "yes"]
              else False)

DIRECTORY_API_URL = os.environ["DIRECTORY_API_URL"]
DIRECTORY_API_CLIENT_KEY = os.environ["DIRECTORY_API_CLIENT_KEY"]
DIRECTORY_API_HEALTH_CHECK_TOKEN = os.environ["DIRECTORY_API_HEALTH_CHECK_TOKEN"]
DIRECTORY_BUYER_API_URL = os.environ["DIRECTORY_BUYER_API_URL"]
DIRECTORY_SSO_URL = os.environ['DIRECTORY_SSO_URL']
DIRECTORY_UI_BUYER_URL = os.environ["DIRECTORY_UI_BUYER_URL"]
DIRECTORY_UI_SUPPLIER_URL = os.environ["DIRECTORY_UI_SUPPLIER_URL"]
DIRECTORY_PROFILE_URL = os.environ["DIRECTORY_PROFILE_URL"]
SSO_PROXY_API_CLIENT_BASE_URL = os.environ["SSO_PROXY_API_CLIENT_BASE_URL"]
SSO_PROXY_SIGNATURE_SECRET = os.environ["SSO_PROXY_SIGNATURE_SECRET"]
EXRED_UI_URL = os.environ["EXRED_UI_URL"]
GOV_NOTIFY_API_KEY = os.environ["GOV_NOTIFY_API_KEY"]
LOCUST_MAX_WAIT = int(os.getenv("LOCUST_MAX_WAIT", 6000))
LOCUST_MIN_WAIT = int(os.getenv("LOCUST_MIN_WAIT", 500))

# run tests for 2.5min by default
LOCUST_TIMEOUT = int(os.getenv("LOCUST_TIMEOUT", 150))
SSO_USER_ID = int(os.getenv("SSO_USER_ID", 0))

# Mailgun details required to get verification emails
MAILGUN_DIRECTORY_DOMAIN = os.environ["MAILGUN_DIRECTORY_DOMAIN"]
MAILGUN_DIRECTORY_EVENTS_URL = "https://api.mailgun.net/v3/%s/events" % MAILGUN_DIRECTORY_DOMAIN
MAILGUN_DIRECTORY_API_USER = "api"
MAILGUN_DIRECTORY_SECRET_API_KEY = os.environ["MAILGUN_DIRECTORY_SECRET_API_KEY"]

# Static data used across the projects
EMAIL_VERIFICATION_MSG_SUBJECT = "Confirm your email address"
FAS_MESSAGE_FROM_BUYER_SUBJECT = ("Someone is interested in your Find a Buyer "
                                  "profile")
FAB_CONFIRM_COLLABORATION_SUBJECT = ("Confirm you’ve been added to {}’s Find a"
                                     " buyer profile")
SSO_PASSWORD_RESET_MSG_SUBJECT = "Reset your great.gov.uk password"
NO_OF_EMPLOYEES = ["1-10", "11-50", "51-200", "201-500", "501-1000",
                   "1001-10000", "10001+"]
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
    "WATER": "Water"
}

COUNTRIES = {
    "China": "CN",
    "Germany": "DE",
    "India": "IN",
    "Japan": "JP",
    "United States": "US"
}

# Absolute path to a directory with test images
TEST_IMAGES_DIR = os.path.abspath(os.path.join("tests", "functional", "files"))

# lists of absolute paths to test images of specific type
PNGs = glob(os.path.join(TEST_IMAGES_DIR, "*.png"))
JPGs = glob(os.path.join(TEST_IMAGES_DIR, "*.jpg"))
JPEGs = glob(os.path.join(TEST_IMAGES_DIR, "*.jpeg"))
BMPs = glob(os.path.join(TEST_IMAGES_DIR, "*.bmp"))
JP2s = glob(os.path.join(TEST_IMAGES_DIR, "*.jp2"))
WEBPs = glob(os.path.join(TEST_IMAGES_DIR, "*.webp"))

"""
Load a list of rare english words.
This list was compiled using:
a) Wictionary top 100,000 most frequently-used English words
  -> https://gist.github.com/h3xx/1976236
b) 20000 most common English words in order of frequency, as determined by
  n-gram frequency analysis of the Google's Trillion Word Corpus
  -> https://github.com/first20hours/google-10000-english

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


SEARCHABLE_CASE_STUDY_DETAILS = [
    'title', 'summary', 'description', 'website', 'keywords', 'caption_1',
    'caption_2', 'caption_3', 'testimonial', 'source_name', 'source_job',
    'source_company', 'slug'
]

FAS_LOGO_PLACEHOLDER_IMAGE = "/static/images/placeholder.fc5114289e5b.png"

SEPARATORS = {
    "pipe": "|",
    "semi-colon": ";",
    "colon": ":",
    "full stop": ".",
    "comma": ","
}
