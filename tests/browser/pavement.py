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
    version="0.1.1",
    author="BrowserStack",
    author_email="support@browserstack.com",
    description="Behave Integration with BrowserStack",
    license="MIT",
    keywords="parallel selenium with browserstack",
    url="https://github.com/browserstack/lettuce-browserstack",
    packages=["features"],
)


def run_behave_test(
    config_name: str,
    task_id: int = 0,
    *,
    browsers: str = "",
    versions: str = "",
    tags: str = None
):
    extra_tags = tags if tags else ""
    sh(
        f"BROWSERS={browsers} VERSIONS={versions} CONFIG={config_name} "
        f"TASK_ID={task_id} behave -k --format progress3 "
        f"--logging-filter=-root --tags=-wip --tags=-skip --tags=-long "
        f"--tags=-fixme {extra_tags}"
    )


@task
@cmdopts(
    [
        make_option(
            "-c",
            "--config",
            help="Configuration name: local, hub, "
            "browsertstack-first-browser-set or "
            "browserstack-second-browser-set",
            default="local",
        ),
        make_option(
            "-t",
            "--tags",
            help="(Optional) Scenario tags for a selective test run",
            default="",
        ),
        make_option(
            "-b",
            "--browsers",
            help="A comma separated list of Browsers to run the tests " "with",
            default="Chrome",
        ),
        make_option(
            "-v",
            "--versions",
            help="A comma separated list of Browsers Versions to run the "
            "tests with",
            default="",
        ),
    ]
)
def run(options):
    """Run single, local and parallel test using different config."""
    jobs = []
    if options.config == "local":
        run_behave_test(
            config_name="local",
            browsers=options.browsers,
            versions=options.versions,
            tags=options.tags,
        )
    else:
        import config

        browser_num = len(config.get(options.config)["environments"])
        for idx in range(browser_num):
            process = Process(
                target=run_behave_test,
                args=(options.config, idx),
                kwargs={
                    "browsers": options.browsers if browser_num == 1 else "",
                    "versions": options.versions,
                    "tags": options.tags,
                },
            )
            jobs.append(process)
            process.start()

        exit_codes = []
        for job in jobs:
            job.join()
            exit_codes.append(job.exitcode)
            print("%s.exitcode = %s" % (job.name, job.exitcode))
        sys.exit(sum(exit_codes))
