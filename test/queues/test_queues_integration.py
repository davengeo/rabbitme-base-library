import os

import pytest
from assertpy import assert_that

from common.config import Config
from common.environments import Environments
from common.templates import Template
from queues.queues import is_present, delete_queue, create_queue

config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))
envs = Environments(path_file=config.get_file_path('config_files', 'tme_environments.json'))
template: Template = Template(config.get_path('template_files'))


@pytest.mark.integration
def test_should_create_queue_in_env() -> None:
    test_env: dict = envs.get_env(env='test')
    queue: dict = template.load_template('queues/sample-queue')
    create_queue(broker=test_env, vhost='EA', name='sample-queue', queue=queue)
    result = is_present(broker=test_env, vhost='EA', name='sample-queue')
    assert_that(result).is_true()
    delete_queue(broker=test_env, vhost='EA', name='sample-queue')
    result = is_present(broker=test_env, vhost='EA', name='sample-queue')
    assert_that(result).is_false()
