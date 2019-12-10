#!/usr/bin/env bash

if [[ -z ${FEATURE_DIR} ]];
then
    echo "FEATURE_DIR env var is unset. e.g. FEATURE_DIR=sso ./run_tests.sh";
    exit 1;
fi

PYTHONPATH=. behave --dry-run --no-source --no-summary --no-snippets --tags=~@wip --tags=~@fixme --tags=~@skip --format=mini features/${FEATURE_DIR} | grep -v "Supplied path\|Trying base directory" | while IFS=$'\r' read -r line ; do
  python3 behave_celery_task.py "chrome" "${line}"
  python3 behave_celery_task.py "firefox" "${line}"
  echo "Added task for scenario: '${line}'"
done

#docker-compose exec pbt_worker sh -c "PYTHONPATH=. behave --dry-run --no-source --no-summary --no-snippets --tags=~@wip --tags=~@fixme --tags=~@skip --format=mini features/${FEATURE_DIR}" | grep -v "Supplied path\|Trying base directory" | while IFS=$'\r' read -r line ; do
#  docker-compose exec -d pbt_worker python3 behave_celery_task.py "chrome" "${line}"
#  docker-compose exec -d pbt_worker python3 behave_celery_task.py "firefox" "${line}"
#  echo "Added task for scenario: '${line}'"
#done
