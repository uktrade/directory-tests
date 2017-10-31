# -*- coding: utf-8 -*-
"""ExRed Page Object Registry"""

from pages import (
    home,
    triage_what_is_your_sector,
    triage_have_you_exported,
    triage_are_you_regular_exporter,
    triage_company_name,
    triage_result,
    personalised_journey,
    triage_do_you_use_online_marketplaces,
    triage_are_you_registered_with_companies_house
)


EXRED_PAGE_REGISTRY = {
    "home": {
        "url": home.URL,
        "po": home
    },
    "triage - what is your sector": {
        "url": triage_what_is_your_sector.URL,
        "po": triage_what_is_your_sector
    },
    "triage - have you exported before": {
        "url": triage_have_you_exported.URL,
        "po": triage_have_you_exported
    },
    "triage - are you regular exporter": {
        "url": triage_are_you_regular_exporter.URL,
        "po": triage_are_you_regular_exporter
    },
    "triage - do you use online marketplaces": {
        "url": triage_do_you_use_online_marketplaces.URL,
        "po": triage_do_you_use_online_marketplaces
    },
    "triage - are you registered with companies house": {
        "url": triage_are_you_registered_with_companies_house.URL,
        "po": triage_are_you_registered_with_companies_house
    },
    "triage - what is your company name": {
        "url": triage_company_name.URL,
        "po": triage_company_name
    },
    "triage - result": {
        "url": triage_result.URL,
        "po": triage_result
    },
    "personalised journey": {
        "url": personalised_journey.URL,
        "po": personalised_journey
    },
}


def get_page_url(page_name: str):
    return EXRED_PAGE_REGISTRY[page_name.lower()]["url"]


def get_page_object(page_name: str):
    return EXRED_PAGE_REGISTRY[page_name.lower()]["po"]


