# -*- coding: utf-8 -*-
"""Export Readiness Articles Registry"""
import random
from collections import namedtuple
from copy import copy

ArticleParent = namedtuple("ArticleParent", ["uuid", "title"])


class Article:
    def __init__(
        self,
        title,
        time_to_read,
        *,
        previous=None,
        next=None,
        index: int = None
    ):
        self.title = title
        self.time_to_read = time_to_read
        self.previous = previous
        self.next = next
        self.index = index

    def __str__(self):
        return (
            "index: {index}, "
            "title: {title}, "
            "time_to_read: {time_to_read}, "
            "previous: {previous}, "
            "next: {next}"
        ).format(**self.__dict__)


RESEARCH_YOUR_MARKET = Article(title="Research your market", time_to_read=0)

DEFINE_MARKET_POTENTIAL = Article(
    title="Define market potential", time_to_read=0
)
DO_FIELD_RESEARCH = Article(title="Do field research", time_to_read=0)
ANALYSE_THE_COMPETITION = Article(
    title="Analyse the competition", time_to_read=0
)
VISIT_TRADE_SHOW = Article(title="Visit a trade show", time_to_read=0)
DOING_BUSINESS_WITH_INTEGRITY = Article(
    title="Doing business with integrity", time_to_read=0
)
KNOW_THE_RELEVANT_LEGISLATION = Article(
    title="Know the relevant legislation", time_to_read=0
)
KNOW_YOUR_CUSTOMERS_AND_PARTNERS = Article(
    title="Know your customers and partners", time_to_read=0
)
MAKE_EXPORTING_PLAN = Article(title="Make an export plan", time_to_read=0)
FIND_A_ROUTE_TO_MARKET = Article(
    title="Find a route to market", time_to_read=0
)
SELL_OVERSEAS_DIRECTLY = Article(
    title="Sell overseas directly", time_to_read=0
)
USE_OVERSEAS_AGENT = Article(title="Use an overseas agent", time_to_read=0)
USE_DISTRIBUTOR = Article(title="Use a distributor", time_to_read=0)
CHOOSING_AGENT_OR_DISTRIBUTOR = Article(
    title="Choosing an agent or distributor", time_to_read=0
)
LICENCE_AND_FRANCHISING = Article(
    title="Licensing and franchising", time_to_read=0
)
LICENCE_YOUR_PRODUCT_OR_SERVICE = Article(
    title="License your product or service", time_to_read=0
)
FRANCHISE_YOUR_BUSINESS = Article(
    title="Franchise your business", time_to_read=0
)
START_JOINT_VENTURE = Article(title="Start a joint venture", time_to_read=0)
SETUP_OVERSEAS_OPERATION = Article(
    title="Set up an overseas operation", time_to_read=0
)
GET_MONEY_TO_EXPORT = Article(title="Get money to export", time_to_read=0)
CHOOSE_THE_RIGHT_FINANCE = Article(
    title="Choose the right finance", time_to_read=0
)
GET_EXPORT_FINANCE = Article(title="Get export finance", time_to_read=0)
RAISE_MONEY_BY_BORROWING = Article(
    title="Raise money by borrowing", time_to_read=0
)
BORROW_AGAINST_ASSETS = Article(title="Borrow against assets", time_to_read=0)
RAISE_MONEY_WITH_INVESTMENT = Article(
    title="Raise money with investment", time_to_read=0
)
GET_GOVERNMENT_FINANCE_SUPPORT = Article(
    title="Get finance support from government", time_to_read=0
)
CONSIDER_HOW_PAID = Article(
    title="Consider how you'll get paid", time_to_read=0
)
INVOICE_CURRENCY_AND_CONTENTS = Article(
    title="Invoice currency and contents", time_to_read=0
)
DECIDE_WHEN_PAID = Article(title="Decide when you'll get paid", time_to_read=0)
PAYMENT_METHODS = Article(title="Payment methods", time_to_read=0)
INSURE_AGAINST_NON_PAYMENT = Article(
    title="Insure against non-payment", time_to_read=0
)
ANTI_BRIBERY_AND_CORRUPTION_TRAINING = Article(
    title="Anti-bribery and corruption training", time_to_read=0
)
REPORT_CORRUPTION_AND_HUMAN_RIGHTS_VIOLATIONS = Article(
    title="Report corruption and human rights violations", time_to_read=0
)
PLAN_THE_LOGISTICS = Article(title="Plan the logistics", time_to_read=0)
USE_FREIGHT_FORWARDER = Article(
    title="Use a freight forwarder", time_to_read=0
)
USE_INCOTERMS_IN_CONTRACTS = Article(
    title="Use incoterms in contracts", time_to_read=0
)
GET_YOUR_EXPORT_DOCUMENTS_RIGHT = Article(
    title="Get your export documents right", time_to_read=0
)
INTERNATIONALISE_WESBITE = Article(
    title="Internationalise your website", time_to_read=0
)
MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE = Article(
    title="Match your website to your audience", time_to_read=0
)
TYPES_OF_INTELLECTUAL_PROPERTY = Article(
    title="Types of intellectual property", time_to_read=0
)
KNOW_WHAT_INTELLECTUAL_PROPERTY_YOU_HAVE = Article(
    title="Know what intellectual property you have", time_to_read=0
)
INTELLECTUAL_PROPERTY_PROTECTION = Article(
    title="International intellectual property protection", time_to_read=0
)
MEET_YOUR_CUSTOMER = Article(title="Meet your customers", time_to_read=0)
MANAGE_LANGUAGE_DIFFERENCES = Article(
    title="Manage language differences", time_to_read=0
)
PROTECT_YOUR_INTELLECTUAL_PROPERTY = Article(
    title="Protect your intellectual property", time_to_read=0
)
UNDERSTAND_YOUR_CUSTOMERS_CULTURE = Article(
    title="Understand your customer's culture", time_to_read=0
)

