import os
from urllib import parse as urlparse


DIRECTORY_API_URL = os.environ["DIRECTORY_API_URL"]
DIRECTORY_BUYER_API_URL = os.environ["DIRECTORY_BUYER_API_URL"]
DIRECTORY_SSO_URL = os.environ['DIRECTORY_SSO_URL']
DIRECTORY_UI_BUYER_URL = os.environ["DIRECTORY_UI_BUYER_URL"]
DIRECTORY_UI_SUPPLIER_URL = os.environ["DIRECTORY_UI_SUPPLIER_URL"]
DIRECTORY_PROFILE_URL = os.environ["DIRECTORY_PROFILE_URL"]
LOCUST_MAX_WAIT = int(os.getenv("LOCUST_MAX_WAIT", 6000))
LOCUST_MIN_WAIT = int(os.getenv("LOCUST_MIN_WAIT", 500))

# run tests for 2.5min by default
LOCUST_TIMEOUT = int(os.getenv("LOCUST_TIMEOUT", 150))
API_CLIENT_KEY = os.getenv("API_CLIENT_KEY")
SSO_USER_ID = int(os.getenv("SSO_USER_ID", 0))

# These are required to fetch email messages with email verification links
# which are stored in AWS S3 by AWS SES for specific test user:
# test@directory.uktrade.io
S3_ACCESS_KEY_ID = os.environ["S3_ACCESS_KEY_ID"]
S3_SECRET_ACCESS_KEY = os.environ["S3_SECRET_ACCESS_KEY"]
S3_BUCKET = os.environ["S3_BUCKET"]
S3_REGION = os.environ["S3_REGION"]

# These DB details are required to do post-test clean-up in Directory DB
DIR_DB_URL = urlparse.urlparse(os.environ['DIR_DATABASE_URL'])
DIR_DB_NAME = DIR_DB_URL.path[1:]
DIR_DB_USER = DIR_DB_URL.username
DIR_DB_PASSWORD = DIR_DB_URL.password
DIR_DB_HOST = DIR_DB_URL.hostname
DIR_DB_PORT = DIR_DB_URL.port

# These DB details are required to do post-test clean-up in SSO DB
SSO_DB_URL = urlparse.urlparse(os.environ['SSO_DATABASE_URL'])
SSO_DB_NAME = SSO_DB_URL.path[1:]
SSO_DB_USER = SSO_DB_URL.username
SSO_DB_PASSWORD = SSO_DB_URL.password
SSO_DB_HOST = SSO_DB_URL.hostname
SSO_DB_PORT = SSO_DB_URL.port

# Static data used across the project
EMAIL_VERIFICATION_MSG_SUBJECT = ("Your great.gov.uk account: Please Confirm "
                                  "Your E-mail Address")
NO_OF_EMPLOYEES = ["1-10", "11-50", "51-200", "201-500", "501-1000",
                   "1001-10000", "10001+"]
SECTORS = [
    "AEROSPACE", "AGRICULTURE_HORTICULTURE_AND_FISHERIES", "AIRPORTS",
    "AUTOMOTIVE", "BIOTECHNOLOGY_AND_PHARMACEUTICALS",
    "BUSINESS_AND_CONSUMER_SERVICES", "CHEMICALS",
    "CLOTHING_FOOTWEAR_AND_FASHION", "COMMUNICATIONS", "CONSTRUCTION",
    "CREATIVE_AND_MEDIA", "EDUCATION_AND_TRAINING",
    "ELECTRONICS_AND_IT_HARDWARE", "ENVIRONMENT",
    "FINANCIAL_AND_PROFESSIONAL_SERVICES", "FOOD_AND_DRINK",
    "GIFTWARE_JEWELLERY_AND_TABLEWARE", "GLOBAL_SPORTS_INFRASTRUCTURE",
    "HEALTHCARE_AND_MEDICAL", "HOUSEHOLD_GOODS_FURNITURE_AND_FURNISHINGS",
    "LEISURE_AND_TOURISM", "MARINE",
    "MECHANICAL_ELECTRICAL_AND_PROCESS_ENGINEERING",
    "METALLURGICAL_PROCESS_PLANT", "METALS_MINERALS_AND_MATERIALS", "MINING",
    "OIL_AND_GAS", "PORTS_AND_LOGISTICS", "POWER", "RAILWAYS",
    "RENEWABLE_ENERGY", "RETAIL_AND_LUXURY", "SECURITY",
    "SOFTWARE_AND_COMPUTER_SERVICES", "TEXTILES_INTERIOR_TEXTILES_AND_CARPETS",
    "WATER"
]

NO_EXPORT_INTENT_LABEL = "No, we are not planning to sell overseas"

EXPORT_STATUSES = {
    "Yes, in the last year": "YES",
    "Yes, 1 to 2 years ago": "ONE_TWO_YEARS_AGO",
    "Yes, but more than 2 years ago": "OVER_TWO_YEARS_AGO",
    "No, but we are preparing to": "NOT_YET",
    NO_EXPORT_INTENT_LABEL: "NO_INTENTION"
}
