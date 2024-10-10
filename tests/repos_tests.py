import pytest

from repository.repository import get_all_crashes, get_all_daily_crashes, get_all_weekly_crashes, \
    get_all_monthly_crashes, get_all_areas, get_all_injuries_by_area, get_all_crash_causes




def test_get_all_crashes():
    res = get_all_crashes()
    assert len(res) > 0

def test_get_all_daily_crashes():
    res = get_all_daily_crashes()
    assert len(res) >= 0

def test_get_all_weekly_crashes():
    res = get_all_weekly_crashes()
    assert len(res) >= 0

def test_get_all_monthly_crashes():
    res = get_all_monthly_crashes()
    assert len(res) >= 0

def test_get_all_areas():
    res = get_all_areas()
    assert len(res) >= 0

def test_get_all_injuries_by_area():
    res = get_all_injuries_by_area()
    assert len(res) >= 0

def test_get_all_crash_causes():
    res = get_all_crash_causes()
    assert len(res) >= 0