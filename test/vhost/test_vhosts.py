from unittest.mock import MagicMock

from assertpy import assert_that, fail

from rabbitmqbaselibrary.common.exceptions import Unauthorised, VhostAlreadyExists, ServerErrorException, \
    VhostNotFound  # noqa: E402
from rabbitmqbaselibrary.vhost.vhost import get_vhosts, is_present, create_vhost, delete_vhost  # noqa: E402
from ..common.fixtures import mock_response, fake_broker, mock_bad_response_with_status  # noqa: E402


def test_should_provide_trivial_vhost_when_get_vhosts(mocker: MagicMock) -> None:
    response = mock_response([{'name': 'test'}, {'name': 'test1'}])
    mocker.patch('requests.get', return_value=response)
    result = get_vhosts(fake_broker())
    # noinspection PyUnresolvedReferences
    response.json.assert_called_once()  # type: ignore
    assert_that(result).is_length(2).contains_only('test', 'test1')


def test_should_raise_exception_when_get_vhost_but_500(mocker: MagicMock) -> None:
    response1 = mock_bad_response_with_status(500)
    mocker.patch('requests.get', return_value=response1)
    try:
        get_vhosts(fake_broker())
        fail('it should raise exception')
    except Exception as e:
        assert_that(e.args[0]).is_equal_to(str(500))


def test_is_present_positive(mocker: MagicMock) -> None:
    response = mock_response([{'name': 'test'}, {'name': 'test1'}])
    mocker.patch('requests.get', return_value=response)
    a = is_present(fake_broker(), vhost='test1')
    assert_that(a).is_true()


def test_is_present_negative(mocker: MagicMock) -> None:
    response = mock_response([{'name': 'test1'}, {'name': 'test2'}])
    mocker.patch('requests.get', return_value=response)
    a = is_present(fake_broker(), vhost='test')
    assert_that(a).is_false()


def test_should_raise_exception_when_create_vhost_but_already_exists(mocker: MagicMock) -> None:
    response_get = mock_response([{'name': 'test1'}])
    mocker.patch('requests.get', return_value=response_get)
    try:
        create_vhost(broker=fake_broker(), vhost='test1')
        fail('it should raise exception')
    except VhostAlreadyExists as e:
        assert_that(e.vhost).is_equal_to('test1')


def test_should_create_vhost(mocker: MagicMock) -> None:
    response_get = mock_response([{'name': 'test1'}])
    response_put = mock_response({})
    mocker.patch('requests.get', return_value=response_get)
    patch = mocker.patch('requests.put', return_value=response_put)
    try:
        create_vhost(broker=fake_broker(), vhost='test2')
    except Exception as e:
        fail('it should not fail but {}'.format(e.args[0]))
    patch.assert_called_with('https://fake-broker/api/vhosts/test2', auth=('guest', 'guest'))


def test_should_raise_exception_when_create_vhost_but_401(mocker: MagicMock) -> None:
    response_get = mock_response([{'name': 'test2'}])
    response_put = mock_bad_response_with_status(401)
    mocker.patch('requests.get', return_value=response_get)
    mocker.patch('requests.put', return_value=response_put)
    try:
        create_vhost(broker=fake_broker(), vhost='test1')
        fail('it should raise exception')
    except Unauthorised as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/vhosts/test1')


def test_should_raise_exception_when_create_vhost_but_500(mocker: MagicMock) -> None:
    response_get = mock_response([{'name': 'test1'}])
    response_put = mock_bad_response_with_status(500)
    mocker.patch('requests.get', return_value=response_get)
    patch = mocker.patch('requests.put', return_value=response_put)
    try:
        create_vhost(broker=fake_broker(), vhost='test')
        fail('it should raise exception')
    except ServerErrorException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/vhosts/test')
        patch.assert_called_with('https://fake-broker/api/vhosts/test', auth=('guest', 'guest'))


def test_should_delete_vhost(mocker: MagicMock) -> None:
    response_get = mock_response([{'name': 'test'}])
    response_delete = mock_response({})
    mocker.patch('requests.get', return_value=response_get)
    patch = mocker.patch('requests.delete', return_value=response_delete)
    try:
        delete_vhost(broker=fake_broker(), vhost='test')
    except Exception as e:
        fail('it should not fail but {}'.format(e))
    patch.assert_called_with('https://fake-broker/api/vhosts/test', auth=('guest', 'guest'))


def test_should_raise_exception_when_delete_vhost_but_it_doesnt_exist(mocker: MagicMock) -> None:
    response_get = mock_response([{'name': 'test'}])
    response_delete = mock_response({})
    mocker.patch('requests.get', return_value=response_get)
    patch = mocker.patch('requests.delete', return_value=response_delete)
    try:
        delete_vhost(broker=fake_broker(), vhost='test1')
        fail('it should fail.')
    except VhostNotFound as e:
        assert_that(e.vhost).is_equal_to('test1')
        patch.assert_not_called()


def test_should_raise_exception_when_delete_vhost_but_500(mocker: MagicMock) -> None:
    response_get = mock_response([{'name': 'test'}])
    response_delete = mock_bad_response_with_status(500)
    mocker.patch('requests.get', return_value=response_get)
    patch = mocker.patch('requests.delete', return_value=response_delete)
    try:
        delete_vhost(broker=fake_broker(), vhost='test')
        fail('it should raise exception')
    except ServerErrorException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/vhosts/test')
        patch.assert_called_with('https://fake-broker/api/vhosts/test', auth=('guest', 'guest'))


def test_should_raise_exception_when_delete_vhost_but_teapot(mocker: MagicMock) -> None:
    response_get = mock_response([{'name': 'test'}])
    response_delete = mock_bad_response_with_status(418)
    mocker.patch('requests.get', return_value=response_get)
    patch = mocker.patch('requests.delete', return_value=response_delete)
    try:
        delete_vhost(broker=fake_broker(), vhost='test')
        fail('it should raise exception')
    except Exception as e:
        assert_that(e.args[0]).is_equal_to(418)
        patch.assert_called_with('https://fake-broker/api/vhosts/test', auth=('guest', 'guest'))
