# -*- coding: utf-8 -*-
from typing import List

from directory_cms_client.client import cms_api_client


def get_news_articles(service: str, visitor_type: str) -> List[dict]:
    news_slugs = {
        "export readiness": {
            "domestic": "home",
            "international": "international-news",
        },
    }
    slug = news_slugs[service.lower()][visitor_type.lower()]
    response = cms_api_client.lookup_by_slug(slug).json()
    articles = response["articles"]
    return [article for article in articles if "news/" in article["full_path"]]
