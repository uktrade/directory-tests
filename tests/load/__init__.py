import os
from mohawk import Sender


USER_AGENT = {"User-Agent": "locust - load tests"}

IP_RESTRICTOR_SKIP_CHECK_SENDER_ID = os.environ["IP_RESTRICTOR_SKIP_CHECK_SENDER_ID"]
IP_RESTRICTOR_SKIP_CHECK_SECRET_INVEST = os.environ["IP_RESTRICTOR_SKIP_CHECK_SECRET_INVEST"]


def hawk_cookie(key):
    sender = Sender(
        credentials={
            'id': IP_RESTRICTOR_SKIP_CHECK_SENDER_ID,
            'key': key,
            'algorithm': 'sha256'
        },
        url='/',
        method='',
        always_hash_content=False
    )
    return {"ip-restrict-signature": sender.request_header}


def invest_hawk_cookie():
    return hawk_cookie(IP_RESTRICTOR_SKIP_CHECK_SECRET_INVEST)
