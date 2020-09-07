import os

import pytest
from assertpy import assert_that, fail

from rabbitmqbaselibrary.common.config import Config
from rabbitmqbaselibrary.common.environments import Environments
from rabbitmqbaselibrary.common.exceptions import NotFoundException
from rabbitmqbaselibrary.common.templates import Template
from rabbitmqbaselibrary.policies.policies import get_policies, create_policy, delete_policy, is_present

config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))
envs = Environments(path_file=config.get_file_path('config_files', 'tme_environments.json'))
template: Template = Template(config.get_path('template_files'))


@pytest.mark.integration
def test_should_response_expected_when_get_policies_with_known_vhost() -> None:
    test_env: dict = envs.get_env(env='test')
    result = get_policies(broker=test_env, vhost='EA')
    assert_that(result).is_length(1).contains_only('dead-letter-exchange')


@pytest.mark.integration
def test_should_response_expected_when_get_policies_but_unknown_vhost() -> None:
    test_env: dict = envs.get_env(env='test')
    try:
        get_policies(broker=test_env, vhost='Unknown-Vhost')
    except NotFoundException as e:
        assert_that(e.message).is_equal_to('resource not found')


@pytest.mark.integration
def test_should_create_and_delete_test_policy() -> None:
    test_env: dict = envs.get_env(env='test')
    try:
        delete_policy(broker=test_env, vhost='EA', name='test')
    except NotFoundException as e:
        print('{} is OK here'.format(e.message))
    try:
        create_policy(broker=test_env, vhost='EA', name='test',
                      policy={
                          "pattern": "^amq.",
                          "definition": {"expires": 100},
                          "priority": 0,
                          "apply-to": "queues"})
        assert_that(is_present(broker=test_env, vhost='EA', name='test')).is_true()
        delete_policy(broker=test_env, vhost='EA', name='test')
    except Exception as e:
        fail('it should not fail but {}'.format(e.args[0]))
    assert_that(is_present(broker=test_env, vhost='EA', name='test')).is_false()
