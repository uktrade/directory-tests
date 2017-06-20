import os
from urllib import parse as urlparse

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

FAB_DB_URL = urlparse.urlparse(os.environ['FAB_DATABASE_URL'])
FAB_DB_NAME = FAB_DB_URL.path[1:]
FAB_DB_USER = FAB_DB_URL.username
FAB_DB_PASSWORD = FAB_DB_URL.password
FAB_DB_HOST = FAB_DB_URL.hostname
FAB_DB_PORT = FAB_DB_URL.port

SSO_DB_URL = urlparse.urlparse(os.environ['SSO_DATABASE_URL'])
SSO_DB_NAME = SSO_DB_URL.path[1:]
SSO_DB_USER = SSO_DB_URL.username
SSO_DB_PASSWORD = SSO_DB_URL.password
SSO_DB_HOST = SSO_DB_URL.hostname
SSO_DB_PORT = SSO_DB_URL.port
