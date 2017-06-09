# -*- coding: utf-8 -*-
"""FAB Given step implementations."""

from tests.functional.features.ScenarioData import Actor


def unauthenticated_supplier(context, supplier_alias):
    actor = Actor(alias=supplier_alias, http_client=None)
    context.add_actor(actor)
