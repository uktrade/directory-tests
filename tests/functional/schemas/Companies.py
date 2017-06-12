# -*- coding: utf-8 -*-
"""JSON Schema for Companies House Search Result.

Use it with JSON response from: FAB api/internal/companies-house-search
"""

COMPANIES = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "definitions": {},
    "id": "https://find-a-buyer.export.great.gov.uk/api/internal/companies-house-search/",
    "items": {
        "id": "/items",
        "properties": {
            "address": {
                "id": "/items/properties/address",
                "properties": {
                    "country": {
                        "id": "/items/properties/address/properties/country",
                        "type": "string"
                    },
                    "locality": {
                        "id": "/items/properties/address/properties/locality",
                        "type": "string"
                    },
                    "postal_code": {
                        "id": "/items/properties/address/properties/postal_code",
                        "type": "string"
                    },
                    "premises": {
                        "id": "/items/properties/address/properties/premises",
                        "type": "string"
                    },
                    "address_line_1": {
                        "id": "/items/properties/address/properties/address_line_1",
                        "type": "string"
                    }
                },
                "required": [
                    "premises",
                    "locality"
                ],
                "type": "object"
            },
            "address_snippet": {
                "id": "/items/properties/address_snippet",
                "type": "string"
            },
            "company_number": {
                "id": "/items/properties/company_number",
                "type": "string"
            },
            "company_status": {
                "id": "/items/properties/company_status",
                "type": "string"
            },
            "company_type": {
                "id": "/items/properties/company_type",
                "type": "string"
            },
            "date_of_creation": {
                "id": "/items/properties/date_of_creation",
                "type": "string"
            },
            "description": {
                "id": "/items/properties/description",
                "type": "string"
            },
            "description_identifier": {
                "id": "/items/properties/description_identifier",
                "items": {
                    "id": "/items/properties/description_identifier/items",
                    "type": "string"
                },
                "type": "array"
            },
            "kind": {
                "id": "/items/properties/kind",
                "type": "string"
            },
            "links": {
                "id": "/items/properties/links",
                "properties": {
                    "self": {
                        "id": "/items/properties/links/properties/self",
                        "type": "string"
                    }
                },
                "required": [
                    "self"
                ],
                "type": "object"
            },
            "matches": {
                "id": "/items/properties/matches",
                "properties": {
                    "snippet": {
                        "id": "/items/properties/matches/properties/snippet",
                        "items": {},
                        "type": "array"
                    },
                    "title": {
                        "id": "/items/properties/matches/properties/title",
                        "items": {
                            "id": "/items/properties/matches/properties/title/items",
                            "type": "integer"
                        },
                        "type": "array"
                    }
                },
                "required": [
                    "snippet",
                    "title"
                ],
                "type": "object"
            },
            "snippet": {
                "id": "/items/properties/snippet",
                "type": "string"
            },
            "title": {
                "id": "/items/properties/title",
                "type": "string"
            }
        },
        "required": [
            "date_of_creation",
            "kind",
            "description",
            "links",
            "title",
            "company_type",
            "address_snippet",
            "company_number",
            "company_status",
            "address",
            "description_identifier"
        ],
        "type": "object"
    },
    "type": "array"
}
