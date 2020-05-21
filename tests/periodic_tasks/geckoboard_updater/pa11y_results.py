# -*- coding: utf-8 -*-
from tests.periodic_tasks.geckoboard_updater.pa11y_helpers import (
    generate_dataset_counters,
    get_tasks_with_last_results,
    parse_task_results,
)

raw_results = get_tasks_with_last_results()
parsed_results = parse_task_results(raw_results)
aggregated_accessibility_issues_per_service = generate_dataset_counters(parsed_results)
