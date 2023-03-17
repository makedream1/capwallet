import base64


def encode(string) -> str:
    string_bytes = string.encode("ascii")

    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii")

    return base64_string


def decode(encoded_string) -> str:
    base64_bytes = encoded_string.encode("ascii")

    try:
        string_bytes = base64.b64decode(base64_bytes)
        encoded_string = string_bytes.decode("ascii")

    except Exception:
        return False

    return encoded_string
