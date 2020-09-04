import json
import os
import sys
import uuid

from assertpy import assert_that

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../rabbitmqbaselibrary')))
from common.report import Report  # noqa: E402


def test_should_create_report() -> None:
    report = Report()
    report.set_context({
        'test': 'this is a test'
    })
    report.append_event('sample record added', {
        'random': str(uuid.uuid4())
    })
    a = json.loads(report.report())
    assert_that(a[0]).contains_key('id')
    assert_that(a[0]).contains_key('random')
    assert_that(a[0]).contains_key('timestamp')
    assert_that(a[0]).contains_entry({'context': {'test': 'this is a test'}})
    assert_that(a[0]).contains_entry({'name': 'sample record added'})