NEXT_STEPS_NEW_EXPORTER = Article(
    title="Next steps for new to exporting", time_to_read=0
)

NEXT_STEPS_OCCASIONAL_EXPORTER = Article(
    title="Next steps for occasional exporters", time_to_read=0
)

NEXT_STEPS_REGULAR_EXPORTER = Article(
    title="Next steps for regular exporters", time_to_read=0
)

PERSONA_NEW_ARTICLES = [
    RESEARCH_YOUR_MARKET,
    DOING_BUSINESS_WITH_INTEGRITY,
    KNOW_THE_RELEVANT_LEGISLATION,
    KNOW_YOUR_CUSTOMERS_AND_PARTNERS,
    MAKE_EXPORTING_PLAN,
    FIND_A_ROUTE_TO_MARKET,
    SELL_OVERSEAS_DIRECTLY,
    USE_OVERSEAS_AGENT,
    USE_DISTRIBUTOR,
    CHOOSING_AGENT_OR_DISTRIBUTOR,
    MEET_YOUR_CUSTOMER,
    MANAGE_LANGUAGE_DIFFERENCES,
    GET_MONEY_TO_EXPORT,
    CHOOSE_THE_RIGHT_FINANCE,
    CONSIDER_HOW_PAID,
    ANTI_BRIBERY_AND_CORRUPTION_TRAINING,
    PLAN_THE_LOGISTICS,
    INTERNATIONALISE_WESBITE,
    PROTECT_YOUR_INTELLECTUAL_PROPERTY,
    TYPES_OF_INTELLECTUAL_PROPERTY,
    REPORT_CORRUPTION_AND_HUMAN_RIGHTS_VIOLATIONS,
    UNDERSTAND_YOUR_CUSTOMERS_CULTURE,
    NEXT_STEPS_NEW_EXPORTER,
]


