from repository.csv_repository import parse_date, get_week_range





def test_date_parsing():
    date = "9/5/2023 19:05"
    new_date = parse_date(date)

    date2 = "3/5/2023 19:05"
    new_date = parse_date(date2)

    assert True


def test_get_week_range():
    date = "9/5/2023 19:05"
    week_r = get_week_range((parse_date(date)))
    i = week_r[0]
    assert False

