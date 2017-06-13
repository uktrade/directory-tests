# -*- coding: utf-8 -*-
"""FAB Given step implementations."""
import string
import random

from tests.functional.features.ScenarioData import Actor


def unauthenticated_supplier(context, supplier_alias):
    """Will create an instance of an unauthenticated Supplier Actor.

    Will generate a random password for user, which can be used later on during
    registration or signing-in.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used within the scenario's scope
    :type supplier_alias: str
    """
    email = "{}+{}@digital.trade.gov.uk".format(supplier_alias.replace(" ", "_"),
                                                random.randint(100000, 999999))
    password_length = 10
    password = ''.join(random.choice(string.ascii_letters)
                       for i in range(password_length))
    actor = Actor(alias=supplier_alias, email=email, password=password,
                  csrfmiddlewaretoken=None)
    context.add_actor(actor)
