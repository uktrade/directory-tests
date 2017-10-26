# -*- coding: utf-8 -*-
"""Paver configuration file."""
import multiprocessing
import sys

from paver.easy import sh, task, consume_nargs
from paver.setuputils import setup

setup(
    name="behave-browserstack",
    version="0.1.0",
    author="BrowserStack",
    author_email="support@browserstack.com",
    description="Behave Integration with BrowserStack",
    license="MIT",
    keywords="parallel selenium with browserstack",
    url="https://github.com/browserstack/lettuce-browserstack",
    packages=['features']
)


def run_behave_test(feature: str, task_id: int = 0):
    sh("TASK_ID={} "
       "behave -k --format progress3 --no-logcapture --tags=-wip --tags=-skip "
       "--tags=~fixme features/{}.feature"
       .format(task_id, feature))


@task
@consume_nargs(1)
def run(args):
    """Run single, local and parallel test using different config."""
    jobs = []
    for i in range(6):
        p = multiprocessing.Process(
            target=run_behave_test, args=("home-page", i))
        jobs.append(p)
        p.start()

    exit_codes = []
    for j in jobs:
        j.join()
        exit_codes.append(j.exitcode)
        print('%s.exitcode = %s' % (j.name, j.exitcode))
    sys.exit(sum(exit_codes))


@task
def test():
    """Run all tests"""
    sh("paver run parallel")
