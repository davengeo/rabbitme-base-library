import os
import sys

from assertpy import assert_that

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../rabbitmqbaselibrary')))
from common.environments import Environments  # noqa: E402


def test_should_open_fake_environment() -> None:
    fake_environments = os.path.abspath(os.path.join(os.path.dirname(__file__), '../resources/fake_environments.json'))
    envs = Environments(fake_environments)
    dev = envs.get_env('dev')
    assert_that(dev).is_equal_to({
        'host': 'yellow-hobbit.rmq.cloudamqp.com',
        'passwd': 'pass_dev',
        'user': 'admin_dev'
    })
    host = envs.get_host('dev')
    assert_that(host).is_equal_to('yellow-hobbit.rmq.cloudamqp.com')
