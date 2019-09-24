# -*- coding: utf-8 -*-
from typing import List

from directory_tests_shared.clients import CMS_API_CLIENT


def get_news_articles(service: str, visitor_type: str) -> List[dict]:
    news_slugs = {
        "export readiness": {
            "domestic": "home",
            "international": "international-eu-exit-news",
        }
    }
    slug = news_slugs[service.lower()][visitor_type.lower()]
    response = CMS_API_CLIENT.lookup_by_slug(slug).json()
    articles = response["articles"]
    return [article for article in articles if "news/" in article["full_path"]]
