# -*- coding: utf-8 -*-
"""Paver configuration file."""
import sys
from multiprocessing import Process

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


def run_behave_test(task_id: int = 0, features_dir: str = ""):
    if features_dir:
        features_path = "tests/functional/features/{}/".format(features_dir)
    sh("TASK_ID={} FEATURE_DIR={} behave -k --format progress3 --no-logcapture"
       " --tags=-wip --tags=-skip --tags=~fixme {}".format(
           task_id, features_dir, features_path))


@task
@consume_nargs(1)
def run(args):
    """Run single, local and parallel test using different config."""
    jobs = []
    for index, folder in enumerate(["fab", "fas", "sso", "sud"]):
        p = Process(target=run_behave_test, args=(index, folder))
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
