


def safe_int(value, default=0):
    try:
        return int(value) if value.strip() else default
    except ValueError:
        return default