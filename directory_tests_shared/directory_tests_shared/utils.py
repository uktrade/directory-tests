# -*- coding: utf-8 -*-
import logging
import sys
import traceback
import uuid
from contextlib import contextmanager
from random import choice, randint
from typing import Union

from .constants import OPERATING_COUNTRIES, PRODUCT_CATEGORIES, RARE_WORDS, SECTORS
from .settings import BASICAUTH_PASS, BASICAUTH_USER


def get_random_email_address():
    return "{}@example.com".format(uuid.uuid4())


def retriable_error(exception):
    """Return True if test should be re-run based on the Exception"""
    return isinstance(exception, (AssertionError,))


def is_500(exception):
    """Return True exception message contains 500"""
    return "500" in str(exception)


def basic_auth():
    return BASICAUTH_USER, BASICAUTH_PASS


def sentence(
    *,
    max_length: int = 60,
    min_word_length: int = 9,
    max_words: int = 10,
    min_words: int = 3,
) -> str:
    """Generate a random string consisting of rare english words.

    NOTE:
    min_word_length is set to 9, because all words in RARE_WORDS are at least 9
    characters long

    :return: a sentence consisting of rare english words
    """
    words = []
    assert min_words <= max_words
    number_of_words = randint(min_words, max_words)
    while len(words) < number_of_words:
        word = choice(RARE_WORDS)
        if len(word) > min_word_length:
            words.append(word)
    while 0 < max_length < len(" ".join(words)):
        words.pop()
    return " ".join(words)


def rare_word(*, min_length: int = 9, max_length: int = 20):
    """Get a random rare english word.

    NOTE:
    min_length is set to 9, because all words in RARE_WORDS are at least 9
    characters long

    :return: a rare english word
    """
    assert min_length < max_length
    word = ""
    while min_length >= len(word) <= max_length:
        word = choice(RARE_WORDS)
    return word


def random_company_number() -> str:
    return str(randint(0, 9999999)).zfill(8)


def random_sector() -> str:
    return choice(SECTORS)


def random_product_categories() -> str:
    return choice(PRODUCT_CATEGORIES)


def random_operating_countries() -> str:
    return choice(OPERATING_COUNTRIES)


def check_for_errors(source: str, url: str):
    assert "404 Not Found" not in source, f"404 Not Found → {url}"
    assert "This page cannot be found" not in source, f"404 Not Found → {url}"
    assert "Internal Server Error" not in source, f"500 ISE → {url}"
    assert (
        "Sorry, there is a problem with the service" not in source
    ), f"500 ISE → {url}"
    assert "trollface.dk" not in url, f"Faced the troll face!"


@contextmanager
def assertion_msg(message: str, *args):
    """This will:
        * print the custom assertion message
        * print the traceback (stack trace)
        * raise the original AssertionError exception
    """
    try:
        yield
    except AssertionError as e:
        if args:
            message = message % args
        logging.error(message)
        e.args += (message,)
        _, _, tb = sys.exc_info()
        if len(sys._current_frames()) == 1:
            print(f"Found 'shallow' Traceback, will inspect outer traceback frames")
            import inspect

            for f in inspect.getouterframes(sys._getframe(0)):
                print(f"{f.filename} +{f.lineno} - in {f.function}")
                if "_def.py" in f.filename:
                    break
        traceback.print_tb(tb)
        raise


def extract_by_css(
    content: str, selector: str, *, first: bool = True
) -> Union[str, list]:
    """Extract values from HTML content using CSS selector.

    :param content: HTML content
    :param selector: CSS selector
    :param first: (optional) return first found element or all of them
    :return: value of the 1st found element or emtpy string if not found; or a list of all found elements
    """
    from scrapy.selector import Selector

    extracted = Selector(text=content).css(selector).extract()
    if first:
        result = extracted[0] if len(extracted) > 0 else ""
    else:
        result = extracted
    return result
