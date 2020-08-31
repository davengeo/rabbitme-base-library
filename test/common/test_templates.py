import os

from assertpy import assert_that, fail

from common.exceptions import TemplateException
from common.templates import Template

template: Template = Template(basename=os.path.abspath(os.path.join(os.path.dirname(__file__), '../resources')))


def test_should_load_existing_policy() -> None:
    result: dict = template.load_template('policies/dead-letter-policy')
    assert_that(result).is_equal_to(
        {'apply-to': 'all', 'definition': {'dead-letter-exchange': 'exchange'}, 'pattern': '.*', 'priority': 0})


def test_should_raise_exception_when_not_found_template() -> None:
    try:
        template.load_template('policies/non-existing-policy')
        fail('it should raise exception')
    except FileNotFoundError as e:
        assert_that(e.filename).contains('policies/non-existing-policy.json')


def test_should_raise_exception_when_bad_template() -> None:
    try:
        template.load_template('policies/example')
        fail('it should raise exception')
    except TemplateException as e:
        assert_that(e.message).contains('exception in template policies/example')


def test_should_load_existing_template_and_fill_params() -> None:
    obj = template.load_template_with_args('policies/example', {'field': 'a', 'value': 'b'})
    assert_that(obj).is_equal_to({'a': 'b'})


def test_should_raise_exception_when_not_found_template_with_args() -> None:
    try:
        template.load_template_with_args('policies/non-existing-policy', {'no': 'a', 'on': 'b'})
        fail('it should raise exception')
    except FileNotFoundError as e:
        assert_that(e.filename).contains('policies/non-existing-policy.json')


def test_should_raise_exception_when_load_existing_template_but_bad_params() -> None:
    try:
        template.load_template_with_args('policies/example', {'no': 'a', 'on': 'b'})
        fail('it should raise exception')
    except TemplateException as e:
        assert_that(e.message).is_equal_to('exception in template policies/example')
