# -*- coding: utf-8 -*-
"""Project configuration module."""
import json


def load_template(config_file: str) -> str:
    with open("config/{}.json".format(config_file)) as file:
        return file.read()


def render(
        template: str, hub_url: str, capabilities: dict, browsers: list,
        build_id: str) -> str:
    # wrap values in double quotes so that they render correct JSON file
    hub_url = '"{}"'.format(hub_url) if hub_url else "null"

    if capabilities:
        capabilities = json.dumps(capabilities)
    else:
        capabilities = {}

    if browsers:
        browsers = ['"{}"'.format(browser) for browser in browsers]
    else:
        browsers = ['"Chrome"', '"Firefox"', '"PhantomJS"']

    build_id = '"{}"'.format(build_id) if build_id else '""'

    return template.format(
        HUB_URL=hub_url, CAPABILITIES=capabilities, BROWSERS=browsers,
        BUILD_ID=build_id)


def get(
        config_file: str, *, hub_url: str = None, capabilities: dict = None,
        browsers: list = None, build_id: str = None) -> dict:
    config_template = load_template(config_file)
    rendered = render(
        config_template, hub_url=hub_url, capabilities=capabilities,
        browsers=browsers, build_id=build_id)
    return json.loads(rendered)
