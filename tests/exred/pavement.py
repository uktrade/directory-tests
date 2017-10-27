# -*- coding: utf-8 -*-
"""Paver configuration file."""
import os
import sys
from multiprocessing import Process

from paver.easy import consume_nargs, sh, task
from paver.setuputils import setup

# Append current directory to Paver's class path.
# This is needed to load the local `config` module
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

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


def run_behave_test(config_name: str, task_id: int = 0):
    sh("CONFIG={} TASK_ID={} behave -k --format progress3 --no-logcapture "
       "--tags=-wip --tags=-skip --tags=~fixme".format(config_name, task_id))


@task
@consume_nargs(1)
def run(args):
    """Run single, local and parallel test using different config."""
    jobs = []
    if args[0] == "local":
        run_behave_test(args[0])
    else:
        import config
        browser_num = len(config.get(args[0])["environments"])
        for idx in range(browser_num):
            process = Process(target=run_behave_test, args=(args[0], idx))
            jobs.append(process)
            process.start()

        exit_codes = []
        for job in jobs:
            job.join()
            exit_codes.append(job.exitcode)
            print('%s.exitcode = %s' % (job.name, job.exitcode))
        sys.exit(sum(exit_codes))
