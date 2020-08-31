import os
import sys

import pytest
from assertpy import assert_that

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../lib')))
from common.config import Config
from common.environments import Environments
from common.templates import Template
from vhost.vhost import create_vhost, delete_vhost
from definitions.definitions import get_definitions, load_definitions

config: Config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))
envs: Environments = Environments(path_file=config.get_file_path('config_files', 'tme_environments.json'))
template: Template = Template(config.get_path('template_files'))


@pytest.mark.integration
def test_should_get_definitions_from_env() -> None:
    broker: dict = envs.get_env(env='test')
    create_vhost(broker=broker, vhost='test-vhost')
    defs = get_definitions(broker=broker, vhost='test-vhost')
    assert_that(defs).contains('rabbit_version', 'policies', 'parameters',
                               'queues', 'exchanges', 'bindings')
    assert_that(defs).contains_entry({'queues': []})
    definitions: dict = template.load_template('definitions/test-vhost')
    load_definitions(broker=broker, vhost='test-vhost', definitions=definitions)
    defs = get_definitions(broker=broker, vhost='test-vhost')
    assert_that(defs).contains_entry(get_queue_entry())
    delete_vhost(broker=broker, vhost='test-vhost')


def get_queue_entry():
    return {
        'queues': [{
            'name': 'test-queue',
            'durable': True,
            'auto_delete': False,
            'arguments': {
                'x-queue-type': 'classic'
            }
        }]
    }
