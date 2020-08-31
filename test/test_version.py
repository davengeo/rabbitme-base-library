import os
import sys

import pytest
from assertpy import assert_that

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from lib import VERSION  # noqa: E402


@pytest.mark.wip
def test_version() -> None:
    assert_that(VERSION).is_equal_to('0.8.0')
