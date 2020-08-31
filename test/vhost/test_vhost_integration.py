import os
import sys

import pytest
from assertpy import assert_that, fail

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../lib')))
from vhost.vhost import get_vhosts, is_present, delete_vhost, create_vhost  # noqa: E402
from common.config import Config  # noqa: E402
from common.environments import Environments  # noqa: E402
from common.exceptions import VhostNotFound  # noqa: E402

config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))
envs = Environments(path_file=config.get_file_path('config_files', 'tme_environments.json'))


@pytest.mark.integration
def test_should_response_expected_when_get_vhosts() -> None:
    result = get_vhosts(envs.get_env(env='test'))
    assert_that(result).contains('EA')


@pytest.mark.integration
def test_should_have_ea_as_vhost() -> None:
    result = is_present(envs.get_env(env='test'), 'EA')
    assert_that(result).is_true()


@pytest.mark.integration
def test_should_create_test_as_vhost() -> None:
    vhost = 'testNewVhost'
    environment = envs.get_env(env='test')
    try:
        delete_vhost(broker=environment, vhost=vhost)
    except VhostNotFound as e:
        assert_that(e.vhost).is_equal_to('testNewVhost')
    try:
        create_vhost(broker=environment, vhost=vhost)
        result = is_present(broker=environment, vhost=vhost)
        delete_vhost(broker=environment, vhost=vhost)
        assert_that(result).is_true()
    except Exception as e:
        fail('exception {} when creating host'.format(e.args[0]))
