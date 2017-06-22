import os


# These variables specify URLs to Services under test
DIRECTORY_API_URL = os.environ["DIRECTORY_API_URL"]
DIRECTORY_SSO_URL = os.environ['DIRECTORY_SSO_URL']
DIRECTORY_UI_BUYER_URL = os.environ["DIRECTORY_UI_BUYER_URL"]
DIRECTORY_UI_SUPPLIER_URL = os.environ["DIRECTORY_UI_SUPPLIER_URL"]
DIRECTORY_PROFILE_URL = os.environ["DIRECTORY_PROFILE_URL"]

# These are required to fetch email messages with email verification links
# which are stored in AWS S3 by AWS SES for specific test user:
# test@directory.uktrade.io
S3_ACCESS_KEY_ID = os.environ["S3_ACCESS_KEY_ID"]
S3_SECRET_ACCESS_KEY = os.environ["S3_SECRET_ACCESS_KEY"]
S3_BUCKET = os.environ["S3_BUCKET"]
S3_REGION = os.environ["S3_REGION"]
