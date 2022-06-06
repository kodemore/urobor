import re


def string_to_snake_case(string: str) -> str:
    string = re.sub(r"[\W]+", " ", string)  # Remove non-ASCII characters
    string = re.sub(r"[\-\.\s]", "_", str(string))  # Replace space and hyphens
    if not string:
        return string

    return re.sub(
        r"_+",
        "_",
        string[0].lower()
        + re.sub(r"[A-Z]", lambda matched: "_" + matched.group(0).lower(), string[1:]),
    )


def string_to_hyphens(string: str) -> str:
    return re.sub(r"_", "-", string_to_snake_case(string))


def string_strip(string: str) -> str:
    return string.strip()


def string_to_lower(string: str) -> str:
    return string.lower()


def string_to_upper(string: str) -> str:
    return string.upper()


def string_replace(string: str, extra: str = "") -> str:
    params = [item.strip() for item in extra.split(">")]
    if len(params) < 2:
        raise ValueError(f"String replace modifier expects `from > to` format, `{extra}` passed instead.")

    return string.replace(params[0], params[1])

