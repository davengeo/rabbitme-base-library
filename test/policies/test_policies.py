# noinspection PyUnresolvedReferences
import os

import pytest
from assertpy import assert_that, fail

from common.exceptions import NotFoundException, ServerErrorException, BadRequest, Unauthorised
from policies.policies import get_policies, create_policy, delete_policy
from ..common.fixtures import mock_response, fake_broker, mock_bad_response_with_status


@pytest.mark.wip
def test_should_provide_trivial_policies_when_get_policies(mocker) -> None:
    response = mock_response([{'name': 'one'}, {'name': 'two'}])
    mocker.patch('requests.get', return_value=response)
    result = get_policies(broker=fake_broker(), vhost='EA')
    # noinspection PyUnresolvedReferences
    response.json.assert_called_once()
    assert_that(result).is_length(2).contains_only('one', 'two')


@pytest.mark.wip
def test_should_raise_exception_when_get_policies_but_unknown_vhost(mocker) -> None:
    response = mock_bad_response_with_status(404)
    patch = mocker.patch('requests.get', return_value=response)
    try:
        get_policies(broker=fake_broker(), vhost='unknown-vhost')
        fail('it should raise exception')
    except NotFoundException as e:
        assert_that(e.message).is_equal_to('resource not found')


@pytest.mark.wip
def test_should_raise_exception_when_get_policies_but_500(mocker) -> None:
    response = mock_bad_response_with_status(500)
    mocker.patch('requests.get', return_value=response)
    try:
        get_policies(broker=fake_broker(), vhost='EA')
        fail('it should raise exception')
    except ServerErrorException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/policies/EA')


@pytest.mark.wip
def test_should_create_policy_when_create_policy(mocker) -> None:
    response = mock_response({})
    patch = mocker.patch('requests.put', return_value=response)
    try:
        create_policy(broker=fake_broker(), vhost='test', name='policy', policy={})
    except Exception as e:
        fail('it should not fail but {}'.format(e.args))
    patch.assert_called_with(
        url='https://fake-broker/api/policies/test/policy', auth=('guest', 'guest'), json={})


@pytest.mark.wip
def test_should_raise_exception_when_create_policy_but_500(mocker) -> None:
    response = mock_bad_response_with_status(500)
    mocker.patch('requests.put', return_value=response)
    try:
        create_policy(broker=fake_broker(), vhost='test', name='policy', policy={})
        fail('it should raise exception')
    except ServerErrorException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/policies/test/policy')


@pytest.mark.wip
def test_should_raise_exception_when_create_policy_but_400(mocker) -> None:
    response = mock_bad_response_with_status(400)
    mocker.patch('requests.put', return_value=response)
    try:
        create_policy(broker=fake_broker(), vhost='test', name='policy', policy={'no-good': 'policy'})
        fail('it should raise exception')
    except BadRequest as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/policies/test/policy')
        assert_that(e.body).is_equal_to({'no-good': 'policy'})


# noinspection PyPep8Naming
@pytest.mark.wip
def test_should_raise_exception_when_create_policy_but_Exception(mocker) -> None:
    response = mock_bad_response_with_status(512)
    response.reason = 'bad'
    mocker.patch('requests.put', return_value=response)
    try:
        create_policy(broker=fake_broker(), vhost='test', name='policy', policy={'no-good': 'policy'})
        fail('it should raise exception')
    except Exception as e:
        assert_that(e.args[0]).is_equal_to(512)
        assert_that(e.args[1]).is_equal_to('bad')


@pytest.mark.wip
def test_should_delete_policy(mocker) -> None:
    response = mock_response({})
    patch = mocker.patch('requests.delete', return_value=response)
    try:
        delete_policy(broker=fake_broker(), vhost='test', name='policy')
    except Exception as e:
        fail('it should not fail but {}'.format(e.args))
    patch.assert_called_with(url='https://fake-broker/api/policies/test/policy',
                             auth=('guest', 'guest'))


@pytest.mark.wip
def test_should_delete_policy_but_401(mocker) -> None:
    response = mock_bad_response_with_status(401)
    mocker.patch('requests.delete', return_value=response)
    try:
        delete_policy(broker=fake_broker(), vhost='test', name='policy')
    except Unauthorised as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/policies/test/policy')


@pytest.mark.wip
def test_should_delete_policy_but_404(mocker) -> None:
    response = mock_bad_response_with_status(404)
    mocker.patch('requests.delete', return_value=response)
    try:
        delete_policy(broker=fake_broker(), vhost='test', name='policy')
    except NotFoundException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/policies/test/policy')
        assert_that(e.message).is_equal_to('resource not found')


@pytest.mark.wip
def test_should_delete_policy_but_500(mocker) -> None:
    response = mock_bad_response_with_status(500)
    mocker.patch('requests.delete', return_value=response)
    try:
        delete_policy(broker=fake_broker(), vhost='test', name='policy')
    except ServerErrorException as e:
        assert_that(e.url).is_equal_to('https://fake-broker/api/policies/test/policy')
        assert_that(e.message).is_equal_to('server exception')
