# -*- coding: utf-8 -*-
"""Jira queries for Tools teams project"""
from collections import namedtuple
from enum import Enum
from typing import List

###############################################################################
# Common bits
###############################################################################

# Class for keeping Jira queries & their description
JQL = namedtuple("JQL", ["description", "query"])


def to_jql_list_string(strings: List) -> str:
    """Convert a list of strings into a string of strings.

    String are surrounded by double quotes
    """
    return ",".join(map('"{0}"'.format, strings))


###############################################################################
# Generic JQLs
###############################################################################

_BACKLOG_BUGS = """
PROJECT = {project}
AND issuetype = Bug
AND status = "{backlog_name}"
ORDER BY labels DESC, priority DESC, updated DESC
"""

_BOARD_BUGS = """
PROJECT = {project}
AND issuetype = Bug
AND status != "{backlog_name}"
AND status != Done
ORDER BY labels DESC, priority DESC, updated DESC
"""

_SPRINT_BOARD_TICKETS = """
project = {project}
AND issuetype in (Bug, Spike, Story, Task)
AND status in ({open_statuses})
AND Sprint in openSprints()
ORDER BY key ASC, labels DESC, priority DESC, updated DESC
"""

_KANBAN_BOARD_TICKETS = """
project = {project}
AND issuetype in (Bug, Spike, Story, Task)
AND status in ({open_statuses})
ORDER BY key ASC, labels DESC, priority DESC, updated DESC
"""

_BUGS_MANUAL_VS_AUTOMATED = """
PROJECT = {project}
AND resolution = Unresolved
AND labels in (qa_auto, qa_manual)
ORDER BY priority DESC, updated DESC
"""

_SCENARIOS_TO_AUTOMATE = """
PROJECT = {project}
AND issuetype in (Task, Sub-task)
AND resolution = Unresolved
AND labels = qa_automated_scenario
ORDER BY created DESC
"""

_BUGS_CLOSED_TODAY = """
PROJECT = {project}
AND issuetype = Bug
AND Status CHANGED FROM ({open_statuses})
TO ({closed_statuses})
DURING (-0d, now())
ORDER BY key ASC, updated DESC
"""

_TICKETS_CLOSED_TODAY = """
PROJECT = {project}
AND issuetype != Bug
AND Status CHANGED FROM ({open_statuses})
TO ({closed_statuses})
DURING (-0d, now())
ORDER BY key ASC, updated DESC
"""

###############################################################################
# Tools Team
###############################################################################

TOOLS_OPEN_STATUSES = [
    "Backlog",
    "Planning",
    "Blocked!",
    "Design - to do",
    "Dev - code review",
    "Dev - in progress",
    "In Progress",
    "Release candidate",
    "Selected for Development",
    "Testing",
]
TOOLS_BOARD_OPEN_STATUSES = [
    "Design - to do",
    "Dev - code review",
    "Dev - in progress",
    "In Progress",
    "Release candidate",
    "Selected for Development",
    "Testing",
]
TOOLS_CLOSED_STATUSES = ["Closed", "Done", "Release Candidate", "Release"]


class ToolsJQLs(Enum):

    BUGS_IN_BACKLOG = JQL(
        description="Bugs in backlog",
        query=_BACKLOG_BUGS.format(project="TT", backlog_name="Backlog"),
    )
    BUGS_ON_BOARD = JQL(
        description="Bugs on Kanban board",
        query=_BOARD_BUGS.format(project="TT", backlog_name="Backlog"),
    )
    BUGS_CLOSED_TODAY = JQL(
        description="Bugs closed today",
        query=_BUGS_CLOSED_TODAY.format(
            project="TT",
            open_statuses=to_jql_list_string(TOOLS_OPEN_STATUSES),
            closed_statuses=to_jql_list_string(TOOLS_CLOSED_STATUSES),
        ),
    )
    TICKETS_CLOSED_TODAY = JQL(
        description="Tickets closed today",
        query=_TICKETS_CLOSED_TODAY.format(
            project="TT",
            open_statuses=to_jql_list_string(TOOLS_OPEN_STATUSES),
            closed_statuses=to_jql_list_string(TOOLS_CLOSED_STATUSES),
        ),
    )
    TICKETS_ON_BOARD = JQL(
        description="Tickets (incl. bugs) on Kanban Board",
        query=_KANBAN_BOARD_TICKETS.format(
            project="TT", open_statuses=to_jql_list_string(TOOLS_BOARD_OPEN_STATUSES),
        ),
    )
