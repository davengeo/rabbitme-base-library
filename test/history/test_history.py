import os
import sys
from unittest.mock import MagicMock, call

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from rabbitmqbaselibrary.history.history import History  # noqa: E402


def test_should_initialise_db(mocker: MagicMock) -> None:
    conn = MagicMock()
    cur = MagicMock()
    conn.cursor.return_value = cur
    cur.fetchone.return_value = None
    patch_sql = mocker.patch('sqlite3.connect', return_value=conn)
    History(hist_path='.', db_name='test')
    patch_sql.assert_called_once()
    conn.cursor.assert_called_once()
    # noinspection SqlResolve
    calls = [call('''SELECT name FROM sqlite_master WHERE type='table' AND name=?''', ('History',)),
             call('''CREATE TABLE History (id INTEGER PRIMARY KEY,  input_file varchar(80) NOT NULL,
                 output_file varchar(80), environment varchar(20), timestamp DATETIME, user varchar(20))''')]
    cur.execute.assert_has_calls(calls=calls, any_order=False)


# def test_should_save_record_db(mocker: MagicMock) -> None:
#     pass
