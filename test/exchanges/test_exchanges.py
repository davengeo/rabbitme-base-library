from unittest.mock import MagicMock

from assertpy import assert_that, fail

from common.exceptions import NotFoundException, ServerErrorException, Unauthorised, BadRequest
from exchanges.exchanges import get_exchanges, is_present, create_exchange, delete_exchange
from ..common.fixtures import mock_response, fake_broker, mock_bad_response_with_status


def test_should_get_existing_exchanges(mocker: MagicMock) -> None:
    response = mock_response([{'name': 'one'}, {'name': 'two'}])
    patch = mocker.patch('requests.get', return_value=response)
    broker = fake_broker()
    exchanges = get_exchanges(broker=broker, vhost='EA')
    assert_that(exchanges).is_equal_to(['one', 'two'])
    assert_that(is_present(broker=broker, vhost='EA', name='one')).is_true()
    patch.assert_called_with(
        url='https://fake-broker/api/exchanges/EA', auth=('guest', 'guest'))


def test_should_raise_exception_when_get_exchanges_but_404(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(404)
    patch = mocker.patch('requests.get', return_value=response)
    try:
        get_exchanges(broker=fake_broker(), vhost='EA')
        fail('it should raise exception')
    except NotFoundException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/exchanges/EA')
    patch.assert_called_with(
        url='https://fake-broker/api/exchanges/EA', auth=('guest', 'guest'))


def test_should_raise_exception_when_get_exchanges_but_500(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(500)
    patch = mocker.patch('requests.get', return_value=response)
    try:
        get_exchanges(broker=fake_broker(), vhost='EA')
        fail('it should raise exception')
    except ServerErrorException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/exchanges/EA')
    patch.assert_called_with(
        url='https://fake-broker/api/exchanges/EA', auth=('guest', 'guest'))


def test_should_raise_exception_when_get_exchanges_but_401(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(401)
    patch = mocker.patch('requests.get', return_value=response)
    try:
        get_exchanges(broker=fake_broker(), vhost='EA')
        fail('it should raise exception')
    except Unauthorised as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/exchanges/EA')
    patch.assert_called_with(
        url='https://fake-broker/api/exchanges/EA', auth=('guest', 'guest'))


def test_should_raise_exception_when_get_exchanges_but_teapot(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(418)
    patch = mocker.patch('requests.get', return_value=response)
    try:
        get_exchanges(broker=fake_broker(), vhost='EA')
        fail('it should raise exception')
    except Exception as e:
        assert_that(e.args[0]).is_equal_to(418)
    patch.assert_called_with(
        url='https://fake-broker/api/exchanges/EA', auth=('guest', 'guest'))


def test_should_create_exchange(mocker: MagicMock) -> None:
    response = mock_response([])
    patch = mocker.patch('requests.put', return_value=response)
    create_exchange(broker=fake_broker(), vhost='EA', name='test', exchange={'type': 'direct'})
    patch.assert_called_with(url='https://fake-broker/api/exchanges/EA/test', auth=('guest', 'guest'),
                             json={'type': 'direct'})


def test_should_raise_exception_when_create_exchange_but_400(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(400)
    patch = mocker.patch('requests.put', return_value=response)
    try:
        create_exchange(broker=fake_broker(), vhost='EA', name='test', exchange={'type': 'direct'})
    except BadRequest as e:
        assert_that(e.body).is_equal_to({'type': 'direct'})
    patch.assert_called_with(url='https://fake-broker/api/exchanges/EA/test', auth=('guest', 'guest'),
                             json={'type': 'direct'})


def test_should_raise_exception_when_create_exchange_but_404(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(404)
    patch = mocker.patch('requests.put', return_value=response)
    try:
        create_exchange(broker=fake_broker(), vhost='EA', name='test', exchange={'type': 'direct'})
    except NotFoundException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/exchanges/EA/test')
    patch.assert_called_with(url='https://fake-broker/api/exchanges/EA/test', auth=('guest', 'guest'),
                             json={'type': 'direct'})


def test_should_raise_exception_when_create_exchange_but_500(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(500)
    patch = mocker.patch('requests.put', return_value=response)
    try:
        create_exchange(broker=fake_broker(), vhost='EA', name='test', exchange={'type': 'direct'})
    except ServerErrorException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/exchanges/EA/test')
    patch.assert_called_with(url='https://fake-broker/api/exchanges/EA/test', auth=('guest', 'guest'),
                             json={'type': 'direct'})


def test_should_raise_exception_when_create_exchange_but_401(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(401)
    patch = mocker.patch('requests.put', return_value=response)
    try:
        create_exchange(broker=fake_broker(), vhost='EA', name='test', exchange={'type': 'direct'})
    except Unauthorised as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/exchanges/EA/test')
    patch.assert_called_with(url='https://fake-broker/api/exchanges/EA/test', auth=('guest', 'guest'),
                             json={'type': 'direct'})


def test_should_raise_exception_when_create_exchange_but_teapot(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(418)
    patch = mocker.patch('requests.put', return_value=response)
    try:
        create_exchange(broker=fake_broker(), vhost='EA', name='test', exchange={'type': 'direct'})
    except Exception as e:
        assert_that(e.args[0]).is_equal_to(418)
    patch.assert_called_with(url='https://fake-broker/api/exchanges/EA/test', auth=('guest', 'guest'),
                             json={'type': 'direct'})


def test_should_delete_exchange(mocker: MagicMock) -> None:
    response = mock_response([])
    patch = mocker.patch('requests.delete', return_value=response)
    delete_exchange(broker=fake_broker(), vhost='EA', name='test')
    patch.assert_called_with(url='https://fake-broker/api/exchanges/EA/test', auth=('guest', 'guest'))


def test_should_raise_exception_when_delete_exchange_but_404(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(404)
    patch = mocker.patch('requests.delete', return_value=response)
    try:
        delete_exchange(broker=fake_broker(), vhost='EA', name='test')
    except NotFoundException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/exchanges/EA/test')
    patch.assert_called_with(url='https://fake-broker/api/exchanges/EA/test', auth=('guest', 'guest'))


def test_should_raise_exception_when_delete_exchange_but_401(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(401)
    patch = mocker.patch('requests.delete', return_value=response)
    try:
        delete_exchange(broker=fake_broker(), vhost='EA', name='test')
    except Unauthorised as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/exchanges/EA/test')
    patch.assert_called_with(url='https://fake-broker/api/exchanges/EA/test', auth=('guest', 'guest'))


def test_should_raise_exception_when_delete_exchange_but_500(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(500)
    patch = mocker.patch('requests.delete', return_value=response)
    try:
        delete_exchange(broker=fake_broker(), vhost='EA', name='test')
    except ServerErrorException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/exchanges/EA/test')
    patch.assert_called_with(url='https://fake-broker/api/exchanges/EA/test', auth=('guest', 'guest'))


def test_should_raise_exception_when_delete_exchange_but_teapot(mocker: MagicMock) -> None:
    response = mock_bad_response_with_status(418)
    patch = mocker.patch('requests.delete', return_value=response)
    try:
        delete_exchange(broker=fake_broker(), vhost='EA', name='test')
    except Exception as e:
        assert_that(e.args[0]).is_equal_to(418)
    patch.assert_called_with(url='https://fake-broker/api/exchanges/EA/test', auth=('guest', 'guest'))
