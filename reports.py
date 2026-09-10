from database import (
    add_report,
    get_all_reports,
    get_report_by_id
)


def create_report(
    user_id,
    title,
    category,
    description,
    latitude=None,
    longitude=None,
    address=None,
    image_filename=None
):
    """
    Create a new civic issue report.
    Returns the report ID if successful.
    """

    if not title or not category or not description:
        return None

    report_id = add_report(
        user_id=user_id,
        title=title,
        category=category,
        description=description,
        latitude=latitude,
        longitude=longitude,
        address=address,
        image_filename=image_filename
    )

    return report_id


def get_reports():
    """Return all civic reports."""

    reports = get_all_reports()

    return [dict(report) for report in reports]


def get_single_report(report_id):
    """Return one civic report by ID."""

    report = get_report_by_id(report_id)

    if report is None:
        return None

    return dict(report)