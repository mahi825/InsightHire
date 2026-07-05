"""
risk.py

Estimates whether a candidate has a stable career or is likely to switch
jobs frequently, using a Career Volatility Index (CVI) built from:
  1. Number of job switches
  2. Average job duration
  3. Experience ratio
  4. A combined rule-based risk score

Expected job_history format (list of dicts), one dict per job:

    job_history = [
        {
            "company": "Infosys",
            "start_date": "2015-06-01",
            "end_date": "2017-08-01"
        },
        {
            "company": "TCS",
            "start_date": "2017-09-01",
            "end_date": "2019-01-15"
        },
        {
            "company": "Google",
            "start_date": "2019-02-01",
            "end_date": None          # None / missing / "present" = current job
        }
    ]

Dates can be given as "YYYY-MM-DD" strings or as datetime.date/datetime.datetime
objects. An end_date of None (or the string "present") is treated as today.
"""

from datetime import datetime, date


def _parse_date(value):
    """
    Internal helper: convert a date value (string, date, or datetime)
    into a datetime object. Returns today's date if value represents
    an ongoing/current job (None, "", or "present").
    """
    if value is None:
        return datetime.today()

    if isinstance(value, datetime):
        return value

    if isinstance(value, date):
        return datetime(value.year, value.month, value.day)

    if isinstance(value, str):
        cleaned = value.strip().lower()
        if cleaned == "" or cleaned == "present" or cleaned == "current":
            return datetime.today()
        # Try common date formats
        for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(value.strip(), fmt)
            except ValueError:
                continue
        # If nothing matched, fall back to today rather than crashing
        return datetime.today()

    return datetime.today()


def _job_duration_years(job):
    """
    Internal helper: duration of a single job in years (float).
    """
    start = _parse_date(job.get("start_date"))
    end = _parse_date(job.get("end_date"))

    days = (end - start).days
    if days < 0:
        days = 0

    return days / 365.25


def calculate_job_switches(job_history):
    """
    Count how many times a candidate has switched jobs.

    Parameters
    ----------
    job_history : list of dict
        Each dict represents one job.

    Returns
    -------
    int
        Number of switches (jobs - 1). Returns 0 if there are 0 or 1 jobs.
    """
    if not job_history:
        return 0

    switches = len(job_history) - 1
    return max(0, switches)


def average_job_duration(job_history):
    """
    Calculate the average duration (in years) the candidate stayed
    at each job.

    Parameters
    ----------
    job_history : list of dict

    Returns
    -------
    float
        Average job duration in years, rounded to 2 decimal places.
        Returns 0.0 if job_history is empty.
    """
    if not job_history:
        return 0.0

    durations = [_job_duration_years(job) for job in job_history]
    avg_duration = sum(durations) / len(durations)

    return round(avg_duration, 2)


def experience_ratio(avg_duration, total_experience):
    """
    Calculate the ratio of average job duration to total experience.
    A higher ratio means the candidate tends to stay longer per job.

    Parameters
    ----------
    avg_duration : float
        Average duration per job (years).
    total_experience : float
        Candidate's total years of experience.

    Returns
    -------
    float
        Ratio between 0 and 1, rounded to 2 decimal places.
        Returns 0.0 if total_experience is 0 to avoid division by zero.
    """
    if not total_experience or total_experience <= 0:
        return 0.0

    ratio = avg_duration / total_experience
    ratio = max(0.0, min(1.0, ratio))

    return round(ratio, 2)


def calculate_risk_score(switches, avg_duration, ratio):
    """
    Combine switches, average duration, and experience ratio into a
    single rule-based risk score (0-100). Higher = more likely to
    switch jobs / less stable.

    Rules
    -----
    - switches > 5              -> +40
    - avg_duration < 1 year      -> +30
    - ratio < 0.2                -> +30

    Parameters
    ----------
    switches : int
    avg_duration : float
    ratio : float

    Returns
    -------
    int
        Risk score between 0 and 100.
    """
    risk_score = 0

    if switches > 5:
        risk_score += 40

    if avg_duration < 1:
        risk_score += 30

    if ratio < 0.2:
        risk_score += 30

    return min(100, risk_score)
