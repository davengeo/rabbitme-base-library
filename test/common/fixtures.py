from unittest.mock import MagicMock


def mock_response(obj: object) -> object:
    r = MagicMock()
    r.ok = True
    r.json.return_value = obj
    return r


def mock_bad_response_with_status(status_code: int) -> object:
    r = MagicMock()
    r.ok = False
    r.status_code = status_code
    return r
