from datetime import date

from django.contrib.postgres.fields.ranges import DateRange


def test_default_date_range_returns_django_date_range():
    from simple_locations.models import default_date_range

    result = default_date_range()
    assert isinstance(result, DateRange)
    assert result.lower == date(1975, 9, 16)
    assert result.upper == date(2999, 12, 31)
