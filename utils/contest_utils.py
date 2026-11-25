from datetime import datetime
from zoneinfo import ZoneInfo

BD_TZ = ZoneInfo("Asia/Dhaka")


def calculate_contest_status(contest):
    now = datetime.now(BD_TZ)

    start_at = contest.start_at
    end_at = contest.end_at

    # Handle datetime values without timezone information.
    if start_at.tzinfo is None:
        start_at = start_at.replace(tzinfo=BD_TZ)
    else:
        start_at = start_at.astimezone(BD_TZ)

    if end_at.tzinfo is None:
        end_at = end_at.replace(tzinfo=BD_TZ)
    else:
        end_at = end_at.astimezone(BD_TZ)

    if now < start_at:
        return "upcoming"

    elif now < end_at:
        return "running"

    else:
        return "past"