#!/usr/bin/env bash

PYTHONPATH=. behave \
    --dry-run \
    --no-source \
    --no-summary \
    --no-snippets \
    --tags=~@wip \
    --tags=~@fixme \
    --tags=~@skip \
    --format=mini \
    features/domestic/header_footer.feature \
    | grep -v "Supplied path\|Trying base directory" > scenario_titles.txt

python3 behave_celery_task.py --create-tasks
python3 behave_celery_task.py --monitor
