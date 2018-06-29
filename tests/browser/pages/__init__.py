from collections import namedtuple
from typing import Dict, Union, List

from bs4 import BeautifulSoup
from requests import Session, Response
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from utils import assertion_msg, selenium_action

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
        response: Response, all_sections: dict, sought_sections: List[str]):
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
        executor: AssertionExecutor, all_sections: dict,
        sought_sections: List[str]):
    if isinstance(executor, WebDriver):
        browser_check_for_sections(executor, all_sections, sought_sections)
    elif isinstance(executor, Response):
        requests_check_for_sections(executor, all_sections, sought_sections)
    else:
        raise NotImplementedError(
            "Unsupported type: {}. Please provide one of supported types: "
            "WebDriver or Response".format(type(executor))
        )