PERSONA_OCCASIONAL_ARTICLES = [
    RESEARCH_YOUR_MARKET,
    DEFINE_MARKET_POTENTIAL,
    DO_FIELD_RESEARCH,
    VISIT_TRADE_SHOW,
    DOING_BUSINESS_WITH_INTEGRITY,
    KNOW_THE_RELEVANT_LEGISLATION,
    ANALYSE_THE_COMPETITION,
    KNOW_YOUR_CUSTOMERS_AND_PARTNERS,
    MAKE_EXPORTING_PLAN,
    FIND_A_ROUTE_TO_MARKET,
    SELL_OVERSEAS_DIRECTLY,
    USE_OVERSEAS_AGENT,
    USE_DISTRIBUTOR,
    CHOOSING_AGENT_OR_DISTRIBUTOR,
    LICENCE_YOUR_PRODUCT_OR_SERVICE,
    START_JOINT_VENTURE,
    MANAGE_LANGUAGE_DIFFERENCES,
    UNDERSTAND_YOUR_CUSTOMERS_CULTURE,
    GET_MONEY_TO_EXPORT,
    CHOOSE_THE_RIGHT_FINANCE,
    GET_EXPORT_FINANCE,
    RAISE_MONEY_BY_BORROWING,
    BORROW_AGAINST_ASSETS,
    RAISE_MONEY_WITH_INVESTMENT,
    GET_GOVERNMENT_FINANCE_SUPPORT,
    CONSIDER_HOW_PAID,
    INVOICE_CURRENCY_AND_CONTENTS,
    DECIDE_WHEN_PAID,
    PAYMENT_METHODS,
    INSURE_AGAINST_NON_PAYMENT,
    USE_FREIGHT_FORWARDER,
    USE_INCOTERMS_IN_CONTRACTS,
    GET_YOUR_EXPORT_DOCUMENTS_RIGHT,
    ANTI_BRIBERY_AND_CORRUPTION_TRAINING,
    INTERNATIONALISE_WESBITE,
    MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE,
    PROTECT_YOUR_INTELLECTUAL_PROPERTY,
    TYPES_OF_INTELLECTUAL_PROPERTY,
    KNOW_WHAT_INTELLECTUAL_PROPERTY_YOU_HAVE,
    INTELLECTUAL_PROPERTY_PROTECTION,
    REPORT_CORRUPTION_AND_HUMAN_RIGHTS_VIOLATIONS,
    NEXT_STEPS_OCCASIONAL_EXPORTER,
]


PERSONA_REGULAR_ARTICLES = [
    DEFINE_MARKET_POTENTIAL,
    DO_FIELD_RESEARCH,
    DOING_BUSINESS_WITH_INTEGRITY,
    KNOW_THE_RELEVANT_LEGISLATION,
    ANALYSE_THE_COMPETITION,
    LICENCE_YOUR_PRODUCT_OR_SERVICE,
    FRANCHISE_YOUR_BUSINESS,
    START_JOINT_VENTURE,
    SETUP_OVERSEAS_OPERATION,
    UNDERSTAND_YOUR_CUSTOMERS_CULTURE,
    CHOOSE_THE_RIGHT_FINANCE,
    GET_EXPORT_FINANCE,
    RAISE_MONEY_BY_BORROWING,
    BORROW_AGAINST_ASSETS,
    RAISE_MONEY_WITH_INVESTMENT,
    GET_GOVERNMENT_FINANCE_SUPPORT,
    INSURE_AGAINST_NON_PAYMENT,
    ANTI_BRIBERY_AND_CORRUPTION_TRAINING,
    KNOW_WHAT_INTELLECTUAL_PROPERTY_YOU_HAVE,
    INTELLECTUAL_PROPERTY_PROTECTION,
    NEXT_STEPS_REGULAR_EXPORTER,
]

GUIDANCE_MARKET_RESEARCH_ARTICLES = [
    RESEARCH_YOUR_MARKET,
    DEFINE_MARKET_POTENTIAL,
    DO_FIELD_RESEARCH,
    ANALYSE_THE_COMPETITION,
    VISIT_TRADE_SHOW,
    DOING_BUSINESS_WITH_INTEGRITY,
    KNOW_THE_RELEVANT_LEGISLATION,
]

GUIDANCE_CUSTOMER_INSIGHT_ARTICLES = [
    KNOW_YOUR_CUSTOMERS_AND_PARTNERS,
    MEET_YOUR_CUSTOMER,
    MANAGE_LANGUAGE_DIFFERENCES,
    UNDERSTAND_YOUR_CUSTOMERS_CULTURE,
]

GUIDANCE_FINANCE_ARTICLES = [
    GET_MONEY_TO_EXPORT,
    CHOOSE_THE_RIGHT_FINANCE,
    GET_EXPORT_FINANCE,
    RAISE_MONEY_BY_BORROWING,
    BORROW_AGAINST_ASSETS,
    RAISE_MONEY_WITH_INVESTMENT,
    GET_GOVERNMENT_FINANCE_SUPPORT,
]

