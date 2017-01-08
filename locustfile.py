# flake8: noqa
from tests.locust.test_ui import (
    RegularUserBuyerUI,
    RegularUserSupplierUI,
    AuthUserBuyerUI
)
from tests.locust.test_sso import (
    RegularUserSSO,
    AuthenticatedUserSSO
)
from tests.locust.test_api import (
    RegularUserAPI,
    AuthenticatedUserAPI
)
