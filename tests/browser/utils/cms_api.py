# -*- coding: utf-8 -*-
from typing import List

from directory_cms_client.client import cms_api_client


def get_news_articles(service: str) -> List[dict]:
    home_pages = {
        "export readiness": "/api/pages/?type=export_readiness.HomePage"
    }
    endpoint = home_pages[service.lower()]
    response = cms_api_client.get(endpoint).json()
    no_items = len(response["items"])
    error = f"Expected to find 1 ExRed Home Page but found {no_items} instead"
    assert no_items == 1, error
    articles = response["items"][0]["articles"]
    return [
        article for article in articles if "/news/" in article["full_path"]
    ]
