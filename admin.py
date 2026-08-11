from database import (
    get_all_reports,
    get_report_by_id,
    update_report_status
)


ALLOWED_STATUSES = [
    "Submitted",
    "Under Review",
    "In Progress",
    "Resolved",
    "Rejected"
]


def get_admin_reports():
    """Return all reports for the admin dashboard."""

    reports = get_all_reports()

    return [dict(report) for report in reports]


def get_admin_report(report_id):
    """Return details of a specific report."""

    report = get_report_by_id(report_id)

    if report is None:
        return None

    return dict(report)


def change_report_status(report_id, status):
    """Change the status of a civic report."""

    if status not in ALLOWED_STATUSES:
        return False

    return update_report_status(report_id, status)