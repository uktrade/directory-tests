# -*- coding: utf-8 -*-
"""ExRed Articles Registry"""

ARTICLES = {
    "analyse the competition": {
        "time to read": 0,
        "guidance": {
            "market research": {
                "index": 4,
                "previous": "do field research",
                "next": "visit a trade show"
            }
        },
        "personalised journey": {
            "occasional": {
                "index": 3,
                "previous": "do field research",
                "next": "know your customers"
            }
        },
        "export readiness": {
            "occasional": {
                "index": 5,
                "next": "know your customers",
                "previous": "visit a trade show"
            },
            "regular": {
                "index": 3,
                "next": "license your product or service",
                "previous": "do field research"
            }
        }
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
        "personalised journey": {
            "occasional": {
                "index": 11,
                "previous": "raise money by borrowing",
                "next": "raise money with investment"
            }
        },
        "export readiness": {
            "occasional": {
                "index": 20,
                "next": "raise money with investment",
                "previous": "raise money by borrowing"
            },
            "regular": {
                "index": 12,
                "next": "raise money with investment",
                "previous": "raise money by borrowing"
            }
        }
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
        "personalised journey": {
            "occasional": {
                "index": 8,
                "previous": "get money to export",
                "next": "get export finance"
            }
        },
        "export readiness": {
            "new": {
                "index": 11,
                "previous": "get money to export",
                "next": "consider how you'll get paid"
            },
            "occasional": {
                "index": 17,
                "next": "get export finance",
                "previous": "get money to export"
            },
            "regular": {
                "index": 9,
                "next": "get export finance",
                "previous": "understand your customer's culture"
            }
        },
    },
    "choosing an agent or distributor": {
        "time to read": 0,
        "guidance": {
            "business planning": {
                "index": 6,
                "previous": "use a distributor",
                "next": "licensing and franchising"
            }
        },
        "personalised journey": {
            "occasional": {
                "index": 18,
                "previous": "use a distributor",
                "next": "license your product or service"
            }
        },
        "export readiness": {
            "new": {
                "index": 7,
                "previous": "use a distributor",
                "next": "meet your customers"
            },
            "occasional": {
                "index": 11,
                "next": "license your product or service",
                "previous": "use a distributor"
            }
        },
    },
    "consider how you'll get paid": {
        "time to read": 0,
        "guidance": {
            "getting paid": {
                "index": 1,
                "previous": None,
                "next": "invoice currency and contents"
            }
        },
        "personalised journey": {
            "new": {
                "index": 10,
                "previous": "use a distributor",
                "next": "plan the logistics"
            },
            "occasional": {
                "index": 21,
                "previous": "start a joint venture",
                "next": "invoice currency and contents"
            }
        },
        "export readiness": {
            "new": {
                "index": 12,
                "previous": "choose the right finance",
                "next": "plan the logistics"
            },
            "occasional": {
                "index": 23,
                "next": "invoice currency and contents",
                "previous": "get finance support from government"
            }
        },
    },
    "decide when you'll get paid": {
        "time to read": 0,
        "guidance": {
            "getting paid": {
                "index": 3,
                "previous": "invoice currency and contents",
                "next": "payment methods"
            }
        },
        "personalised journey": {
            "occasional": {
                "index": 23,
                "previous": "invoice currency and contents",
                "next": "payment methods"
            }
        },
        "export readiness": {
            "occasional": {
                "index": 25,
                "next": "payment methods",
                "previous": "invoice currency and contents"
            }
        }
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
        "personalised journey": {
            "occasional": {
                "index": 1,
                "previous": None,
                "next": "do field research"
            }
        },
        "export readiness": {
            "occasional": {
                "index": 2,
                "previous": "do research first",
                "next": "do field research"
            },
            "regular": {
                "index": 1,
                "next": "do field research",
                "previous": None
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
        "personalised journey": {
            "occasional": {
                "index": 2,
                "previous": "define market potential",
                "next": "analyse the competition"
            }
        },
        "export readiness": {
            "occasional": {
                "index": 3,
                "previous": "define market potential",
                "next": "visit a trade show"
            },
            "regular": {
                "index": 2,
                "next": "analyse the competition",
                "previous": "define market potential"
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
        "personalised journey": {
            "new": {
                "index": 1,
                "previous": None,
                "next": "know your customers"
            }
        },
        "export readiness": {
            "new": {
                "index": 1,
                "previous": None,
                "next": "know your customers"
            },
            "occasional": {
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
                "next": "sell overseas directly"
            }
        },
        "personalised journey": {
            "new": {
                "index": 7,
                "previous": "make an export plan",
                "next": "use an overseas agent"
            },
            "occasional": {
                "index": 15,
                "previous": "make an export plan",
                "next": "use an overseas agent"
            }
        },
        "export readiness": {
            "new": {
                "index": 4,
                "previous": "make an export plan",
                "next": "use an overseas agent"
            },
            "occasional": {
                "index": 8,
                "next": "use an overseas agent",
                "previous": "make an export plan"
            }
        },
    },
    "franchise your business": {
        "time to read": 0,
        "guidance": {
            "business planning": {
                "index": 9,
                "previous": "license your product or service",
                "next": "start a joint venture"
            }
        },
        "export readiness": {
            "regular": {
                "index": 5,
                "next": "start a joint venture",
                "previous": "license your product or service"
            }
        }
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
        "personalised journey": {
            "occasional": {
                "index": 9,
                "previous": "choose the right finance",
                "next": "raise money by borrowing"
            }
        },
        "export readiness": {
            "occasional": {
                "index": 18,
                "next": "raise money by borrowing",
                "previous": "choose the right finance"
            },
            "regular": {
                "index": 10,
                "next": "raise money by borrowing",
                "previous": "choose the right finance"
            }
        }
    },
    "get finance support from government": {
        "time to read": 0,
        "guidance": {
            "finance": {
                "index": 7,
                "previous": "raise money with investment",
                "next": None
            }
        },
        "personalised journey": {
            "occasional": {
                "index": 13,
                "previous": "raise money with investment",
                "next": "make an export plan"
            }
        },
        "export readiness": {
            "occasional": {
                "index": 22,
                "next": "consider how you'll get paid",
                "previous": "raise money with investment"
            },
            "regular": {
                "index": 14,
                "next": "insure against non-payment",
                "previous": "raise money with investment"
            }
        }
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
        "personalised journey": {
            "new": {
                "index": 5,
                "previous": "manage language differences",
                "next": "make an export plan"
            },
            "occasional": {
                "index": 7,
                "previous": "understand your customer's culture",
                "next": "choose the right finance"
            }
        },
        "export readiness": {
            "new": {
                "index": 10,
                "previous": "manage language differences",
                "next": "choose the right finance"
            },
            "occasional": {
                "index": 16,
                "next": "choose the right finance",
                "previous": "understand your customer's culture"
            }
        },
    },
    "get your export documents right": {
        "time to read": 0,
        "guidance": {
            "operations and compliance": {
                "index": 4,
                "previous": "user incoterms in contracts",
                "next": "match your website to your audience"
            }
        },
        "personalised journey": {
            "occasional": {
                "index": 28,
                "previous": "user incoterms in contracts",
                "next": "match your website to your audience"
            }
        },
        "export readiness": {
            "occasional": {
                "index": 30,
                "next": "internationalise your website",
                "previous": "user incoterms in contracts"
            }
        }
    },
    "ip protection in multiple countries": {
        "time to read": 0,
        "guidance": {
            "operations and compliance": {
                "index": 10,
                "previous": "know what IP you have",
                "next": None
            }
        },
        "personalised journey": {
            "occasional": {
                "index": 34,
                "previous": "know what ip you have",
                "next": None
            }
        },
        "export readiness": {
            "occasional": {
                "index": 36,
                "next": "next steps for occasional exporters",
                "previous": "know what IP you have"
            },
            "regular": {
                "index": 17,
                "next": "next steps for regular exporters",
                "previous": "know what IP you have"
            }
        }
    },
    "insure against non-payment": {
        "time to read": 0,
        "guidance": {
            "getting paid": {
                "index": 5,
                "previous": "payment methods",
                "next": None
            }
        },
        "personalised journey": {
            "occasional": {
                "index": 25,
                "previous": "payment methods",
                "next": "use a freight forwarder"
            }
        },
        "export readiness": {
            "occasional": {
                "index": 27,
                "next": "use a freight forwarder",
                "previous": "payment methods"
            },
            "regular": {
                "index": 15,
                "next": "know what IP you have",
                "previous": "get finance support from government"
            }
        }
    },
    "internationalise your website": {
        "time to read": 0,
        "guidance": {
            "operations and compliance": {
                "index": 6,
                "previous": "match your website to your audience",
                "next": "what intellectual property is"
            }
        },
        "personalised journey": {
            "new": {
                "index": 12,
                "previous": "plan the logistics",
                "next": "what intellectual property is"
            },
            "occasional": {
                "index": 30,
                "previous": "match your website to your audience",
                "next": "what intellectual property is"
            }
        },
        "export readiness": {
            "new": {
                "index": 14,
                "previous": "plan the logistics",
                "next": "what intellectual property is"
            },
            "occasional": {
                "index": 31,
                "next": "match your website to your audience",
                "previous": "get your export documents right"
            }
        },
    },
    "invoice currency and contents": {
        "time to read": 0,
        "guidance": {
            "getting paid": {
                "index": 2,
                "previous": "consider how you'll get paid",
                "next": "decide when you'll get paid"
            }
        },
        "personalised journey": {
            "occasional": {
                "index": 22,
                "previous": "consider how you'll get paid",
                "next": "decide when you'll get paid"
            }
        },
        "export readiness": {
            "occasional": {
                "index": 24,
                "next": "decide when you'll get paid",
                "previous": "consider how you'll get paid"
            }
        }
    },
    "know what ip you have": {
        "time to read": 0,
        "guidance": {
            "operations and compliance": {
                "index": 9,
                "previous": "types of intellectual property",
                "next": "ip protection in multiple countries"
            }
        },
        "personalised journey": {
            "occasional": {
                "index": 33,
                "previous": "types of intellectual property",
                "next": "ip protection in multiple countries"
            }
        },
        "export readiness": {
            "occasional": {
                "index": 35,
                "next": "ip protection in multiple countries",
                "previous": "types of intellectual property"
            },
            "regular": {
                "index": 16,
                "next": "ip protection in multiple countries",
                "previous": "insure against non-payment"
            }
        }
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
        "personalised journey": {
            "new": {
                "index": 2,
                "previous": "do research first",
                "next": "meet your customers"
            },
            "occasional": {
                "index": 4,
                "previous": "analyse the competition",
                "next": "manage language differences"
            },
        },
        "export readiness": {
            "new": {
                "index": 2,
                "previous": "do research first",
                "next": "make an export plan"
            },
            "occasional": {
                "index": 6,
                "next": "make an export plan",
                "previous": "analyse the competition"
            },
        },
    },
    "licensing and franchising": {
        "time to read": 0,
        "guidance": {
            "business planning": {
                "index": 7,
                "previous": "choosing an agent or distributor",
                "next": "license your product or service"
            }
        },
    },
    "license your product or service": {
        "time to read": 0,
        "guidance": {
            "business planning": {
                "index": 8,
                "previous": "licensing and franchising",
                "next": "franchise your business"
            }
        },
        "personalised journey": {
            "occasional": {
                "index": 19,
                "previous": "choosing an agent or distributor",
                "next": "start a joint venture"
            }
        },
        "export readiness": {
            "occasional": {
                "index": 12,
                "next": "start a joint venture",
                "previous": "choosing an agent or distributor"
            },
            "regular": {
                "index": 4,
                "next": "franchise your business",
                "previous": "analyse the competition"
            }
        }
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
        "personalised journey": {
            "new": {
                "index": 6,
                "previous": "get money to export",
                "next": "find a route to market"
            },
            "occasional": {
                "index": 14,
                "previous": "get finance support from government",
                "next": "find a route to market"
            }
        },
        "export readiness": {
            "new": {
                "index": 3,
                "previous": "know your customers",
                "next": "find a route to market"
            },
            "occasional": {
                "index": 7,
                "next": "find a route to market",
                "previous": "know your customers"
            }
        },
    },
    "manage language differences": {
        "time to read": 0,
        "guidance": {
            "customer insight": {
                "index": 3,
                "previous": "meet your customers",
                "next": "understand your customer's culture"
            }
        },
        "personalised journey": {
            "new": {
                "index": 4,
                "previous": "meet your customers",
                "next": "get money to export"
            },
            "occasional": {
                "index": 5,
                "previous": "know your customers",
                "next": "understand your customer's culture"
            }
        },
        "export readiness": {
            "new": {
                "index": 9,
                "previous": "meet your customers",
                "next": "get money to export"
            },
            "occasional": {
                "index": 14,
                "next": "understand your customer's culture",
                "previous": "start a joint venture"
            }
        },
    },
    "match your website to your audience": {
        "time to read": 0,
        "guidance": {
            "operations and compliance": {
                "index": 5,
                "previous": "get your export documents right",
                "next": "internationalise your website"
            }
        },
        "personalised journey": {
            "occasional": {
                "index": 29,
                "previous": "get your export documents right",
                "next": "internationalise your website"
            }
        },
        "export readiness": {
            "occasional": {
                "index": 32,
                "next": "what intellectual property is",
                "previous": "internationalise your website"
            }
        }
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
        "personalised journey": {
            "new": {
                "index": 3,
                "previous": "know your customers",
                "next": "manage language differences"
            }
        },
        "export readiness": {
            "new": {
                "index": 8,
                "previous": "choosing an agent or distributor",
                "next": "manage language differences"
            },
        },
    },
    "next steps for new to exporting": {
        "time to read": 0,
        "export readiness": {
            "new": {
                "index": 17,
                "previous": "types of intellectual property",
                "next": None
            },
        },
    },
    "next steps for occasional exporters": {
        "time to read": 0,
        "export readiness": {
            "occasional": {
                "index": 37,
                "next": None,
                "previous": "ip protection in multiple countries"
            },
        },
    },
    "next steps for regular exporters": {
        "time to read": 0,
        "export readiness": {
            "regular": {
                "index": 18,
                "next": None,
                "previous": "ip protection in multiple countries"
            }
        },
    },
    "payment methods": {
        "time to read": 0,
        "guidance": {
            "getting paid": {
                "index": 4,
                "previous": "decide when you'll get paid",
                "next": "insure against non-payment"
            }
        },
        "personalised journey": {
            "occasional": {
                "index": 24,
                "previous": "decide when you'll get paid",
                "next": "insure against non-payment"
            }
        },
        "export readiness": {
            "occasional": {
                "index": 26,
                "next": "insure against non-payment",
                "previous": "decide when you'll get paid"
            }
        }
    },
    "plan the logistics": {
        "time to read": 0,
        "guidance": {
            "operations and compliance": {
                "index": 1,
                "previous": None,
                "next": "use a freight forwarder"
            }
        },
        "personalised journey": {
            "new": {
                "index": 11,
                "previous": "consider how you'll get paid",
                "next": "internationalise your website"
            }
        },
        "export readiness": {
            "new": {
                "index": 13,
                "previous": "consider how you'll get paid",
                "next": "internationalise your website"
            },
        },
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
        "personalised journey": {
            "occasional": {
                "index": 10,
                "previous": "get export finance",
                "next": "borrow against assets"
            }
        },
        "export readiness": {
            "occasional": {
                "index": 19,
                "next": "borrow against assets",
                "previous": "get export finance"
            },
            "regular": {
                "index": 11,
                "next": "borrow against assets",
                "previous": "get export finance"
            }
        }
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
        "personalised journey": {
            "occasional": {
                "index": 12,
                "previous": "borrow against assets",
                "next": "get finance support from government"
            }
        },
        "export readiness": {
            "occasional": {
                "index": 21,
                "next": "get finance support from government",
                "previous": "borrow against assets"
            },
            "regular": {
                "index": 13,
                "next": "get finance support from government",
                "previous": "borrow against assets"
            }
        }
    },
    "sell overseas directly": {
        "time to read": 0,
        "guidance": {
            "business planning": {
                "index": 3,
                "previous": "find a route to market",
                "next": "use an overseas agent"
            }
        },
    },
    "set up an overseas operation": {
        "time to read": 0,
        "guidance": {
            "business planning": {
                "index": 11,
                "previous": "start a joint venture",
                "next": None
            }
        },
        "export readiness": {
            "regular": {
                "index": 7,
                "next": "understand your customer's culture",
                "previous": "start a joint venture"
            }
        },
    },
    "start a joint venture": {
        "time to read": 0,
        "guidance": {
            "business planning": {
                "index": 10,
                "previous": "franchise your business",
                "next": "set up an overseas operation"
            }
        },
        "personalised journey": {
            "occasional": {
                "index": 20,
                "previous": "license your product or service",
                "next": "consider how you'll get paid"
            }
        },
        "export readiness": {
            "occasional": {
                "index": 13,
                "next": "manage language differences",
                "previous": "license your product or service"
            },
            "regular": {
                "index": 6,
                "next": "set up an overseas operation",
                "previous": "franchise your business"
            }
        }
    },
    "types of intellectual property": {
        "time to read": 0,
        "guidance": {
            "operations and compliance": {
                "index": 8,
                "previous": "what intellectual property is",
                "next": "know what IP you have"
            }
        },
        "personalised journey": {
            "new": {
                "index": 14,
                "previous": "what intellectual property is",
                "next": None
            },
            "occasional": {
                "index": 32,
                "previous": "what intellectual property is",
                "next": "know what ip you have"
            }
        },
        "export readiness": {
            "new": {
                "index": 16,
                "previous": "what intellectual property is",
                "next": "next steps for new to exporting"
            },
            "occasional": {
                "index": 34,
                "next": "know what IP you have",
                "previous": "what intellectual property is"
            }
        },
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
        "personalised journey": {
            "occasional": {
                "index": 6,
                "previous": "manage language differences",
                "next": "get money to export"
            }
        },
        "export readiness": {
            "occasional": {
                "index": 15,
                "next": "get money to export",
                "previous": "manage language differences"
            },
            "regular": {
                "index": 8,
                "next": "choose the right finance",
                "previous": "set up an overseas operation"
            },
        }
    },
    "use a distributor": {
        "time to read": 0,
        "guidance": {
            "business planning": {
                "index": 5,
                "previous": "use an overseas agent",
                "next": "choosing an agent or distributor"
            }
        },
        "personalised journey": {
            "new": {
                "index": 9,
                "previous": "use an overseas agent",
                "next": "consider how you'll get paid"
            },
            "occasional": {
                "index": 17,
                "previous": "use an overseas agent",
                "next": "choosing an agent or distributor"
            }
        },
        "export readiness": {
            "new": {
                "index": 6,
                "previous": "use an overseas agent",
                "next": "choosing an agent or distributor"
            },
            "occasional": {
                "index": 10,
                "next": "choosing an agent or distributor",
                "previous": "use an overseas agent"
            }
        },
    },
    "use a freight forwarder": {
        "time to read": 0,
        "guidance": {
            "operations and compliance": {
                "index": 2,
                "previous": "plan the logistics",
                "next": "user incoterms in contracts"
            }
        },
        "personalised journey": {
            "occasional": {
                "index": 26,
                "previous": "insure against non-payment",
                "next": "user incoterms in contracts"
            }
        },
        "export readiness": {
            "occasional": {
                "index": 28,
                "next": "user incoterms in contracts",
                "previous": "insure against non-payment"
            }
        }
    },
    "use an overseas agent": {
        "time to read": 0,
        "guidance": {
            "business planning": {
                "index": 4,
                "previous": "sell overseas directly",
                "next": "use a distributor"
            }
        },
        "personalised journey": {
            "new": {
                "index": 8,
                "previous": "find a route to market",
                "next": "use a distributor"
            },
            "occasional": {
                "index": 16,
                "previous": "find a route to market",
                "next": "use a distributor"
            }
        },
        "export readiness": {
            "new": {
                "index": 5,
                "previous": "find a route to market",
                "next": "use a distributor"
            },
            "occasional": {
                "index": 9,
                "next": "use a distributor",
                "previous": "find a route to market"
            }
        },
    },
    "user incoterms in contracts": {
        "time to read": 0,
        "guidance": {
            "operations and compliance": {
                "index": 3,
                "previous": "use a freight forwarder",
                "next": "get your export documents right"
            }
        },
        "personalised journey": {
            "occasional": {
                "index": 27,
                "previous": "use a freight forwarder",
                "next": "get your export documents right"
            }
        },
        "export readiness": {
            "occasional": {
                "index": 29,
                "next": "get your export documents right",
                "previous": "use a freight forwarder"
            }
        }
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
        "export readiness": {
            "occasional": {
                "index": 4,
                "next": "analyse the competition",
                "previous": "do field research"
            }
        }
    },
    "what intellectual property is": {
        "time to read": 0,
        "guidance": {
            "operations and compliance": {
                "index": 7,
                "previous": "internationalise your website",
                "next": "types of intellectual property"
            }
        },
        "personalised journey": {
            "new": {
                "index": 13,
                "previous": "internationalise your website",
                "next": "types of intellectual property"
            },
            "occasional": {
                "index": 31,
                "previous": "internationalise your website",
                "next": "types of intellectual property"
            }
        },
        "export readiness": {
            "new": {
                "index": 15,
                "previous": "internationalise your website",
                "next": "types of intellectual property"
            },
            "occasional": {
                "index": 33,
                "next": "types of intellectual property",
                "previous": "match your website to your audience"
            }
        },
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
    filtered = filter_articles(group.lower(), category.lower())
    return sorted(filtered, key=get_article_index)


def find_article(group: str, category: str, name: str) -> dict:
    result = {}
    articles = get_articles(group, category)
    for idx, article in enumerate(articles):
        current = list(article.keys())[0]
        if current == name:
            if (idx - 1) >= 0:
                prev_name = list(articles[idx-1].keys())[0]
                prev_article = {
                    "index": articles[idx-1][prev_name]['index'],
                    "name": prev_name,
                    "next": articles[idx-1][prev_name]['next'],
                    "previous": articles[idx-1][prev_name]['previous'],
                    "time to read": articles[idx-1][prev_name]['time to read'],
                }
            else:
                prev_article = None

            if (idx + 1) < len(articles):
                next_name = list(articles[idx+1].keys())[0]
                next_article = {
                    "index": articles[idx+1][next_name]['index'],
                    "name": next_name,
                    "next": articles[idx+1][next_name]['next'],
                    "previous": articles[idx+1][next_name]['previous'],
                    "time to read": articles[idx+1][next_name]['time to read'],
                }
            else:
                next_article = None

            result = {
                "index": article[current]['index'],
                "name": current,
                "next": next_article,
                "previous": prev_article,
                "time to read": article[current]['time to read']
            }
    return result


def get_first_article(group: str, category: str) -> dict:
    articles = get_articles(group, category)
    name = list(articles[0].keys())[0]
    return find_article(group, category, name)
