from enum import Enum
import importlib
import pkgutil
from collections import namedtuple
from typing import Dict, Union, List

from bs4 import BeautifulSoup
from requests import Session, Response
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from utils import assertion_msg, selenium_action

from types import ModuleType

import pages

REQUIRED_PROPERTIES = ["SERVICE", "NAME", "TYPE", "URL", "SELECTORS"]

Executor = Union[WebDriver, Session]
AssertionExecutor = Union[WebDriver, Response]

Selector = namedtuple(
    "Selector", ["by", "value", "in_desktop", "in_mobile", "in_horizontal"]
)
Selector.__new__.__defaults__ = (None, None, True, True, True)


def get_desktop_selectors(section: dict) -> Dict[str, Selector]:
    return {
        key: selector
        for key, selector in section.items()
        if selector.in_desktop
    }


def get_mobile_selectors(section: dict) -> Dict[str, Selector]:
    return {
        key: selector
        for key, selector in section.items()
        if selector.in_mobile
    }


def get_horizontal_selectors(section: dict) -> Dict[str, Selector]:
    return {
        key: selector
        for key, selector in section.items()
        if selector.in_horizontal
    }


def browser_visit(driver: WebDriver, url: str):
    driver.get(url)


def requests_visit(session: Session, url: str) -> Response:
    return session.get(url)


def visit_url(executor: Executor, url: str) -> Union[Response, None]:
    if isinstance(executor, WebDriver):
        executor.get(url)
    elif isinstance(executor, Session):
        return executor.get(url)
    else:
        raise NotImplementedError(
            "Unsupported type: {}. Please provide one of supported types: "
            "WedDriver or Session".format(type(executor))
        )


def browser_check_for_sections(
    driver: WebDriver,
    all_sections: dict,
    sought_sections: List[str],
    *,
    desktop: bool = True,
    mobile: bool = False,
    horizontal: bool = False
):
    for name in sought_sections:
        if desktop:
            selectors = get_desktop_selectors(all_sections[name.lower()])
        elif mobile:
            selectors = get_mobile_selectors(all_sections[name.lower()])
        elif horizontal:
            selectors = get_horizontal_selectors(all_sections[name.lower()])
        else:
            raise KeyError(
                "Please choose from desktop, mobile or horizontal (mobile) "
                "selectors"
            )
        for key, selector in selectors.items():
            with selenium_action(
                driver,
                "Could not find element: %s identified by '%s' selector",
                key,
                selector.value,
            ):
                element = driver.find_element(
                    by=selector.by, value=selector.value
                )
            with assertion_msg(
                "It looks like '%s' element identified by '%s' selector is"
                " not visible on %s",
                key,
                selector,
                driver.current_url,
            ):
                assert element.is_displayed()


def requests_check_for_sections(
    response: Response, all_sections: dict, sought_sections: List[str]
):
    for name in sought_sections:
        selectors = get_desktop_selectors(all_sections[name.lower()])
        for key, selector in selectors.items():
            soup = BeautifulSoup(response.content, "lxml")
            if selector.by == By.ID:
                element = soup.find_all(id=selector.value)
            else:
                element = soup.find_all(selector.value)
            assert element is not None


def check_for_sections(
    executor: AssertionExecutor, all_sections: dict, sought_sections: List[str]
):
    if isinstance(executor, WebDriver):
        browser_check_for_sections(executor, all_sections, sought_sections)
    elif isinstance(executor, Response):
        requests_check_for_sections(executor, all_sections, sought_sections)
    else:
        raise NotImplementedError(
            "Unsupported type: {}. Please provide one of supported types: "
            "WebDriver or Response".format(type(executor))
        )


def is_page_object(module: ModuleType):
    return all([hasattr(module, prop) for prop in REQUIRED_PROPERTIES])


class PageObjects(Enum):
    """Page Objects enumeration.

    Values can only be modules with properties required for a Page Object.
    """
    def __new__(cls, value):
        if not is_page_object(value):
            raise TypeError(
                "Expected to get a Page Object module but got: {}".format(
                    value
                )
            )
        member = object.__new__(cls)
        member._value_ = value
        return member

    def __str__(self):
        return "{}-{} [{} - {}]".format(
            self.value.SERVICE,
            self.value.NAME,
            self.value.TYPE,
            self.value.URL,
        )

    @property
    def name(self) -> str:
        return self.value.NAME

    @property
    def service(self) -> str:
        return self.value.SERVICE

    @property
    def type(self) -> str:
        return self.value.TYPE

    @property
    def url(self) -> str:
        return self.value.URL

    @property
    def selectors(self) -> Dict:
        return self.value.SELECTORS


def get_page_object_modules(package: ModuleType) -> Dict:
    def get_enum_key(mod: ModuleType) -> str:
        return "{}_{}".format(mod.SERVICE, mod.NAME).upper().replace(" ", "_")

    result = {}
    prefix = package.__name__ + "."
    for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
        if not is_pkg:
            module = importlib.import_module(prefix + module_name)
            if is_page_object(module):
                enum_key = get_enum_key(module)
                result[enum_key] = module

    return result


PAGES = PageObjects("PageObjects", names=get_page_object_modules(pages))
