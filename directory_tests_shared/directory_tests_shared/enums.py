from enum import Enum
from random import choice


class BusinessType(Enum):
    COMPANIES_HOUSE = "companies-house-company"
    SOLE_TRADED = "non-companies-house-company"
    TAX_PAYER = "not-company"
    OVERSEAS_COMPANY = "overseas-company"

    @classmethod
    def random(cls):
        return choice(list(cls.__members__.values()))
