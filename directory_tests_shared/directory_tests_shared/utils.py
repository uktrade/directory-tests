# -*- coding: utf-8 -*-
import logging
import operator
import sys
import traceback
import uuid
from contextlib import contextmanager
from difflib import SequenceMatcher
from enum import Enum
from random import choice, randint
from types import BuiltinFunctionType
from typing import List, Tuple, Union
from urllib.parse import urlsplit

from scrapy.selector import Selector as ScrapySelector
from termcolor import cprint

import parse
from .constants import (
    OPERATING_COUNTRIES,
    POPULAR_ENGLISH_WORDS,
    PRODUCT_CATEGORIES,
    SECTORS,
)
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
    min_word_length: int = 5,
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
        word = choice(POPULAR_ENGLISH_WORDS)
        if len(word) > min_word_length:
            words.append(word)
    while 0 < max_length < len(" ".join(words)):
        words.pop()
    return " ".join(words)


def rare_word(*, min_length: int = 5, max_length: int = 20):
    """Get a random rare english word.

    NOTE:
    min_length is set to 9, because all words in RARE_WORDS are at least 9
    characters long

    :return: a rare english word
    """
    assert min_length < max_length
    longest_word = sorted(POPULAR_ENGLISH_WORDS, key=lambda x: len(x))[-1]
    assert min_length <= len(longest_word)
    word = ""
    while min_length >= len(word) <= max_length:
        word = choice(POPULAR_ENGLISH_WORDS)
    return word


def random_company_number() -> str:
    return str(randint(0, 9999999)).zfill(8)


def random_sector() -> str:
    return choice(SECTORS)


def random_product_categories() -> str:
    return choice(PRODUCT_CATEGORIES)


def random_operating_countries() -> str:
    return choice(OPERATING_COUNTRIES)


def access_was_denied(source: str) -> bool:
    network_errors = ["Unfortunately your IP address", "If you require access"]
    return all(msg in source for msg in network_errors)


def check_if_access_denied(
    source: str, url: str, *, error_msg: str = "Access denied (on error check) → {url}"
):
    network_errors = ["Unfortunately your IP address", "If you require access"]
    with assertion_msg(error_msg.format(url=url)):
        assert all(msg not in source for msg in network_errors)


def check_for_errors(source: str, url: str):
    check_if_access_denied(source, url)
    with assertion_msg(f"404 Not Found → {url}"):
        assert "404 Not Found" not in source
        assert "This page cannot be found" not in source
    with assertion_msg(f"503 Service Unavailable → {url}"):
        assert "503 Service Unavailable" not in source
    with assertion_msg(f"502 Bad Gateway → {url}"):
        assert "502 Bad Gateway" not in source
    with assertion_msg(f"500 ISE → {url}"):
        assert "Internal Server Error" not in source
    with assertion_msg(f"500 ISE → {url}"):
        assert "there is a problem with the service" not in source
    with assertion_msg(f"Faced the troll face!"):
        assert "trollface.dk" not in url


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


def extract_attributes_by_css(
    content: str, selector: str, *, attrs: List[str] = None, text: bool = True
) -> List[dict]:
    """Extract attributes of matching html elements.

    If element has no matching attribute then it's value will default to None

    :param content: HTML page content
    :param selector: a CSS selector
    :param attrs: (optional) a list of attributes to extract
    :param text: (optional) extract element's text (defaults to True)
    :return: a list of dictionaries with matching attribute values
    """
    results = []
    elements = ScrapySelector(text=content).css(selector)
    for element in elements:
        element_details = {}
        if attrs:
            for attribute in attrs:
                element_details[attribute] = element.attrib.get(attribute, None)

        if text:
            parts = [part for part in element.css("*::text").getall() if part.strip()]
            element_details["text"] = parts[0] if parts else None

        if element_details:
            results.append(element_details)

    return results


def extract_by_css(
    content: str, selector: str, *, first: bool = True
) -> Union[str, list]:
    """Extract values from HTML content using CSS selector.

    :param content: HTML content
    :param selector: CSS selector
    :param first: (optional) return first found element or all of them
    :return: value of the 1st found element or emtpy string if not found; or a list of all found elements
    """
    extracted = ScrapySelector(text=content).css(selector).extract()
    if first:
        result = extracted[0] if len(extracted) > 0 else ""
    else:
        result = extracted
    return result


def get_operator_from_operation(comparison_function):
    """Get arithmetic representation of a comparison function"""
    return {
        operator.lt: "<",
        operator.le: "<=",
        operator.eq: "==",
        operator.ne: "!=",
        operator.ge: ">=",
        operator.gt: ">",
    }[comparison_function]


def evaluate_comparison(
    value_name: str, value_to_compare: int, comparison: Tuple[BuiltinFunctionType, int]
):
    """Will evaluate comparison operator on value_to_compare & compared_value"""
    comparison_operation = comparison[0]
    compared_value = comparison[1]
    operator_function = get_operator_from_operation(comparison_operation)
    error = (
        f"Expected {value_name} {operator_function} {compared_value} but got "
        f"{value_to_compare} instead"
    )
    with assertion_msg(error):
        assert comparison_operation(value_to_compare, compared_value)


