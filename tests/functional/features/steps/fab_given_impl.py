# -*- coding: utf-8 -*-
"""FAB Given step implementations."""
from tests.functional.features.ScenarioData import Actor


def unauthenticated_supplier(context, supplier_alias):
    """Will create an instance of an unauthenticated Supplier Actor.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used within the scenario's scope
    :type supplier_alias: str
    """
    actor = Actor(alias=supplier_alias)
    context.add_actor(actor)
