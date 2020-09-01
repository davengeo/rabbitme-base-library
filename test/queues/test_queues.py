from assertpy import assert_that, fail

from common.exceptions import NotFoundException, Unauthorised, ServerErrorException, BadRequest
from queues.queues import get_queues, is_present, create_queue, delete_queue
from ..common.fixtures import mock_response, mock_bad_response_with_status, fake_broker


def test_should_get_existing_queues(mocker) -> None:
    response = mock_response([{'name': 'one'}, {'name': 'two'}])
    patch = mocker.patch('requests.get', return_value=response)
    broker = fake_broker()
    exchanges = get_queues(broker=broker, vhost='EA')
    assert_that(exchanges).is_equal_to(['one', 'two'])
    assert_that(is_present(broker=broker, vhost='EA', name='one')).is_true()
    patch.assert_called_with(
        url='https://fake-broker/api/queues/EA', auth=('guest', 'guest'))


def test_should_raise_exception_when_get_queues_but_404(mocker) -> None:
    response = mock_bad_response_with_status(404)
    patch = mocker.patch('requests.get', return_value=response)
    try:
        get_queues(broker=fake_broker(), vhost='EA')
        fail('it should raise exception')
    except NotFoundException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/queues/EA')
    patch.assert_called_with(
        url='https://fake-broker/api/queues/EA', auth=('guest', 'guest'))


def test_should_raise_exception_when_get_queues_but_401(mocker) -> None:
    response = mock_bad_response_with_status(401)
    patch = mocker.patch('requests.get', return_value=response)
    try:
        get_queues(broker=fake_broker(), vhost='EA')
        fail('it should raise exception')
    except Unauthorised as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/queues/EA')
    patch.assert_called_with(
        url='https://fake-broker/api/queues/EA', auth=('guest', 'guest'))


def test_should_raise_exception_when_get_queues_but_500(mocker) -> None:
    response = mock_bad_response_with_status(500)
    patch = mocker.patch('requests.get', return_value=response)
    try:
        get_queues(broker=fake_broker(), vhost='EA')
        fail('it should raise exception')
    except ServerErrorException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/queues/EA')
    patch.assert_called_with(
        url='https://fake-broker/api/queues/EA', auth=('guest', 'guest'))


def test_should_raise_exception_when_get_queues_but_teapot(mocker) -> None:
    response = mock_bad_response_with_status(418)
    patch = mocker.patch('requests.get', return_value=response)
    try:
        get_queues(broker=fake_broker(), vhost='EA')
        fail('it should raise exception')
    except Exception as e:
        assert_that(e.args[0]).is_equal_to(418)
    patch.assert_called_with(
        url='https://fake-broker/api/queues/EA', auth=('guest', 'guest'))


def test_should_create_queue(mocker) -> None:
    response = mock_response([])
    patch = mocker.patch('requests.put', return_value=response)
    create_queue(broker=fake_broker(), vhost='EA', name='test', queue={'test': True})
    patch.assert_called_with(
        url='https://fake-broker/api/queues/EA/test',
        auth=('guest', 'guest'), json={'test': True})


def test_should_raise_exception_when_create_queue_but_400(mocker) -> None:
    response = mock_bad_response_with_status(400)
    patch = mocker.patch('requests.put', return_value=response)
    try:
        create_queue(broker=fake_broker(), vhost='EA', name='test', queue={'test': True})
    except BadRequest as e:
        assert_that(e.body).is_equal_to({'test': True})
        assert_that(e.url).is_equal_to('https://fake-broker/api/queues/EA/test')
    patch.assert_called_with(
        url='https://fake-broker/api/queues/EA/test',
        auth=('guest', 'guest'), json={'test': True})


def test_should_raise_exception_when_create_queue_but_404(mocker) -> None:
    response = mock_bad_response_with_status(404)
    patch = mocker.patch('requests.put', return_value=response)
    try:
        create_queue(broker=fake_broker(), vhost='EA', name='test', queue={'test': True})
    except NotFoundException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/queues/EA/test')
    patch.assert_called_with(
        url='https://fake-broker/api/queues/EA/test',
        auth=('guest', 'guest'), json={'test': True})


def test_should_raise_exception_when_create_queue_but_401(mocker) -> None:
    response = mock_bad_response_with_status(401)
    patch = mocker.patch('requests.put', return_value=response)
    try:
        create_queue(fake_broker(), 'EA', 'test', {'test': True})
    except Unauthorised as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/queues/EA/test')
    patch.assert_called_with(
        url='https://fake-broker/api/queues/EA/test',
        auth=('guest', 'guest'), json={'test': True})


def test_should_raise_exception_when_create_queue_but_500(mocker) -> None:
    response = mock_bad_response_with_status(500)
    patch = mocker.patch('requests.put', return_value=response)
    try:
        create_queue(broker=fake_broker(), vhost='EA', name='test', queue={'test': True})
    except ServerErrorException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/queues/EA/test')
    patch.assert_called_with(
        url='https://fake-broker/api/queues/EA/test',
        auth=('guest', 'guest'), json={'test': True})


def test_should_raise_exception_when_create_queue_but_teapot(mocker) -> None:
    response = mock_bad_response_with_status(418)
    patch = mocker.patch('requests.put', return_value=response)
    try:
        create_queue(broker=fake_broker(), vhost='EA', name='test', queue={'test': True})
    except Exception as e:
        assert_that(e.args[0]).is_equal_to(418)
    patch.assert_called_with(
        url='https://fake-broker/api/queues/EA/test',
        auth=('guest', 'guest'), json={'test': True})


def test_should_delete_queue(mocker) -> None:
    response = mock_response([])
    patch = mocker.patch('requests.delete', return_value=response)
    delete_queue(broker=fake_broker(), vhost='EA', name='test')
    patch.assert_called_with(
        url='https://fake-broker/api/queues/EA/test',
        auth=('guest', 'guest'))


def test_should_raise_exception_when_delete_queue_but_404(mocker) -> None:
    response = mock_bad_response_with_status(404)
    patch = mocker.patch('requests.delete', return_value=response)
    try:
        delete_queue(broker=fake_broker(), vhost='EA', name='test')
    except NotFoundException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/queues/EA/test')
    patch.assert_called_with(
        url='https://fake-broker/api/queues/EA/test',
        auth=('guest', 'guest'))


def test_should_raise_exception_when_delete_queue_but_401(mocker) -> None:
    response = mock_bad_response_with_status(401)
    patch = mocker.patch('requests.delete', return_value=response)
    try:
        delete_queue(broker=fake_broker(), vhost='EA', name='test')
    except Unauthorised as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/queues/EA/test')
    patch.assert_called_with(
        url='https://fake-broker/api/queues/EA/test',
        auth=('guest', 'guest'))


def test_should_raise_exception_when_delete_queue_but_500(mocker) -> None:
    response = mock_bad_response_with_status(500)
    patch = mocker.patch('requests.delete', return_value=response)
    try:
        delete_queue(broker=fake_broker(), vhost='EA', name='test')
    except ServerErrorException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/queues/EA/test')
    patch.assert_called_with(
        url='https://fake-broker/api/queues/EA/test',
        auth=('guest', 'guest'))


def test_should_raise_exception_when_delete_queue_but_teapot(mocker) -> None:
    response = mock_bad_response_with_status(418)
    patch = mocker.patch('requests.delete', return_value=response)
    try:
        delete_queue(broker=fake_broker(), vhost='EA', name='test')
    except Exception as e:
        assert_that(e.args[0]).is_equal_to(418)
    patch.assert_called_with(
        url='https://fake-broker/api/queues/EA/test',
        auth=('guest', 'guest'))