def get_comparison_details(description: str) -> Tuple[BuiltinFunctionType, int]:
    """Get comparison function & value from its text description"""
    last_word = description.split()[-1]
    number = -1
    if last_word.isnumeric():
        number = int(last_word)

    parsed = {
        "less than": (operator.lt, number),
        "less or equal to": (operator.le, number),
        "exactly": (operator.eq, number),
        "no": (operator.eq, 0),
        "anything but": (operator.ne, 0),
        "at least": (operator.ge, number),
        "more than": (operator.gt, number),
    }
    matching_comparison_details = [
        parsed[key] for key in parsed.keys() if key in description
    ]
    error = (
        f"Expected to find only 1 matching comparison for: '{description}' but found "
        f"{len(matching_comparison_details)} instead: {matching_comparison_details}"
    )
    assert len(matching_comparison_details) == 1, error
    return matching_comparison_details[0]


class ANSIIColor(Enum):
    """ANSII text color codes
    see: https://en.wikipedia.org/wiki/ANSI_escape_code
    """

    BLACK = "30"
    DARK_RED = "31"
    DARK_GREEN = "32"
    RED = "33"
    DARK_BLUE = "34"
    PURPLE = "35"
    BLUE = "36"
    GRAY = "37"
    BRIGHT_BLACK = "1;30"
    BRIGHT_RED = "1;31"
    BRIGHT_GREEN = "1;32"
    BRIGHT_YELLOW = "1;33"
    BRIGHT_BLUE = "1;34"
    BRIGHT_PURPLE = "1;35"
    BRIGHT_CYAN = "1;36"
    BRIGHT_GRAY = "1;37"


class ANSIIStyle:
    """Generate ANSII text style & color escape start & end codes
    see: https://en.wikipedia.org/wiki/ANSI_escape_code
    """

    start = ""
    end = ""

    def __init__(
        self,
        *,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        strikethrough: bool = False,
        color: ANSIIColor = None,
    ):
        tmp = []
        if bold:
            tmp.append("1")
        if italic:
            tmp.append("3")
        if underline:
            tmp.append("4")
        if strikethrough:
            tmp.append("9")
        if color:
            tmp.append(color.value)
        if tmp:
            self.start = f"\033[{';'.join(tmp)}m"
            self.end = "\033[0m"


def red(x: str):
    """Print out a message in red to console."""
    cprint(x, "red", attrs=["bold"])


def green(x: str):
    """Print out a message in green to console."""
    cprint(x, "green", attrs=["bold"])


def blue(x: str):
    """Print out a message in blue to console."""
    cprint(x, "blue", attrs=["bold"])


def format_matching_parts(
    string_a: str,
    string_b: str,
    *,
    invert: bool = False,
    style: ANSIIStyle = ANSIIStyle(),
) -> Tuple[str, str]:
    """Format matching parts of both strings in desired style & color"""
    if invert:
        start = ""
        end = ""
        invert_start = style.start
        invert_end = style.end
    else:
        start = style.start
        end = style.end
        invert_start = ""
        invert_end = ""

    string_a_matches = ""
    string_b_matches = ""
    blocks = SequenceMatcher(isjunk=None, a=string_a, b=string_b).get_matching_blocks()
    for idx, block in enumerate(blocks):
        if idx == 0 and block.a != 0:
            string_a_matches += f"{invert_start}{string_a[:block.a]}{invert_end}"
            string_b_matches += f"{invert_start}{string_b[:block.b]}{invert_end}"
        string_a_matches += f"{start}{string_a[block.a:(block.a + block.size)]}{end}"
        string_b_matches += f"{start}{string_b[block.b:(block.b + block.size)]}{end}"
        if idx + 1 < len(blocks):
            string_a_matches += f"{invert_start}{string_a[(block.a + block.size):blocks[idx + 1].a]}{invert_end}"
            string_b_matches += f"{invert_start}{string_b[(block.b + block.size):blocks[idx + 1].b]}{invert_end}"
    return string_a_matches, string_b_matches


def check_url_path_matches_template(template: str, url_or_path: str):
    """Check if given URL matches expected URL path or URL template.

    Possible checks:
        url url -> url
        url path -> path
        path url -> path
        path path -> path
    """
    parser = parse.compile(template)

    if template.startswith("http") and url_or_path.startswith("http"):
        result = parser.parse(url_or_path)
        template_matches, url_matches = format_matching_parts(template, url_or_path)
        error = f"Provided URL: {url_matches} does not match: {template_matches}"
        success = f"Provided URL: {url_or_path} matches URL template: {template}"
    else:
        path = urlsplit(url_or_path).path

        # ensure that both template and checked string start in the same way
        if path.startswith("/"):
            path = path[1:]
        if template.startswith("/"):
            template = template[1:]

        result = parser.parse(path)
        template_matches, path_matches = format_matching_parts(template, path)
        error = (
            f"Path '{path_matches}' of provided URL: {url_or_path} does not match: "
            f"{template_matches}"
        )
        success = f"Path part {path} of {url_or_path} matches template: {template}"

    with assertion_msg(error):
        assert result
        logging.debug(success)
