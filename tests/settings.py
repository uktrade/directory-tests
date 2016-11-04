import os


DIRECTORY_API_URL = os.environ["DIRECTORY_API_URL"]
DIRECTORY_SSO_URL = os.environ['DIRECTORY_SSO_URL']
DIRECTORY_UI_URL = os.environ["DIRECTORY_UI_URL"]
LOCUST_MAX_WAIT = int(os.getenv("LOCUST_MAX_WAIT", 6000))
LOCUST_MIN_WAIT = int(os.getenv("LOCUST_MIN_WAIT", 500))
# run tests for 2.5min by default
LOCUST_TIMEOUT = int(os.getenv("LOCUST_TIMEOUT", 150))
API_CLIENT_KEY = os.environ["API_CLIENT_KEY"]
SSO_USER_ID = int(os.environ["SSO_USER_ID"])
