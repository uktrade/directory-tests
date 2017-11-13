# -*- coding: utf-8 -*-
"""Paver configuration file."""
import os
import sys
from multiprocessing import Process
from optparse import make_option

from paver.easy import cmdopts, sh, task
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


def run_behave_test(
        config_name: str, task_id: int = 0, *, browsers: str = "",
        versions: str = "", tag: str = None):
    extra_tag = "--tags={}".format(tag) if tag else ""
    sh("BROWSERS={} VERSIONS={} CONFIG={} TASK_ID={} behave -k --format "
       "progress3 --no-logcapture --tags=-wip --tags=-skip --tags=~fixme {}"
        .format(browsers, versions, config_name, task_id, extra_tag))


@task
@cmdopts([
    make_option('-c', '--config',
                help='Configuration name: local, hub, '
                     'browsertstack-first-browser-set or '
                     'browserstack-second-browser-set',
                default="local"),
    make_option('-t', '--tag',
                help='Scenario tag for a selective test run', default=''),
    make_option('-b', '--browsers',
                help='A comma separated list of Browsers to run the tests '
                     'with',
                default='Chrome'),
    make_option('-v', '--versions',
                help='A comma separated list of Browsers Versions to run the '
                     'tests with',
                default='')
])
def run(options):
    """Run single, local and parallel test using different config."""
    jobs = []
    if options.config == "local":
        run_behave_test(
            config_name="local", tag=options.tag, browsers=options.browsers,
            versions=options.versions
        )
    else:
        import config
        browser_num = len(config.get(options.config)["environments"])
        for idx in range(browser_num):
            process = Process(
                target=run_behave_test,
                args=(options.config, idx),
                kwargs={
                    "tag": options.tag,
                    "browsers": options.browsers,
                    "versions": options.versions
                })
            jobs.append(process)
            process.start()

        exit_codes = []
        for job in jobs:
            job.join()
            exit_codes.append(job.exitcode)
            print('%s.exitcode = %s' % (job.name, job.exitcode))
        sys.exit(sum(exit_codes))