ARTICLES = {
    "ip protection in multiple countries": {
    },
    "analyse the competition": {
        "time to read": 0,
        "guidance": {
            "market research": {
                "index": 4,
                "previous": "do field research",
                "next": "visit a trade show"
            }
        },
    },
    "borrow against assets": {
        "time to read": 0,
        "guidance": {
            "finance": {
                "index": 5,
                "previous": "raise money by borrowing",
                "next": None
            }
        },
    },
    "choose the right finance": {
        "time to read": 0,
        "guidance": {
            "finance": {
                "index": 2,
                "previous": "get money to export",
                "next": "get export finance"
            }
        },
    },
    "choosing an agent or distributor": {
        "time to read": 0,
        "guidance": {
            "business planning": {
                "index": 5,
                "previous": "use a distributor",
                "next": "licensing and franchising"
            }
        },
    },
    "consider how you'll get paid": {

    },
    "decide when you'll get paid": {

    },
    "define market potential": {
        "time to read": 0,
        "guidance": {
            "market research": {
                "index": 2,
                "previous": "do research first",
                "next": "do field research"
            }
        },
    },
    "do field research": {
        "time to read": 0,
        "guidance": {
            "market research": {
                "index": 3,
                "previous": "define market potential",
                "next": "analyse the competition"
            }
        },
    },
    "do research first": {
        "time to read": 0,
        "guidance": {
            "market research": {
                "index": 1,
                "previous": None,
                "next": "define market potential"
            }
        },
    },
    "find a route to market": {
        "time to read": 0,
        "guidance": {
            "business planning": {
                "index": 2,
                "previous": "make an export plan",
                "next": "use an overseas agent"
            }
        },
    },
    "franchise your business": {
        "time to read": 0,
        "guidance": {
            "business planning": {
                "index": 8,
                "previous": "license your product or service",
                "next": "start a joint venture"
            }
        },
    },
    "get export finance": {
        "time to read": 0,
        "guidance": {
            "finance": {
                "index": 3,
                "previous": "choose the right finance",
                "next": "raise money by borrowing"
            }
        },
    },
    "get government finance support": {
        "time to read": 0,
        "guidance": {
            "finance": {
                "index": 7,
                "previous": "raise money with investment",
                "next": None
            }
        },
    },
    "get money to export": {
        "time to read": 0,
        "guidance": {
            "finance": {
                "index": 1,
                "previous": None,
                "next": "choose the right finance"
            }
        },
    },
    "get your export documents right": {

    },
    "iP protection in multiple countries": {

    },
    "insure against non-payment": {

    },
    "internationalise your website": {

    },
    "invoice currency and contents": {

    },
    "know what IP you have": {

    },
    "know your customers": {
        "time to read": 0,
        "guidance": {
            "customer insight": {
                "index": 1,
                "previous": None,
                "next": "meet your customers"
            }
        },
    },
    "licensing and franchising": {
        "time to read": 0,
        "guidance": {
            "business planning": {
                "index": 6,
                "previous": "choosing an agent or distributor",
                "next": "license your product or service"
            }
        },
    },
    "license your product or service": {
        "time to read": 0,
        "guidance": {
            "business planning": {
                "index": 7,
                "previous": "licensing and franchising",
                "next": "franchise your business"
            }
        },
    },
    "make an export plan": {
        "time to read": 0,
        "guidance": {
            "business planning": {
                "index": 1,
                "previous": None,
                "next": "find a route to market"
            }
        },
    },
    "manage language differences": {
        "time to read": 0,
        "guidance": {
            "customer insight": {
                "index": 3,
                "previous": "meet your customers",
                "next": "Understand your customer's culture"
            }
        },
    },
    "match your website to your audience": {

    },
    "meet your customers": {
        "time to read": 0,
        "guidance": {
            "customer insight": {
                "index": 2,
                "previous": "meet your customers",
                "next": "manage language differences"
            }
        },
    },
    "payment methods": {

    },
    "plan the logistics": {

    },
    "raise money by borrowing": {
        "time to read": 0,
        "guidance": {
            "finance": {
                "index": 4,
                "previous": "get export finance",
                "next": "borrow against assets"
            }
        },
    },
    "raise money with investment": {
        "time to read": 0,
        "guidance": {
            "finance": {
                "index": 6,
                "previous": None,
                "next": None
            }
        },
    },
    "set up an overseas operation": {
        "time to read": 0,
        "guidance": {
            "business planning": {
                "index": 10,
                "previous": "start a joint venture",
                "next": None
            }
        },
    },
    "start a joint venture": {
        "time to read": 0,
        "guidance": {
            "business planning": {
                "index": 9,
                "previous": "franchise your business",
                "next": "set up an overseas operation"
            }
        },
    },
    "types of intellectual property": {

    },
    "understand your customer's culture": {
        "time to read": 0,
        "guidance": {
            "customer insight": {
                "index": 4,
                "previous": "manage language differences",
                "next": None
            }
        },
    },
    "use a distributor": {
        "time to read": 0,
        "guidance": {
            "business planning": {
                "index": 4,
                "previous": "use an overseas agent",
                "next": "choosing an agent or distributor"
            }
        },
    },
    "use a freight forwarder": {

    },
    "use an overseas agent": {
        "time to read": 0,
        "guidance": {
            "business planning": {
                "index": 3,
                "previous": "find a route to market",
                "next": "use a distributor"
            }
        },
    },
    "user incoterms in contracts": {

    },
    "visit a trade show": {
        "time to read": 0,
        "guidance": {
            "market research": {
                "index": 5,
                "previous": "analyse the competition",
                "next": None
            }
        },
    },
    "what intellectual property is": {

    },
}


def filter_articles(group: str, category: str) -> list:
    """Filter articles by group and category.

    :param group: Article Group: Guidance, Export Readiness, Triage
    :param category: Category of Articles that belong to a specific Group
    :return: a list of matching Article dictionaries
    """
    filtered = [{
                name: {
                    "index": ARTICLES[name][group][category]["index"],
                    "time to read": ARTICLES[name]["time to read"],
                    "previous": ARTICLES[name][group][category]["previous"],
                    "next": ARTICLES[name][group][category]["next"],
                }} for name in ARTICLES if
                group in ARTICLES[name] and category in ARTICLES[name][group]]
    return filtered


def get_article_index(dictionary: dict) -> int:
    """Get Article index. Handy when sorting articles by index.

    :param dictionary: a dict with one key and dict as value that has index key
    :return: the article index value
    """
    return list(dictionary.values())[0]['index']


def get_articles(group: str, category: str) -> list:
    """Find matching articles and sort them by their category index.

    :param group: Article Group: Guidance, Export Readiness, Triage
    :param category: Category of Articles that belong to a specific Group
    :return: a list of matching Article sorted by their category index
    """
    filtered = filter_articles(group, category)
    return sorted(filtered, key=get_article_index)
