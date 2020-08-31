import os

import pytest
from assertpy import assert_that

from common.config import Config
from common.environments import Environments
from common.templates import Template
from exchanges.exchanges import is_present, create_exchange, delete_exchange

config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))
envs = Environments(path_file=config.get_file_path('config_files', 'tme_environments.json'))
template: Template = Template(config.get_path('template_files'))


@pytest.mark.integration
def test_should_check_existing_exchange() -> None:
    test_env: dict = envs.get_env(env='test')
    result = is_present(broker=test_env, vhost='EA', name='amq.topic')
    assert_that(result).is_true()
    result = is_present(broker=test_env, vhost='EA', name='amq.fantasy')
    assert_that(result).is_false()


@pytest.mark.integration
def test_should_create_new_exchange() -> None:
    test_env: dict = envs.get_env(env='test')
    if is_present(broker=test_env, vhost='EA', name='test_exchange'):
        delete_exchange(broker=test_env, vhost='EA', name='test_exchange')
    fanout = template.load_template(name='exchanges/fanout')
    create_exchange(broker=test_env, vhost='EA', name='test_exchange', exchange=fanout)
    result = is_present(broker=test_env, vhost='EA', name='test_exchange')
    assert_that(result).is_true()
    delete_exchange(broker=test_env, vhost='EA', name='test_exchange')
    result = is_present(broker=test_env, vhost='EA', name='test_exchange')
    assert_that(result).is_false()