GUIDANCE_BUSINESS_PLANNING_ARTICLES = [
    MAKE_EXPORTING_PLAN,
    FIND_A_ROUTE_TO_MARKET,
    SELL_OVERSEAS_DIRECTLY,
    USE_OVERSEAS_AGENT,
    USE_DISTRIBUTOR,
    CHOOSING_AGENT_OR_DISTRIBUTOR,
    LICENCE_AND_FRANCHISING,
    LICENCE_YOUR_PRODUCT_OR_SERVICE,
    FRANCHISE_YOUR_BUSINESS,
    START_JOINT_VENTURE,
    SETUP_OVERSEAS_OPERATION,
]

GUIDANCE_GETTING_PAID_ARTICLES = [
    CONSIDER_HOW_PAID,
    INVOICE_CURRENCY_AND_CONTENTS,
    DECIDE_WHEN_PAID,
    PAYMENT_METHODS,
    INSURE_AGAINST_NON_PAYMENT,
]

GUIDANCE_OPERATIONS_AND_COMPLIANCE_ARTICLES = [
    ANTI_BRIBERY_AND_CORRUPTION_TRAINING,
    PLAN_THE_LOGISTICS,
    USE_FREIGHT_FORWARDER,
    USE_INCOTERMS_IN_CONTRACTS,
    GET_YOUR_EXPORT_DOCUMENTS_RIGHT,
    INTERNATIONALISE_WESBITE,
    MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE,
    PROTECT_YOUR_INTELLECTUAL_PROPERTY,
    TYPES_OF_INTELLECTUAL_PROPERTY,
    KNOW_WHAT_INTELLECTUAL_PROPERTY_YOU_HAVE,
    INTELLECTUAL_PROPERTY_PROTECTION,
    REPORT_CORRUPTION_AND_HUMAN_RIGHTS_VIOLATIONS,
]

GUIDANCE = {
    "market research": GUIDANCE_MARKET_RESEARCH_ARTICLES,
    "customer insight": GUIDANCE_CUSTOMER_INSIGHT_ARTICLES,
    "finance": GUIDANCE_FINANCE_ARTICLES,
    "business planning": GUIDANCE_BUSINESS_PLANNING_ARTICLES,
    "getting paid": GUIDANCE_GETTING_PAID_ARTICLES,
    "operations and compliance": GUIDANCE_OPERATIONS_AND_COMPLIANCE_ARTICLES,
}

GROUPS = {
    "guidance": GUIDANCE,
    "personalised journey": {
        "regular": GUIDANCE,
        "occasional": PERSONA_OCCASIONAL_ARTICLES,
        "new": PERSONA_NEW_ARTICLES,
    },
    "export readiness": {
        "regular": PERSONA_REGULAR_ARTICLES,
        "occasional": PERSONA_OCCASIONAL_ARTICLES,
        "new": PERSONA_NEW_ARTICLES,
    },
}


def get_articles(
    group: str, category: str, *, sub_category: str = None
) -> list:
    """Get an ordered list of articles for specific group & category.

    NOTE:
    in order to avoid the trouble with creating overly nested structure of
    related articles, a `copy` of article object is created inside the loop,
    that find `previous` and `next` article.

    :param group: Article Group: Guidance, Export Readiness, Triage
    :param category: Category of Articles that belong to a specific Group
    :param sub_category: an article sub-category for Regular exporters
    :return: a list of matching Articles sorted by their category index
    """
    ret = []
    if sub_category is not None:
        sub_category = sub_category.lower()
        articles = GROUPS[group.lower()][category.lower()][sub_category]
    else:
        articles = GROUPS[group.lower()][category.lower()]

    for idx, article in enumerate(articles):
        article = copy(article)
        previous_article = None
        next_article = None

        if (idx - 1) >= 0:
            previous_article = articles[idx - 1]
            previous_article.index = idx - 1

        if (idx + 1) < len(articles):
            next_article = articles[idx + 1]
            next_article.index = idx + 1

        article.index = idx
        article.previous = previous_article
        article.next = next_article
        ret.append(article)
    return ret


def get_random_article(
    group: str, category: str, *, sub_category: str = None
) -> Article:
    group_articles = get_articles(group, category, sub_category=sub_category)
    return random.choice(group_articles)


def get_article(group: str, category: str, name: str) -> Article:
    result = None
    articles = get_articles(group, category)
    for idx, article in enumerate(articles):
        if article.title.lower() == name.lower():
            result = article
    return result
