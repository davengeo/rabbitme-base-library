import os
import sys
from typing import List
from unittest.mock import MagicMock

from assertpy import assert_that
from pyramda import map

from ..common.fixtures import mock_response, fake_broker, mock_bad_response_with_status

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../rabbitmqbaselibrary')))
from common.exceptions import NotFoundException, Unauthorised, ServerErrorException, BadRequest  # noqa: E402
from bindings.bindings import get_bindings, get_bindings_from_source, create_binding, Binding, \
    delete_binding  # noqa: E402


def test_should_get_existing_bindings(mocker: MagicMock) -> None:
    bindings = [{'source': 'one-s', 'destination': 'one-d',
                 'routing_key': 'one-r', 'destination_type': 'queue', 'arguments': None},
                {'source': 'two-s', 'destination': 'two-d',
                 'routing_key': 'two-r', 'destination_type': 'exchange', 'arguments': None}]
    response = mock_response(bindings)
    patch = mocker.patch('requests.get', return_value=response)
    result = map(lambda i: i.to_dict(), get_bindings(broker=fake_broker(), vhost='EA'))
    assert_that(result).is_equal_to(bindings)
    patch.assert_called_with(url='https://fake-broker/api/bindings/EA', auth=('guest', 'guest'))


def test_should_return_empty_list_when_get_bindings_but_no_bindings(mocker: MagicMock) -> None:
    bindings: List[dict] = []
    response = mock_response(bindings)
    patch = mocker.patch('requests.get', return_value=response)
    result = map(lambda i: i.to_dict(), get_bindings(broker=fake_broker(), vhost='EA'))
    assert_that(result).is_equal_to([])
    patch.assert_called_with(url='https://fake-broker/api/bindings/EA', auth=('guest', 'guest'))


