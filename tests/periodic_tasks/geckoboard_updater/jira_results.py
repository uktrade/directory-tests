# -*- coding: utf-8 -*-
from tests.periodic_tasks.geckoboard_updater.jira_helpers import (
    jira_links,
    tickets_by_labels,
    total_tickets,
)
from tests.periodic_tasks.geckoboard_updater.jira_queries import ContentJQLs, ToolsJQLs

content_bugs_in_backlog_by_labels = tickets_by_labels(
    jql=ContentJQLs.BUGS_IN_BACKLOG,
    ignored_labels=["auto", "manual"],
    team="content",
    metric="Bugs in Backlog by labels",
)
content_bugs_on_board_by_labels = tickets_by_labels(
    jql=ContentJQLs.BUGS_ON_BOARD,
    ignored_labels=["auto", "manual"],
    team="content",
    metric="Bugs on Board by labels",
)
content_bugs_closed_today = total_tickets(
    jql=ContentJQLs.BUGS_CLOSED_TODAY, team="content"
)
content_bugs_in_backlog = total_tickets(jql=ContentJQLs.BUGS_IN_BACKLOG, team="content")
content_tickets_closed_today = total_tickets(
    jql=ContentJQLs.TICKETS_CLOSED_TODAY, team="content"
)
content_tickets_on_board = total_tickets(
    jql=ContentJQLs.TICKETS_ON_BOARD, team="content"
)
content_jira_links = jira_links(ContentJQLs)


tools_bugs_in_backlog_by_labels = tickets_by_labels(
    jql=ToolsJQLs.BUGS_IN_BACKLOG,
    ignored_labels=["auto", "manual"],
    team="tools",
    metric="Bugs in Backlog by labels",
)
tools_bugs_on_board_by_labels = tickets_by_labels(
    jql=ToolsJQLs.BUGS_ON_BOARD,
    ignored_labels=["auto", "manual"],
    team="tools",
    metric="Bugs on Board by labels",
)
tools_bugs_closed_today = total_tickets(jql=ToolsJQLs.BUGS_CLOSED_TODAY, team="tools")
tools_bugs_in_backlog = total_tickets(jql=ToolsJQLs.BUGS_IN_BACKLOG, team="tools")
tools_tickets_closed_today = total_tickets(
    jql=ToolsJQLs.TICKETS_CLOSED_TODAY, team="tools"
)
tools_tickets_on_board = total_tickets(jql=ToolsJQLs.TICKETS_ON_BOARD, team="tools")
tools_jira_links = jira_links(ToolsJQLs)


jira_bugs_by_labels = (
    content_bugs_in_backlog_by_labels
    + content_bugs_on_board_by_labels
    + tools_bugs_in_backlog_by_labels
    + tools_bugs_on_board_by_labels
)

jira_bug_and_ticket_counters = (
    content_bugs_closed_today
    + content_bugs_in_backlog
    + content_tickets_closed_today
    + content_tickets_on_board
    + tools_bugs_closed_today
    + tools_bugs_in_backlog
    + tools_tickets_closed_today
    + tools_tickets_on_board
)
