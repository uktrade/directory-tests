#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Modified version of fetch function with semaphore created by: Paweł Miech
src: https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html
"""
import argparse
import asyncio
import sys
from argparse import Namespace
from asyncio import Semaphore
from typing import List

import async_timeout
from aiohttp import ClientSession

DEFAULT_USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.6.01001)' 


async def fetch(
        url: str, session: ClientSession, user_agent: str, timeout: int,
        verbose: bool):
    user_agent = user_agent or DEFAULT_USER_AGENT
    headers = {
        'User-Agent': user_agent
    }
    try:
        async with async_timeout.timeout(timeout):
            async with session.get(url, headers=headers) as response:
                if verbose:
                    print('{:<75} → {:>3}'.format(url, response.status))
                await response.read()
                return response.status
    except asyncio.TimeoutError:
        if verbose:
            print('{:<75} → timed out'.format(url))
        return 'timedout'


async def bound_fetch(
        sem: Semaphore, url: str, session: ClientSession, responses: dict,
        user_agent: str, timeout: int, verbose: bool):
    """Getter function with semaphore."""
    async with sem:
        status = await fetch(url, session, user_agent, timeout, verbose)
        if url in responses:
            responses[url].append(status)
        else:
            responses[url] = [status]


async def monitor(
        urls: List[str], limit: int, interval: int, responses: dict,
        user_agent: str, timeout: int, verbose: bool):
    tasks = []
    # create instance of Semaphore
    semaphore = Semaphore(1000)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for i in range(limit):
            for url in urls:
                # pass Semaphore and session to every GET request
                task = asyncio.ensure_future(bound_fetch(
                    semaphore, url, session, responses, user_agent, timeout,
                    verbose))
                tasks.append(task)
            if verbose:
                print(
                    'Will wait {} seconds before proceeding with the next '
                    'batch of requests'.format(interval))
            await asyncio.sleep(interval)
        await asyncio.gather(*tasks)


def parse_arguments(argv: List[str]) -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '-u', '--urlsfile', help='Path to a file with URLs to monitor',
            type=str, required=True)
    parser.add_argument(
            '-l', '--limit', help='Limit monitoring to N consequent requests',
            type=int, required=False, default=5)
    parser.add_argument(
            '-i', '--interval', help='Number of seconds between requests',
            type=int, required=False, default=10)
    parser.add_argument(
            '-a', '--user-agent', help='User-Agent header value',
            type=str, required=False, default=DEFAULT_USER_AGENT)
    parser.add_argument(
            '-t', '--timeout', help='Request timeout',
            type=int, required=False, default=15)
    parser.add_argument(
            '-v', '--verbose', help='Print intermediate status codes',
            action='count')
    args = parser.parse_args()
    return args


def clean_lines(lines: List[str]) -> List[str]:
    return [line for line in lines if line or line.startswith('#')]


def parse_urlsfile(path: str) -> List[str]:
    with open(path, 'r') as urls:
        return clean_lines(urls.read().splitlines())


def print_results(results: dict):
    for url, status_codes in results.items():
        non_200 = [status for status in status_codes if status != 200]
        attempts = 'attempts' if len(status_codes) > 1 else 'attempt'
        if non_200:
            times = 'times' if len(non_200) > 1 else 'time'
            print(
                '{:<75} responded with status code other than "200 OK" {} {} '
                'out of {} {}'.format(
                    url, len(non_200), times, len(status_codes), attempts))
            print('Here\'s a list of status codes: {}'.format(status_codes))
        else:
            times = 'times' if len(status_codes) > 1 else 'time'
            print(
                '{:<75} responded with "200 OK" {} {} out of {} {}'
                .format(
                    url, len(status_codes), times, len(status_codes),
                    attempts))


if __name__ == '__main__':
    arguments = parse_arguments(sys.argv[1:])
    urls = parse_urlsfile(arguments.urlsfile)
    limit = arguments.limit
    interval = arguments.interval
    user_agent = arguments.user_agent
    timeout = arguments.timeout
    verbose = arguments.verbose

    print(
        'Will check {} times for status codes from {} URLs every {} seconds.\n'
        'User-Agent: {}\n'
        .format(interval, len(urls), limit, user_agent))
    responses = {}
    loop = asyncio.get_event_loop()
    try:
        future = asyncio.ensure_future(
                monitor(
                    urls, limit, interval, responses, user_agent, timeout,
                    verbose))
        loop.run_until_complete(future)
        print_results(responses)
    finally:
        # see: https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.shutdown_asyncgens
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