def test_should_raise_exception_when_get_bindings_but_404(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(404)
    patch = mocker.patch('requests.get', return_value=response)
    try:
        get_bindings(broker=fake_broker(), vhost='EA')
    except NotFoundException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/bindings/EA')
    patch.assert_called_with(url='https://fake-broker/api/bindings/EA', auth=('guest', 'guest'))


def test_should_raise_exception_when_get_bindings_but_401(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(401)
    patch = mocker.patch('requests.get', return_value=response)
    try:
        get_bindings(broker=fake_broker(), vhost='EA')
    except Unauthorised as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/bindings/EA')
    patch.assert_called_with(url='https://fake-broker/api/bindings/EA', auth=('guest', 'guest'))


def test_should_raise_exception_when_get_bindings_but_500(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(500)
    patch = mocker.patch('requests.get', return_value=response)
    try:
        get_bindings(broker=fake_broker(), vhost='EA')
    except ServerErrorException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/bindings/EA')
    patch.assert_called_with(url='https://fake-broker/api/bindings/EA', auth=('guest', 'guest'))


def test_should_raise_exception_when_get_bindings_but_teapot(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(418)
    patch = mocker.patch('requests.get', return_value=response)
    try:
        get_bindings(broker=fake_broker(), vhost='EA')
    except Exception as e:
        assert_that(e.args[0]).is_equal_to(418)
    patch.assert_called_with(url='https://fake-broker/api/bindings/EA', auth=('guest', 'guest'))


def test_should_return_get_bindings_from_source(mocker: MagicMock) -> None:
    bindings = [{'source': 'one-s', 'destination': 'one-d',
                 'routing_key': 'one-r', 'destination_type': 'queue', 'arguments': None},
                {'source': 'two-s', 'destination': 'two-d',
                 'routing_key': 'two-r', 'destination_type': 'exchange', 'arguments': None}]
    response = mock_response(bindings)
    patch = mocker.patch('requests.get', return_value=response)
    result = map(lambda i: i.to_dict(), get_bindings_from_source(broker=fake_broker(), vhost='EA', source='test'))
    assert_that(result).is_equal_to(bindings)
    patch.assert_called_with(url='https://fake-broker/api/exchanges/EA/test/bindings/source', auth=('guest', 'guest'))


def test_should_return_empty_list_when_get_bindings_from_source_but_none(mocker: MagicMock) -> None:
    bindings: List[dict] = []
    response = mock_response(bindings)
    patch = mocker.patch('requests.get', return_value=response)
    result = map(lambda i: i.to_dict(), get_bindings_from_source(broker=fake_broker(), vhost='EA', source='test'))
    assert_that(result).is_empty()
    patch.assert_called_with(url='https://fake-broker/api/exchanges/EA/test/bindings/source', auth=('guest', 'guest'))


def test_should_raise_exception_when_get_bindings_from_source_but_404(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(404)
    patch = mocker.patch('requests.get', return_value=response)
    try:
        get_bindings_from_source(broker=fake_broker(), vhost='EA', source='test')
    except NotFoundException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/exchanges/EA/test/bindings/source')
    patch.assert_called_with(url='https://fake-broker/api/exchanges/EA/test/bindings/source', auth=('guest', 'guest'))


def test_should_raise_exception_when_get_bindings_from_source_but_401(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(401)
    patch = mocker.patch('requests.get', return_value=response)
    try:
        get_bindings_from_source(broker=fake_broker(), vhost='EA', source='test')
    except Unauthorised as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/exchanges/EA/test/bindings/source')
    patch.assert_called_with(url='https://fake-broker/api/exchanges/EA/test/bindings/source', auth=('guest', 'guest'))


def test_should_raise_exception_when_get_bindings_from_source_but_500(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(500)
    patch = mocker.patch('requests.get', return_value=response)
    try:
        get_bindings_from_source(broker=fake_broker(), vhost='EA', source='test')
    except ServerErrorException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/exchanges/EA/test/bindings/source')
    patch.assert_called_with(url='https://fake-broker/api/exchanges/EA/test/bindings/source', auth=('guest', 'guest'))


def test_should_raise_exception_when_get_bindings_from_source_but_teapot(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(418)
    patch = mocker.patch('requests.get', return_value=response)
    try:
        get_bindings_from_source(broker=fake_broker(), vhost='EA', source='test')
    except Exception as e:
        assert_that(e.args[0]).is_equal_to(418)
    patch.assert_called_with(url='https://fake-broker/api/exchanges/EA/test/bindings/source', auth=('guest', 'guest'))


def test_should_create_bindings(mocker: MagicMock) -> None:
    response = mock_response([])
    patch = mocker.patch('requests.post', return_value=response)
    binding = {'source': 'one-s', 'destination': 'one-d',
               'routing_key': 'one-r', 'destination_type': 'queue', 'arguments': None}
    create_binding(broker=fake_broker(), vhost='EA', binding=Binding(binding))
    patch.assert_called_with(url='https://fake-broker/api/bindings/EA/e/one-s/q/one-d',
                             auth=('guest', 'guest'), json={'routing_key': 'one-r', 'arguments': None})


def test_should_raise_exception_when_create_bindings_but_404(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(404)
    patch = mocker.patch('requests.post', return_value=response)
    binding = {'source': 'one-s', 'destination': 'one-d',
               'routing_key': 'one-r', 'destination_type': 'queue', 'arguments': None}
    try:
        create_binding(broker=fake_broker(), vhost='EA', binding=Binding(binding))
    except NotFoundException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/bindings/EA/e/one-s/q/one-d')
    patch.assert_called_with(url='https://fake-broker/api/bindings/EA/e/one-s/q/one-d',
                             auth=('guest', 'guest'), json={'routing_key': 'one-r', 'arguments': None})


def test_should_raise_exception_when_create_bindings_but_401(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(401)
    patch = mocker.patch('requests.post', return_value=response)
    binding = {'source': 'one-s', 'destination': 'one-d',
               'routing_key': 'one-r', 'destination_type': 'queue', 'arguments': None}
    try:
        create_binding(broker=fake_broker(), vhost='EA', binding=Binding(binding))
    except Unauthorised as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/bindings/EA/e/one-s/q/one-d')
    patch.assert_called_with(url='https://fake-broker/api/bindings/EA/e/one-s/q/one-d',
                             auth=('guest', 'guest'), json={'routing_key': 'one-r', 'arguments': None})


def test_should_raise_exception_when_create_bindings_but_400(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(400)
    patch = mocker.patch('requests.post', return_value=response)
    binding = {'source': 'one-s', 'destination': 'one-d',
               'routing_key': 'one-r', 'destination_type': 'queue', 'arguments': None}
    try:
        create_binding(broker=fake_broker(), vhost='EA', binding=Binding(binding))
    except BadRequest as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/bindings/EA/e/one-s/q/one-d')
        assert_that(e.body).is_equal_to({'routing_key': 'one-r', 'arguments': None})
    patch.assert_called_with(url='https://fake-broker/api/bindings/EA/e/one-s/q/one-d',
                             auth=('guest', 'guest'), json={'routing_key': 'one-r', 'arguments': None})


def test_should_raise_exception_when_create_bindings_but_500(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(500)
    patch = mocker.patch('requests.post', return_value=response)
    binding = {'source': 'one-s', 'destination': 'one-d',
               'routing_key': 'one-r', 'destination_type': 'queue', 'arguments': None}
    try:
        create_binding(broker=fake_broker(), vhost='EA', binding=Binding(binding))
    except ServerErrorException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/bindings/EA/e/one-s/q/one-d')
    patch.assert_called_with(url='https://fake-broker/api/bindings/EA/e/one-s/q/one-d',
                             auth=('guest', 'guest'), json={'routing_key': 'one-r', 'arguments': None})


def test_should_raise_exception_when_create_bindings_but_teapot(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(418)
    patch = mocker.patch('requests.post', return_value=response)
    binding = {'source': 'one-s', 'destination': 'one-d',
               'routing_key': 'one-r', 'destination_type': 'queue', 'arguments': None}
    try:
        create_binding(broker=fake_broker(), vhost='EA', binding=Binding(binding))
    except Exception as e:
        assert_that(e.args[0]).is_equal_to(418)
    patch.assert_called_with(url='https://fake-broker/api/bindings/EA/e/one-s/q/one-d',
                             auth=('guest', 'guest'), json={'routing_key': 'one-r', 'arguments': None})


def test_should_delete_bindings(mocker: MagicMock) -> None:
    response = mock_response([])
    patch = mocker.patch('requests.delete', return_value=response)
    binding = {'source': 'one-s', 'destination': 'one-d',
               'routing_key': 'one-r', 'destination_type': 'queue',
               'arguments': None, 'properties_key': '~'}
    delete_binding(broker=fake_broker(), vhost='EA', binding=Binding(binding))
    patch.assert_called_with(url='https://fake-broker/api/bindings/EA/e/one-s/q/one-d/~',
                             auth=('guest', 'guest'))


def test_should_raise_exception_when_delete_bindings_but_404(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(404)
    patch = mocker.patch('requests.delete', return_value=response)
    binding = {'source': 'one-s', 'destination': 'one-d',
               'routing_key': 'one-r', 'destination_type': 'queue',
               'arguments': None, 'properties_key': '~'}
    try:
        delete_binding(broker=fake_broker(), vhost='EA', binding=Binding(binding))
    except NotFoundException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/bindings/EA/e/one-s/q/one-d/~')
    patch.assert_called_with(url='https://fake-broker/api/bindings/EA/e/one-s/q/one-d/~',
                             auth=('guest', 'guest'))


def test_should_raise_exception_when_delete_bindings_but_401(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(401)
    patch = mocker.patch('requests.delete', return_value=response)
    binding = {'source': 'one-s', 'destination': 'one-d',
               'routing_key': 'one-r', 'destination_type': 'queue',
               'arguments': None, 'properties_key': '~'}
    try:
        delete_binding(broker=fake_broker(), vhost='EA', binding=Binding(binding))
    except Unauthorised as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/bindings/EA/e/one-s/q/one-d/~')
    patch.assert_called_with(url='https://fake-broker/api/bindings/EA/e/one-s/q/one-d/~',
                             auth=('guest', 'guest'))


def test_should_raise_exception_when_delete_bindings_but_500(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(500)
    patch = mocker.patch('requests.delete', return_value=response)
    binding = {'source': 'one-s', 'destination': 'one-d',
               'routing_key': 'one-r', 'destination_type': 'queue',
               'arguments': None, 'properties_key': '~'}
    try:
        delete_binding(broker=fake_broker(), vhost='EA', binding=Binding(binding))
    except ServerErrorException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/bindings/EA/e/one-s/q/one-d/~')
    patch.assert_called_with(url='https://fake-broker/api/bindings/EA/e/one-s/q/one-d/~',
                             auth=('guest', 'guest'))


def test_should_raise_exception_when_delete_bindings_but_teapot(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(418)
    patch = mocker.patch('requests.delete', return_value=response)
    binding = {'source': 'one-s', 'destination': 'one-d',
               'routing_key': 'one-r', 'destination_type': 'queue',
               'arguments': None, 'properties_key': '~'}
    try:
        delete_binding(broker=fake_broker(), vhost='EA', binding=Binding(binding))
    except Exception as e:
        assert_that(e.args[0]).is_equal_to(418)
    patch.assert_called_with(url='https://fake-broker/api/bindings/EA/e/one-s/q/one-d/~',
                             auth=('guest', 'guest'))


def test_should_check_equality_between_bindings() -> None:
    a = Binding({'source': 'one-s', 'destination': 'one-d',
                 'routing_key': 'one-r', 'destination_type': 'queue',
                 'arguments': None, 'properties_key': '~'})
    b = Binding({'source': 'one-s', 'destination': 'one-d',
                 'routing_key': 'one-r', 'destination_type': 'queue',
                 'arguments': None, 'properties_key': '~'})
    assert_that(a.equals(b)).is_true()
    b = Binding({'source': 'one-s', 'destination': 'one-d',
                 'routing_key': 'one-r', 'destination_type': 'queue',
                 'arguments': None, 'properties_key': 'EE'})
    assert_that(a.equals(b)).is_true()
    b = Binding({'source': 'one-s', 'destination': 'one-d',
                 'routing_key': 'one-r', 'destination_type': 'queue',
                 'arguments': {'something': True}, 'properties_key': 'EE'})
    assert_that(a.equals(b)).is_false()
    assert_that(a.equals([])).is_equal_to(NotImplemented)
