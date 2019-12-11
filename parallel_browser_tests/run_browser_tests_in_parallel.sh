#!/usr/bin/env bash

PYTHONPATH=. behave --dry-run --no-source --no-summary --no-snippets --tags=~@wip --tags=~@fixme --tags=~@skip --format=mini features/ | grep -v "Supplied path\|Trying base directory" | while IFS=$'\r' read -r line ; do
  python3 behave_celery_task.py --browser="chrome" --scenario="${line}"
  python3 behave_celery_task.py --browser="firefox" --scenario="${line}"
  echo "Added task for scenario: '${line}'"
done

# print stats until there are tests to execute
python3 behave_celery_task.py
