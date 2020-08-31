import os
import sys
from unittest.mock import MagicMock

from assertpy import assert_that, fail

from ..common.fixtures import mock_response, mock_bad_response_with_status, fake_broker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../lib')))
from common.exceptions import NotFoundException, BadRequest
from definitions.definitions import get_definitions, load_definitions


def get_definition_example():
    return {
        'queues': [{
            'name': 'test-queue',
            'durable': True,
            'auto_delete': False,
            'arguments': {
                'x-queue-type': 'classic'
            }
        }]
    }


def test_should_get_definitions(mocker: MagicMock) -> None:
    response = mock_response(get_definition_example())
    patch = mocker.patch('requests.get', return_value=response)
    result = get_definitions(broker=fake_broker(), vhost='test')
    assert_that(result).is_equal_to(get_definition_example())
    patch.assert_called_with(url='https://fake-broker/api/definitions/test',
                             auth=('guest', 'guest'))


def test_should_raise_exception_when_get_definitions_but_404(mocker) -> None:
    response = mock_bad_response_with_status(404)
    patch = mocker.patch('requests.get', return_value=response)
    try:
        get_definitions(broker=fake_broker(), vhost='test')
    except NotFoundException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/definitions/test')
    patch.assert_called_with(url='https://fake-broker/api/definitions/test',
                             auth=('guest', 'guest'))


def test_should_load_definitions(mocker) -> None:
    response = mock_response([])
    patch = mocker.patch('requests.post', return_value=response)
    load_definitions(broker=fake_broker(), vhost='test', definitions=get_definition_example())
    patch.assert_called_with(url='https://fake-broker/api/definitions/test',
                             auth=('guest', 'guest'), json=get_definition_example())


def test_should_raise_exception_when_load_definitions_but_400(mocker) -> None:
    response = mock_bad_response_with_status(400)
    patch = mocker.patch('requests.post', return_value=response)
    try:
        load_definitions(broker=fake_broker(), vhost='test', definitions=get_definition_example())
        fail('it should raise exception')
    except BadRequest as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/definitions/test')
    patch.assert_called_with(url='https://fake-broker/api/definitions/test',
                             auth=('guest', 'guest'), json=get_definition_example())
